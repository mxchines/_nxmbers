# Dockerfile.app

FROM python:3.12-slim

# Install necessary dependencies for your app service
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        # Add other necessary system packages \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create a virtual environment
RUN python -m venv /venv

# Copy the requirements file into the container
COPY requirements_app.txt .

# Upgrade pip and install Python dependencies
RUN /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements_app.txt

# Copy the application code into the container
COPY . .

# Set the environment variable to use the virtual environment
ENV PATH="/venv/bin:$PATH"

# Set the command to run the application
CMD ["python", "app.py"]
