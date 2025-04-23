# Use a Python base image compatible with ARMv7
FROM arm32v7/python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY main.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the script is executable
RUN chmod +x /app/main.py

# Command to run the application
CMD ["python", "-u", "main.py"]