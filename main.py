import os
import io
import asyncio
import discord
from discord.ext import commands
from groq import Groq
import pypdf
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validate environment variables before starting
if not DISCORD_BOT_TOKEN or not GROQ_API_KEY:
    raise ValueError("Missing API Keys! Please check your .env file.")

# Initialize Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)

# Initialize Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------------------------------------------------
# PROMPTS
# ---------------------------------------------------------

ACADEMIC_PROMPT = """
You are an expert academic tutor and research assistant.
The user provided a research paper or study material. Synthesize it into a structured Markdown note.

Rules:
- Strictly base your response on the provided input. Do not make up facts.
- Use clear bullet points and bold headers.

Structure:
# 📚 Study Notes: [Topic]
## 🎯 Core Executive Summary
## 🔑 Key Takeaways & Contributions
## 🛠️ Methodologies & Architecture
## ❓ Revision & Self-Test Questions
"""

CASUAL_PROMPT = """
You are a witty, sarcastic, and funny AI buddy on Discord.
When responding to casual chatter:
1. Be humorous, playful, and sharp.
2. Respond in Bangla/Banglish with street-smart slang (e.g., 'আরে মামা', 'প্যারা নাই', 'মাথা নষ্ট', 'ছাতার মাথা', 'চিল কর', 'আঁতলামি করিস না').
3. Keep responses relatively short (1-3 sentences max).
4. Playfully roast users if they say something silly, but always remain a fun and helpful companion.
"""

def extract_pdf_text(file_bytes: bytes) -> str:
    """Extracts text from uploaded PDF files synchronously."""
    reader = pypdf.PdfReader(io.BytesIO(file_bytes))
    text = "".join([page.extract_text() or "" for page in reader.pages])
    return text[:12000]

@bot.event
async def on_ready():
    print(f"✅ Groq Bot is live as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Check triggers
    is_mentioned = bot.user in message.mentions
    has_pdf = any(att.filename.endswith(".pdf") for att in message.attachments)
    
    # Respond only if mentioned or a PDF is attached
    if not (is_mentioned or has_pdf):
        await bot.process_commands(message)
        return

    content_to_process = ""
    is_academic = False

    # 1. Process PDF attachments (Academic Mode)
    if has_pdf:
        for attachment in message.attachments:
            if attachment.filename.endswith(".pdf"):
                status_msg = await message.channel.send("📄 Extracting text from PDF...")
                pdf_bytes = await attachment.read()
                
                # Run the blocking PDF extraction in a separate thread
                content_to_process = await asyncio.to_thread(extract_pdf_text, pdf_bytes)
                is_academic = True
                
                await status_msg.delete()
                break

    # 2. Process Text Messages
    if not content_to_process and message.content:
        clean_text = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()

        if clean_text:
            content_to_process = clean_text
            
            # Academic check
            academic_keywords = ["paper", "abstract", "research", "methodology", "summary", "notes", "thesis", "study"]
            if len(content_to_process) > 250 or any(kw in content_to_process.lower() for kw in academic_keywords):
                is_academic = True

    # Handle blank mentions
    if not content_to_process:
        await message.channel.send("কী রে মামা, কিছু না লিখে শুধু মেনশন দিলি কেন? 🤨")
        return

    # Select System Prompt and Temperature
    system_prompt = ACADEMIC_PROMPT if is_academic else CASUAL_PROMPT
    temp = 0.2 if is_academic else 0.95
    
    status_msg = await message.channel.send("⚡ Thinking...")

    try:
        # Run Groq API call in a thread to prevent blocking the gateway
        completion = await asyncio.to_thread(
            groq_client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content_to_process}
            ],
            temperature=temp,
            max_tokens=1500
        )
        response_text = completion.choices[0].message.content

        await status_msg.delete()

        # Handle Discord 2000-character message limit
        if len(response_text) <= 2000:
            await message.channel.send(response_text)
        else:
            # Chunk the message safely
            for i in range(0, len(response_text), 1900):
                await message.channel.send(response_text[i:i+1900])

    except Exception as e:
        await status_msg.edit(content=f"❌ Error querying Groq: {str(e)}")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)