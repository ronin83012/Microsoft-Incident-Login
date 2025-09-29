# Use official Python image
FROM python:3.11-slim

# Force unbuffered output
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy files into the container
COPY . .

# Expose port 8080 (your server runs on this)
EXPOSE 8080

# Run your Python server
CMD ["python", "backend.py"]
