# ⚡ brainwave-discord (Groq-Powered Discord Academic & Assistant Bot)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0%2B-5865F2.svg?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.3%2070B-f34f29.svg)](https://groq.com/)

An ultra-fast, intelligent Discord bot powered by **Groq API (`llama-3.3-70b-versatile`)**. It acts as a dual-purpose assistant: automatically parsing research paper PDFs into structured academic study guides, while handling casual server chatter with a dynamic, witty, and customizable persona.

---

## 📌 System Architecture

```text
┌──────────────────────┐       ┌───────────────────────┐       ┌────────────────────────┐
│   Discord Channel    │ ────> │  Python Bot Backend   │ ────> │       Groq Cloud       │
│                      │       │                       │       │  (Llama-3.3-70b Engine)│
│ • PDF Attachments    │       │ • PyPDF Text Extractor│       │                        │
│ • @Bot Mentions      │ <──── │ • Dual Prompt Router  │ <──── │ • 500+ Tokens/Sec LLM  │
│ • Name/Keyword Pings │       │ • Message Chunking    │       │ • Sub-Second Synthesis │
└──────────────────────┘       └───────────────────────┘       └────────────────────────┘

```

---

## ✨ Key Features

* **📄 Instant PDF Paper Synthesis:** Upload any research paper PDF into Discord. The bot extracts text and formats it into a structured Markdown study guide in sub-seconds.
* **⚡ Blazing Fast Speed:** Leverages Groq's high-speed Llama 3.3 70B inference engine for near-instant responses.
* **🎭 Dual-Prompt Persona Router:**
* **Academic Mode (`temp=0.2`):** Factual, structured research synthesis without hallucination.
* **Casual Mode (`temp=0.95`):** High-creativity, witty server companion supporting custom character protocols and localized street slang/banter.


* **🛡️ Mention & Attachment Guard:** Prevents channel spam by only responding when explicitly `@mentioned`, when configured keywords are dropped, or when a `.pdf` file is attached.

---

## 🎯 Generated Study Document Format

When an academic paper is uploaded, the bot formats its output into this standardized Markdown layout:

```markdown
# 📚 Study Notes: [Topic]

## 🎯 Core Executive Summary
> High-level executive overview of the paper's primary contribution.

## 🔑 Key Takeaways & Contributions
* Bulleted breakdown of core findings and experimental results.

## 🛠️ Methodologies & Architecture
* Technical breakdown of algorithms, system design, or protocols used.

## ❓ Revision & Self-Test Questions
1. Conceptual test questions to help verify comprehension.

```

---

## 🛠️ Tech Stack & Dependencies

| Component | Library / Service | Purpose |
| --- | --- | --- |
| **Language** | Python 3.10+ | Core runtime environment |
| **Bot Gateway** | `discord.py` | Asynchronous Discord Gateway connection |
| **LLM Engine** | Groq API (`llama-3.3-70b-versatile`) | High-speed LLM inference |
| **PDF Extraction** | `pypdf` | Extracting text from uploaded PDF documents |
| **Configuration** | `python-dotenv` | Secure environment variable handling |

---

## 🚀 Quick Start & Setup

### 1. Prerequisites

Ensure you have generated your API credentials:

* **Discord Bot Token** ([Discord Developer Portal](https://discord.com/developers/applications))
* **Groq API Key** ([Groq Cloud Console](https://console.groq.com/))

### 2. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

```

### 3. Install Dependencies

```bash
pip install discord.py groq pypdf python-dotenv

```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GROQ_API_KEY=your_groq_api_key_here

```

### 5. Run the Bot

```bash
python main.py

```

---

## 🔒 Security Best Practices

Ensure your `.env` file containing secret tokens is **never committed** to version control. Add a `.gitignore` file with:

```text
.env
__pycache__/
*.pyc
```
