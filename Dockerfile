# Start with a Python base image that includes a slim OS for a smaller image size
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install a minimal build toolchain and the CPU-only version of torch first for stability
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy the rest of the requirements file and install the remaining Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY src /app/src
COPY artifacts /app/artifacts
COPY mlbook.pdf /app/mlbook.pdf
COPY app.py .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
