# Kubernetes Event Summarizer

## Overview

Kubernetes Event Summarizer is a Python-based web application that interacts with a Kubernetes cluster to fetch pod events, summarize them using OpenAI's language model, and present the output via a RESTful API. This tool helps operations teams understand Kubernetes events more efficiently.

![kubernetes_event_summarizer.png](/kubernetes_event_summarizer.png)

## Project Structure

```plaintext
K8S-EVENT-SUMMARIZER/
├── app/
│   ├── .env                # Environment variables file (e.g., OpenAI API key)
│   ├── app.py              # Main Python application code
│   └── requirements.txt    # Python dependencies
├── .dockerignore           # Files and directories to ignore during Docker build
├── .gitignore              # Files and directories to ignore in Git
├── Dockerfile              # Docker configuration for building the application image
├── README.md               # Project documentation
└── test-pod.yaml           # Kubernetes YAML file for deploying a test pod
```

## Requirements

- Python 3.9+
- Docker
- Kubernetes cluster (e.g., Docker Desktop Kubernetes, Minikube)
- pip (Python package installer)

## Installation

- Clone the repository:

```bash
git clone https://github.com/sprider/k8s-event-summarizer.git
cd k8s-event-summarizer
```

- Set up the Python environment:

Ensure you have Python 3.9 or higher installed. Create a virtual environment and install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r app/requirements.txt
```

- Configure environment variables:

Create a `.env` file in the `app/` directory and set the OpenAI API key:

```plaintext
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Run Locally

- Start the application:

```bash
python3 app/app.py
```

- Access the API:

The application will run on `http://localhost:8000`. Use an API tool like Postman or `curl` to interact with the endpoint:

```bash
curl http://localhost:8000/summarize/<pod-name>
```

### Run with Docker

- Build the Docker image:

```bash
docker build -t k8s-event-summarizer .
```

- Run the container:

```bash
docker run -p 8000:8000 --env-file app/.env k8s-event-summarizer
```

## Deploying a Test Pod

Use the `test-pod.yaml` file to deploy a test pod in your Kubernetes cluster to generate events:

```bash
kubectl apply -f test-pod.yaml
```

## API Endpoints

- `GET /summarize/<pod-name>`: Fetches and summarizes events for the specified pod name.

![postman-output.png](/postman-output.png)

## Dependencies

The required dependencies for this project are listed in `app/requirements.txt`:

```plaintext
Flask==2.2.5
openai==1.54.3
python-dotenv==0.21.0
kubernetes==31.0.0
```
