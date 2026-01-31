# Use an official Python runtime based on your local version (3.13)
FROM python:3.13-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure output is sent directly to terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (needed for ImageKit/Pillow)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first (for better cache utilization)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project code
COPY . /app/

# Change directory to where manage.py is located
# (Since your manage.py is inside the 'youtube' folder)
WORKDIR /app/youtube

# Expose port 8000
EXPOSE 8000

# Command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]