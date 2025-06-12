import os
import json
from markdown import markdown
from bs4 import BeautifulSoup

def md_to_text(md_content):
    html = markdown(md_content)
    return BeautifulSoup(html, "html.parser").get_text()

def chunk_text(text, size=500, overlap=100):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size - overlap)]

data_chunks = []

# ✅ 1. Load and chunk course content (.md files)
notes_path = "tools-in-data-science-public"
for root, _, files in os.walk(notes_path):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path, encoding="utf-8") as f:
                text = md_to_text(f.read())
                chunks = chunk_text(text)
                for chunk in chunks:
                    data_chunks.append({
                        "text": chunk,
                        "source": f"https://tds.s-anand.net/#{file}"
                    })

# ✅ 2. Load and chunk Discourse data
with open("discourse_data.json", encoding="utf-8") as f:
    discourse = json.load(f)
    for post in discourse:
        chunks = chunk_text(post["text"])
        for chunk in chunks:
            data_chunks.append({
                "text": chunk,
                "source": post["url"]
            })

# ✅ 3. Save to chunks.json
with open("chunks.json", "w", encoding="utf-8") as out:
    json.dump(data_chunks, out, indent=2)

print(f"✅ Chunking complete! Total chunks: {len(data_chunks)}")
