# MLOps NLP Project

A comprehensive MLOps pipeline for news classification using transformer models, featuring model training, ONNX optimization, FastAPI deployment, and Airflow-based ETL processes.

## Project Architecture

![image (1)](https://github.com/user-attachments/assets/bc23ff32-e6ca-43dd-8810-983342f9a3a3)


## Project Structure

```
├── airflow/
│   └── dags/                 # Airflow DAG definitions
├── api/                      # FastAPI application
├── data/                     # AG News dataset
├── modeling/
│   ├── traditional/         # RNN and LSTM models
│   └── transformers/        # ELECTRA and DistilBERT implementations
├── electra_trainer/         # Trained ELECTRA model
├── electra_onnx/            # ONNX-optimized ELECTRA model
├── distilbert_trainer/      # Trained DistilBERT model
├── distilbert_onnx/         # ONNX-optimized DistilBERT model
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # API service container definition
├── onnx_maker.py          # ONNX conversion utility
├── pyproject.toml         # Poetry dependencies
└── README.md
```

## Features

- **Model Training**: Implementation of both traditional (RNN, LSTM) and transformer-based (ELECTRA, DistilBERT) models
- **Model Tracking**: Integration with MLflow and DagsHub for experiment tracking
- **Model Optimization**: ONNX runtime optimization for improved inference performance
- **API Service**: FastAPI-based REST API for model serving
- **ETL Pipeline**: Airflow-based pipeline for news scraping, processing, and classification
- **Containerization**: Docker-based deployment with proper service orchestration

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Poetry for dependency management
- PostgreSQL (for Airflow metadata)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mlops-nlp
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Build and start the Docker services:
```bash
docker-compose up --build
```

## Components

### 1. Model Training and Optimization

The project supports multiple model architectures:
- Traditional approaches (RNN, LSTM) in `modeling/traditional/`
- Transformer models (ELECTRA, DistilBERT) in `modeling/transformers/`
- Model optimization using ONNX Runtime via `onnx_maker.py`

### 2. FastAPI Service

The API service (`api/app.py`) provides:
- Text classification endpoint at `/predict`
- Health check endpoint at `/health`
- ONNX Runtime inference for optimized performance

### 3. Airflow ETL Pipeline

The ETL pipeline (`airflow/dags/`) performs:
- News scraping from BBC RSS feeds
- Text preprocessing and cleaning
- Model inference using the API service
- Storage in PostgreSQL database

## API Usage

Make predictions using the API:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your news text here"}'
```

Response format:
```json
{
    "label": "Category",
    "confidence": 0.95
}
```

## Airflow Pipeline

The ETL pipeline includes the following tasks:
1. News scraping from BBC RSS
2. Text cleaning and preprocessing
3. Model prediction via API
4. Database storage
5. CSV backup creation

Access the Airflow UI at `http://localhost:8080` with default credentials:
- Username: airflow
- Password: airflow

## Development

1. Export requirements from Poetry:
```bash
poetry export --without-hashes --dev -f requirements.txt > requirements.txt
```

2. Run the API locally:
```bash
poetry run python api/app.py
```

3. Run Airflow locally:
```bash
poetry run airflow standalone
```

## Environment Variables

Required environment variables:
- `AIRFLOW_UID`: Airflow user ID
- `POETRY_VERSION`: Poetry version for Docker build
- `_AIRFLOW_WWW_USER_USERNAME`: Airflow web UI username
- `_AIRFLOW_WWW_USER_PASSWORD`: Airflow web UI password

## Monitoring and Logging

- API logs are stored in the `logging` directory
- Airflow logs are available in `airflow/logs`
- Model training metrics are tracked in MLflow/DagsHub
