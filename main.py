from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from agent import app

app_api = FastAPI()


@app_api.get("/")
def home():
    return {"message": "GAP Agent is live"}


# Chat API
@app_api.get("/chat")
async def chat(message: str):
    async for chunk in app.stream_query(message):
        try:
            return {
                "response": chunk["content"]["parts"][0]["text"]
            }
        except:
            continue

    return {"response": "No response"}


# UI Route
@app_api.get("/ui", response_class=HTMLResponse)
def ui():
    with open("index.html") as f:
        return f.read()