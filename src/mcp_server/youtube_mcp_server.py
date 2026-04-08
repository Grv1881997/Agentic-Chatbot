from fastapi import FastAPI
import yt_dlp

app = FastAPI()

@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": "search_youtube",
                "description": "Search YouTube videos",
                "parameters": {"query": "string"}
            }
        ]
    }

@app.post("/tools/search_youtube")
def search_youtube(data: dict):
    query = data.get("query")
    print(f"Received search query: {query}")
    ydl_opts = {
        "quiet": True,
        "extract_flat": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch5:{query}", download=False)

    videos = []
    for entry in result["entries"]:
        videos.append({
            "title": entry.get("title"),
            "url": entry.get("url"),
            "channel": entry.get("uploader")
        })

    return {"videos": videos}