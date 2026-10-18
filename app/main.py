from fastapi import FastAPI

app = FastAPI(
    title="DevOps CI/CD Demo API",
    description="A sample API for an end-to-end DevOps project",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the DevOps CI/CD project!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
