# Deployment Instructions

This document outlines how to build the Docker image for the Agent API service (Part 1) and run it using Docker.

## Prerequisites

*   [Docker](https://www.docker.com/get-started/) installed and running on your machine.
*   Access to your API keys and configuration (e.g., Google Cloud credentials, OpenAI API key) needed by the application. It's recommended to provide these via environment variables.

## 1. Building the Docker Image

Navigate to the root directory of this project in your terminal (the directory containing `part1/`, `part2/`, and `Dockerfile`).

Build the Docker image using the `Dockerfile` located in the `part2/` directory. We'll tag the image for easy reference.

```bash
docker build -t agent-api:latest -f part2/Dockerfile .