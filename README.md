# End-to-End DevOps CI/CD Project

An end-to-end DevOps portfolio project that automates testing, container image building, vulnerability scanning, publishing, and GitOps-based Kubernetes deployment of a FastAPI application.

## Project Overview

This project demonstrates an automated CI/CD workflow using GitHub Actions, Docker, Trivy, GitHub Container Registry (GHCR), Kubernetes, Helm, and Argo CD. Application and Kubernetes metrics are collected using Prometheus and visualized in Grafana.

The application is deployed to a local Kubernetes cluster running on Minikube.

## Architecture

```mermaid
flowchart TD
    A[Developer pushes code to GitHub] --> B[GitHub Actions CI/CD]
    B --> C[Run automated tests]
    C --> D[Build Docker image]
    D --> E[Scan image with Trivy]
    E --> F[Push image to GHCR]
    F --> G[Update Helm values with image SHA]
    G --> H[Git repository: Helm chart]
    H --> I[Argo CD detects Git change]
    I --> J[Sync Helm chart to Minikube]
    J --> K[Kubernetes Deployment]
    K --> L[FastAPI application]
    L --> M[Health endpoint /health]
    L --> N[Prometheus metrics endpoint /metrics]
    N --> O[Prometheus]
    O --> P[Grafana dashboard and alerting]
```

## Technology Stack

| Area | Technology |
|---|---|
| Application | Python, FastAPI |
| CI/CD | GitHub Actions |
| Containerization | Docker |
| Image vulnerability scanning | Trivy |
| Container registry | GitHub Container Registry (GHCR) |
| Container orchestration | Kubernetes, Minikube |
| Packaging and deployment configuration | Helm |
| GitOps continuous delivery | Argo CD |
| Metrics collection | Prometheus |
| Monitoring and visualization | Grafana |

## CI/CD Workflow

1. Code changes are pushed to the GitHub repository.
2. GitHub Actions runs automated tests.
3. A Docker image is built.
4. Trivy scans the image for vulnerabilities; the configured gate fails on detected HIGH/CRITICAL vulnerabilities that meet the scan settings.
5. The image is published to GHCR using an immutable Git commit SHA tag.
6. The workflow updates the image tag in the Helm values file.
7. Argo CD detects the Git change and synchronizes the Helm chart.
8. Kubernetes performs the deployment and uses readiness/liveness probes to check application health.

## Kubernetes and Helm

The FastAPI application is deployed with a Helm chart located at `helm/devops-api`.

The deployment configuration includes:
- Configurable replica count and container image tag.
- CPU and memory requests and limits.
- Readiness and liveness probes using `/health`.
- Non-root container execution (UID/GID 10001).
- Disabled privilege escalation, dropped Linux capabilities, and `RuntimeDefault` seccomp profile.
- ClusterIP service for internal application access.
- ServiceMonitor resource for Prometheus scraping.

## GitOps with Argo CD

Argo CD continuously monitors the repository's Helm chart and reconciles the cluster with the desired state stored in Git. Automated sync is configured with pruning and self-healing.

Git is the source of truth for deployment configuration.

## Monitoring and Alerting

Prometheus scrapes application metrics exposed at `/metrics` through a Kubernetes ServiceMonitor.

The Grafana dashboard, **DevOps API Monitoring**, includes:
- Total HTTP requests by handler.
- HTTP request rate.
- HTTP error rate.
- 95th percentile request latency.
- Kubernetes container CPU usage.
- Kubernetes container memory usage.

A Grafana alert rule, **DevOps API Target Down**, monitors the availability of the application target.

## Rollback Strategy

The primary rollback strategy is Git-based rollback through the Helm image tag:

1. Identify the last known-good image SHA.
2. Revert the relevant image-tag change in Git (or commit the known-good tag to the Helm values file).
3. Argo CD detects the desired-state change and synchronizes it.
4. Kubernetes rolls out the previous application image.
5. Verify Argo CD sync/health, Deployment rollout status, pod readiness, and the `/health` endpoint.

A controlled rollback and recovery test was performed using these image tags:

- Previous image: `084d940b537392f5e52fec3f7d761013f18d12eb`
- Restored image: `0cd284da10d41c13e84814a7aaff932b7372f6b8`

Both rollback and recovery were verified with the application healthy. Kubernetes `kubectl rollout undo` is a secondary manual option, but Git-based rollback is preferred because Argo CD reconciles the cluster from Git.

## Repository Structure

```text

devops-end-to-end-cicd/
├── .github/
│   └── workflows/          # CI/CD workflow
├── app/                    # FastAPI application
├── argocd/                 # Argo CD application manifests
├── helm/
│   └── devops-api/         # Helm chart
├── k8s/                    # Kubernetes manifests
├── tests/                  # Automated tests
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

> Update this tree if the actual repository structure differs; it is intended as a high-level overview.

## Local Access

The project runs on Minikube. Example port-forward commands:

**FastAPI service**
```powershell
kubectl port-forward svc/devops-api -n devops-api 8000:8000
```

- API: http://localhost:8000/
- Health check: http://localhost:8000/health
- Prometheus metrics: http://localhost:8000/metrics

**Prometheus**
```powershell
kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9090:9090
```
- Prometheus UI: http://localhost:9090

**Grafana**
```powershell
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
```
- Grafana UI: http://localhost:3000

## Key DevOps Practices Demonstrated

- Automated CI pipeline with test execution.
- Container image build, vulnerability scanning, and registry publishing.
- Immutable image tagging by Git commit SHA.
- Helm-based Kubernetes deployment configuration.
- GitOps continuous delivery using Argo CD.
- Kubernetes health probes and resource requests/limits.
- Prometheus application metrics and Grafana dashboards/alerting.
- Git-based rollback and recovery validation.
- Container security hardening.

## Scope and Environment

This is a learning and portfolio project deployed to a local Minikube cluster. It demonstrates DevOps workflows in a local environment and does not claim production cloud deployment.

## Author

**Sakthi Manikandan**

GitHub: [Sakthi-Manikandan](https://github.com/Sakthi-Manikandan)
