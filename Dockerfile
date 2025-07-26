# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Flask/Gunicorn will run on
EXPOSE 3000

# Run the app using Gunicorn (production-grade server)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:app"]

