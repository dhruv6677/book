from db.chroma_handler import list_all_documents
import streamlit as st
from pathlib import Path
import os
import subprocess
from db.chroma_handler import store_version, update_score, get_ranked_documents
# === Utility Functions ===


def load_file(filepath):
    file = Path(filepath)
    return file.read_text(encoding="utf-8") if file.exists() else ""


def save_file(filepath, content):
    os.makedirs(Path(filepath).parent, exist_ok=True)
    Path(filepath).write_text(content, encoding="utf-8")


# === UI Setup ===
st.set_page_config(page_title="AI Book Publisher", layout="wide")
st.title("📚 Automated Book Publisher")

# In main.py (top sidebar section)
st.sidebar.header("🔐 Gemini API Key")
user_api_key = st.sidebar.text_input(
    "Enter your Gemini API key", type="password")

if user_api_key:
    # Save to a .env file for subprocess access
    with open(".env", "w") as f:
        f.write(f"GEMINI_API_KEY={user_api_key}\n")
    st.success("✅ API key saved!")

# === Step 0: Chapter URL input ===
st.sidebar.header("Chapter URL")
default_url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_{}"
# chapter_url = st.sidebar.text_input("Paste chapter URL:", default_url)
chapter_number = st.sidebar.selectbox("Select Chapter Number", [1,2])
chapter_url = default_url.format(chapter_number)
# st.sidebar.markdown(f"**Chapter URL:**\n{chapter_url}")
print(f"**Chapter URL:**\n{chapter_url}")

# === Step 1: Manual Controls ===
st.sidebar.header("action Controls")

# if st.sidebar.button("🔍 Scrape Chapter"):
#     st.info("📥 Running scraper...")
#     subprocess.run(["python", "scraping_folder/scraper.py"])
#     st.success("✅ Chapter scraped and saved.")
if st.sidebar.button("🔍 Scrape Chapter"):
    st.info(f"Scraping Chapter {chapter_number}...")
    subprocess.run(
        ["python", "scraping_folder/scraper.py", str(chapter_number)])
    st.success("✅ Chapter scraped and saved.")

if st.sidebar.button("✍️ Rewrite with Gemini"):
    st.info("🔄 Rewriting...")
    subprocess.run(["python", "ai_agents/writer.py"])
    st.success("✅ Rewritten version saved.")

if st.sidebar.button("🧠 Review with Gemini"):
    st.info("🔎 Reviewing...")
    subprocess.run(["python", "ai_agents/reviewer.py"])
    st.success("✅ Reviewed version saved.")

# === Step 2: Version selection ===
st.sidebar.header("Select Version")
version = st.sidebar.radio(
    "Choose version", ["Original", "AI Edited", "Reviewed", "Human Edited"])
# Step 1: Chapter selection
chapter_num = st.sidebar.selectbox("Select Chapter", options=[
                                   1, 2, 3], format_func=lambda x: f"Chapter {x}")

# Step 2: Dynamic file map based on chapter number
file_map = {
    "Original": f"assets/chapter{chapter_num}_raw.txt",
    "AI Edited": f"assets/chapter{chapter_num}_ai.txt",
    "Reviewed": f"assets/chapter{chapter_num}_reviewed.txt",
    "Human Edited": f"assets/chapter{chapter_num}_human.txt",
}

# file_map = {
#     "Original": "assets/chapter1_raw.txt",
#     "AI Edited": "assets/chapter1_ai.txt",
#     "Reviewed": "assets/chapter1_reviewed.txt",
#     "Human Edited": "assets/chapter1_human.txt",
# }

# === Load content ===
# If human edit not exists, prefill it from reviewed
if version == "Human Edited" and not Path(file_map[version]).exists():
    reviewed = load_file(file_map["Reviewed"])
    save_file(file_map["Human Edited"], reviewed)

content = load_file(file_map[version])
st.subheader(f"{version} Content")
edited_text = st.text_area("Edit below:", value=content, height=400)

# === Save Human Edit ===
if version == "Human Edited" and st.button("💾 Save Human Edit"):
    save_file(file_map["Human Edited"], edited_text)
    st.success("✅ Human Edited version saved.")

# === Publish Final ===
if st.button("🚀 Publish Final Version"):
    final_path = "assets/chapter1_final.txt"
    save_file(final_path, edited_text)

    # Store all versions in ChromaDB
    chapter_id = "chapter1"
    versions = {
        "raw": "assets/chapter1_raw.txt",
        "ai": "assets/chapter1_ai.txt",
        "reviewed": "assets/chapter1_reviewed.txt",
        "human": "assets/chapter1_human.txt",
        "final": final_path
    }

    for ver, path in versions.items():
        store_version(chapter_id, ver, path)

    st.success("✅ Final version saved and all versions stored in ChromaDB.")

# step 4: View Stored Versions from ChromaDB == =
st.sidebar.header("📦 View Stored Versions")

if st.sidebar.checkbox("Show Stored Versions"):
    from db.chroma_handler import list_all_versions, get_chapter_version

    all_versions = list_all_versions()

    if all_versions:
        selected_doc = st.sidebar.selectbox(
            "Select a stored version", all_versions)
        content = get_chapter_version(selected_doc)
        st.subheader(f"📝 Stored Content: {selected_doc}")
        st.text_area("Document Content", value=content, height=400)
    else:
        st.warning("No versions stored yet in ChromaDB.")

# list_all_documents() # for debugging purpose

# === Show Screenshot ===
screenshot_path = "assets/screenshot.png"
with st.expander("🖼️ Click here to View Screenshot"):
    try:
        st.image(screenshot_path, caption="Web Page Screenshot",
                 use_container_width=True)
    except Exception as e:
        st.warning("sorry we Don't have image yet scrape chapter first")

st.markdown("---")
st.header("🧠 Feedback on Stored Versions")

ranked_docs = get_ranked_documents()

for doc_id, meta, content in ranked_docs:
    # Use session state to store scores
    score_key = f"score_{doc_id}"
    if score_key not in st.session_state:
        st.session_state[score_key] = meta.get("score", 0)

    with st.expander(f"📄 {doc_id} | 🔢 Score: {st.session_state[score_key]:.2f}"):
        st.text_area("Document Preview",
                     value=content[:1000], height=200,
                     disabled=True, key=f"preview_{doc_id}")

        col1, col2 = st.columns(2)

        if col1.button(f"👍 Upvote {doc_id}", key=f"up_{doc_id}"):
            new_score = update_score(doc_id, reward=1.0)
            st.session_state[score_key] = new_score
            st.success(f"👍 Score updated to {new_score:.2f}")

        if col2.button(f"👎 Downvote {doc_id}", key=f"down_{doc_id}"):
            new_score = update_score(doc_id, reward=0.0)
            st.session_state[score_key] = new_score
            st.warning(f"👎 Score updated to {new_score:.2f}")
