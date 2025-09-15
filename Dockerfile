# Start with a Python base image that includes a slim OS for a smaller image size
# Using Python 3.11 or later is recommended for better sqlite3 compatibility
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for better compatibility and performance
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# This block is for Streamlit Cloud and the pysqlite3 workaround
# This will ensure the module is swapped correctly
COPY app.py .
RUN sed -i '1s/^/__import__("pysqlite3")\nimport sys\nsys.modules["sqlite3"] = sys.modules.pop("pysqlite3")\nimport sqlite3\n/' app.py

# Copy the entire application code and artifacts into the container
COPY src /app/src
COPY artifacts /app/artifacts
COPY mlbook.pdf /app/mlbook.pdf

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
