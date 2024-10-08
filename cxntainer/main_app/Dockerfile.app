# Dockerfile.app

FROM python:3.12-slim

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        r-base \
        r-base-dev \
        libssl-dev \
        libcurl4-openssl-dev \
        libffi-dev \
        && rm -rf /var/lib/apt/lists/*

# Verify R installation
RUN R --version

# Optionally set R_HOME environment variable
ENV R_HOME /usr/lib/R

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Create a virtual environment
RUN python -m venv /venv

# Upgrade pip and install Python dependencies
RUN /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the environment variable to use the virtual environment
ENV PATH="/venv/bin:$PATH"

# Set the command to run your application
CMD ["python", "app.py"]
