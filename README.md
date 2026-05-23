# Scalable Data Processing API

Memory-Efficient Large-Scale CSV Join System using FastAPI.

## Features

- Out-of-core CSV processing
- Hash partition join
- Streaming architecture
- FastAPI backend
- BackgroundTasks execution
- ThreadPoolExecutor concurrency
- RabbitMQ worker architecture
- Memory-efficient joins

## Installation

pip install -r requirements.txt

## Generate Dataset

python generate_data.py

## Run BackgroundTasks API

uvicorn api.api_background_tasks:service --reload --port 8000

## Run ThreadPool API

uvicorn api.api_threadpool:service --reload --port 8001