# Start with a Python base image that includes a slim OS for a smaller image size
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for sqlite3 and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install pysqlite3 to ensure the correct version of sqlite3
RUN pip install pysqlite3

# Copy the entire application code into the container
COPY src /app/src
COPY artifacts /app/artifacts
COPY mlbook.pdf /app/mlbook.pdf
COPY app.py .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]