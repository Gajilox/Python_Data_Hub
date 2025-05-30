# Python Data Hub

This repository contains two Dockerized Python applications for interacting with a data hub:

## Folders

1. **Publish**
   - Contains a Python script to send `POST` requests for writing variables.
   - Includes:
     - `main.py`: Interactive script for sending `POST` requests.
     - `Dockerfile`: Defines the Docker image for ARMv7 architecture.
     - `requirements.txt`: Lists Python dependencies.

2. **Subscribe**
   - Contains a Python script to fetch data using `GET` requests.
   - Includes:
     - `main.py`: Script for fetching data periodically.
     - `Dockerfile`: Defines the Docker image for ARMv7 architecture.
     - `requirements.txt`: Lists Python dependencies.

## Usage

### Build and Run the Docker Images

1. Navigate to the respective folder (`Publish` or `Subscribe`).
2. Build the Docker image:
   ```bash
   docker buildx build --platform linux/arm/v7 -t <image-name>:<tag> --push .