# Use the official Python image as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK data
RUN python download_nltk_modules.py

# Run any additional setup scripts (e.g., downloading GloVe)
RUN python download_glove_gigaword.py

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "server.wsgi:application", "--bind", "0.0.0.0:8000"]
