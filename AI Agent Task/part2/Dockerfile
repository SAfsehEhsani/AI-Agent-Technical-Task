# part2/Dockerfile

# Stage 1: Build Stage (Optional but good for complex builds, less needed here)
# Using a slim image is generally better for production as it's smaller.
# Using buster or bullseye provides necessary build tools if you have complex dependencies.
FROM python:3.11-slim-buster AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    # Use a non-root user for security best practices
    # PEP 436 recommends VIRTUAL_ENV for identifying the venv path
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Create directories for the application and virtual environment
RUN mkdir /app
WORKDIR /app

# Copy requirements.txt first to leverage Docker caching
COPY ../requirements.txt .

# Create and activate the virtual environment
RUN python -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --upgrade pip && \
    # Install dependencies from requirements.txt
    # Use --no-cache-dir to prevent pip from caching, saving space
    # Consider using --user if you weren't using a venv or installing to a non-standard path
    $VIRTUAL_ENV/bin/pip install -r requirements.txt


# Stage 2: Production Stage
# Use a smaller runtime image if possible, copying only the venv and app code
# python:3.11-slim-buster is already quite minimal, so we can continue from it
# If you had complex C extensions, you might need to use the builder image
FROM python:3.11-slim-buster

# Use the same environment variables for consistency
ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Create app directory
RUN mkdir /app
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
# Copy the 'part1' directory containing your FastAPI app
COPY ../part1 /app/part1/
# Copy the .env file if you are using it directly in the app (ensure it's in the root)
# COPY ../.env /app/.env # Be cautious with secrets in images! Environment variables are better.


# Expose the port your application listens on
# Your FastAPI app runs on 8000 locally, but Gunicorn/Uvicorn can run on 80 inside the container
EXPOSE 80

# Command to run the application
# We'll use Gunicorn with Uvicorn workers for production
# -w <workers>: Number of worker processes. Good starting point is (2*CPU)+1.
# -k uvicorn.workers.UvicornWorker: Use the Uvicorn worker class
# part1.main:app: The location of your FastAPI app instance
# --bind 0.0.0.0:80: Bind to all interfaces on port 80
# Consider adding --threads <threads_per_worker> if your app benefits from threading (e.g., I/O bound tasks)
# Also consider --max-requests <num> --max-requests-jitter <num> for robustness
# And --timeout <seconds> for worker timeouts

ARG GUNICORN_WORKERS=4 # Define workers as a build argument, default to 4
# Use --log-level info for production logging
CMD ["gunicorn", "part1.main:app", "-w", "${GUNICORN_WORKERS}", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "--log-level", "info"]

# Alternative CMD using just uvicorn (less common for production due to single process):
# CMD ["uvicorn", "part1.main:app", "--host", "0.0.0.0", "--port", "80"]