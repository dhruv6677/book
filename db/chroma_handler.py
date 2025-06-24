import chromadb
from pathlib import Path

client = chromadb.PersistentClient(path="./chroma_store")
collection = client.get_or_create_collection(name="book_versions")


# def store_version(chapter_id: str, version_name: str, filepath: str):
#     path = Path(filepath)
#     if path.exists():
#         content = path.read_text(encoding="utf-8")
#         doc_id = f"{chapter_id}_{version_name}"
#         collection.add(documents=[content], ids=[doc_id])
#         print(f"✅ Stored {doc_id} in ChromaDB")
#     else:
#         print(f"⚠️ File {filepath} not found, skipping...")

def store_version(chapter_id: str, version_name: str, filepath: str, score: float = 0.5):
    path = Path(filepath)
    if path.exists():
        content = path.read_text(encoding="utf-8")
        doc_id = f"{chapter_id}_{version_name}"
        collection.add(
            documents=[content],
            ids=[doc_id],
            metadatas=[{"score": 0.5}]
        )
        print(f"✅ Stored {doc_id} in ChromaDB")
    else:
        print(f"⚠️ File {filepath} not found, skipping...")


def list_all_versions():
    results = collection.get()
    return results['ids']


def get_chapter_version(doc_id):
    result = collection.get(ids=[doc_id])
    return result['documents'][0] if result['documents'] else "Document not found."


# def list_all_documents():
#     results = collection.get()
#     print(f"🗂 Total stored documents: {len(results['ids'])}")
#     for doc_id in results['ids']:
#         print(f"📄 ID: {doc_id}")
def list_all_documents():
    results = collection.get()
    ids = results.get("ids", [])
    metadatas = results.get("metadatas", [])

    print(f"🗂 Total stored documents: {len(ids)}")

    for i, doc_id in enumerate(ids):
        meta = metadatas[i] if metadatas and i < len(metadatas) else {}
        score = meta.get("score", "N/A")
        print(f"📄 ID: {doc_id} | 🔢 Score: {score}")


# --- RL-style functions ---
# def get_ranked_documents():
#     results = collection.get()
#     docs = zip(results["ids"], results["metadatas"], results["documents"])
#     ranked = sorted(docs, key=lambda x: x[1].get("score", 0), reverse=True)
#     return ranked


def get_ranked_documents():
    results = collection.get()
    docs = zip(results["ids"], results["metadatas"], results["documents"])
    ranked = sorted(
        docs,
        key=lambda x: (x[1] or {}).get("score", 0),  # Safely handle None
        reverse=True
    )
    return ranked


def update_score(doc_id, reward, learning_rate=0.1):
    result = collection.get(ids=[doc_id])
    metadata = result["metadatas"][0]
    current_score = metadata.get("score", 0.5)
    new_score = current_score + learning_rate * (reward - current_score)
    collection.update(ids=[doc_id], metadatas=[{"score": new_score}])
    return new_score
