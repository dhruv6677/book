import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key
load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_text(file_path):
    return Path(file_path).read_text(encoding="utf-8") if Path(file_path).exists() else ""


def save_text(file_path, content):
    Path(file_path).write_text(content, encoding="utf-8")


def rewrite_with_gemini(text):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        "Rewrite the following chapter in engaging and fluent language while preserving its meaning:\n\n"
        + text
    )

    response = model.generate_content(prompt)
    return response.text.strip()


if __name__ == "__main__":
    chapter_num = 1
    input_path = f"assets/chapter{chapter_num}_raw.txt"
    output_path = f"assets/chapter{chapter_num}_ai.txt"

    print("📖 Loading raw chapter...")
    raw_text = load_text(input_path)

    print("✨ Rewriting with Gemini...")
    rewritten = rewrite_with_gemini(raw_text)

    print("💾 Saving rewritten version...")
    save_text(output_path, rewritten)

    print(f"✅ Rewritten chapter saved to {output_path}")
