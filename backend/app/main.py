from fastapi import FastAPI

app = FastAPI(title="EduBot API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "EduBot is running!", "status": "ok"}


@app.get("/health")
def health():
    return {"status": "healthy"}
