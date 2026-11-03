from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="DevOps CI/CD Demo API",
    description="A sample API for an end-to-end DevOps project",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "End-to-end deployment successful!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


# Enable Prometheus application metrics
Instrumentator().instrument(app).expose(app)
