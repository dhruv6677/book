import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def load_text(file_path):
    return Path(file_path).read_text(encoding="utf-8") if Path(file_path).exists() else ""


def save_text(file_path, content):
    Path(file_path).write_text(content, encoding="utf-8")


def review_chapter(text):
    model = genai.GenerativeModel("gemini-1.5-flash")  # or "gemini-pro"
    prompt = (
        "You're an experienced book editor. Please review the following AI-written chapter for clarity, "
        "tone, grammar, and storytelling consistency. Rewrite it to improve readability without changing the meaning:\n\n"
        + text
    )
    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    chapter_num = 1
    input_path = f"assets/chapter{chapter_num}_ai.txt"
    output_path = f"assets/chapter{chapter_num}_reviewed.txt"

    print("📄 Loading AI-written chapter...")
    ai_text = load_text(input_path)

    print("🛠 Reviewing with Gemini...")
    reviewed_text = review_chapter(ai_text)

    print("💾 Saving reviewed version...")
    save_text(output_path, reviewed_text)

    print(f"✅ Reviewed chapter saved to {output_path}")
