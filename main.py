from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "سلام! این اولین صفحه پروژه منه 🎮"}