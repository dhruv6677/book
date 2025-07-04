# 📚 Automated Book Publisher AI

## 🔍 Objective

Create a fully automated AI-powered system that:

- Scrapes book chapters from [Wikisource](https://en.wikisource.org/wiki/The_Gates_of_Morning)
- Applies AI-based rewriting and reviewing (Gemini)
- Allows human-in-the-loop editing via UI
- Stores all versions using ChromaDB
- Enables intelligent version retrieval using RL-style feedback-based ranking

---

## 🚀 Features

| Module                | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| ✅ Scraping           | Uses Playwright to extract chapter content and full-page screenshots       |
| ✅ AI Writer & Reviewer | Uses Gemini 1.5 to rewrite and review chapters                            |
| ✅ Human-in-the-Loop  | Editable text area for manual edits + save functionality                   |
| ✅ Versioning         | Stores raw, AI, reviewed, human-edited, and final versions in ChromaDB      |
| ✅ Feedback (RL Search)| Users vote 👍/👎 and scores are updated to rank versions dynamically        |
| ✅ Streamlit UI       | Interactive interface for complete workflow control and visualization      |

---

## 🛠️ Tech Stack

- **Python** – Core development
- **Playwright** – Web scraping + screenshot capture
- **Gemini API** (Google GenerativeAI) – Text rewriting and review
- **ChromaDB** – Version storage and metadata management
- **Streamlit** – UI and human-in-the-loop interaction
- **RL-inspired scoring** – Simple reinforcement-like logic based on user feedback

---

## 📂 Project Structure

book_publisher_ai/
├── assets/ # Stores scraped content, screenshots, etc.
├── ai_agents/
│ ├── writer.py # AI rewriting using Gemini
│ └── reviewer.py # AI review/refinement
├── scraping_folder/
│ └── scraper.py # Scraper using Playwright
├── db/
│ └── chroma_handler.py # ChromaDB versioning and RL score handling
├── main.py # Streamlit UI
├── .env # Stores GEMINI_API_KEY get from user from frontend side
└── README.md # 📘 You're here


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/dhruv6677/book.git
cd book_publisher_ai

### 2. Create Environment and Install Dependencies
conda create -n bookenv python=3.10 or 3.11
conda activate bookenv
pip install -r requirements.txt
playwright install

# 💻 How to Run
# Start the App

    streamlit run main.py

# 2. Use the Sidebar to Navigate:

# Select chapter number (e.g., Chapter 1)

# Scrape content from Wikisource

# Rewrite using Gemini

# Review using Gemini

# Edit manually and save as “Human Edited”

# Publish the final version

# View Stored Versions:

# Enable "Show Stored Versions" in the sidebar

# Select and preview any stored document version

# Rate Content:

# Provide feedback (👍 / 👎)

# Scores update live using RL-inspired logic

✅ How It Works
| Step | Description                          |
| ---- | ------------------------------------ |
| 1️⃣  | Select a chapter number              |
| 2️⃣  | Scrape content + screenshot          |
| 3️⃣  | Rewrite & review with AI             |
| 4️⃣  | Human can edit final version         |
| 5️⃣  | Publish to store all versions        |
| 6️⃣  | Upvote/downvote for RL-based ranking |


# ### Note:- chroma_store folder created after save final file in db 