# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app.py into the container
COPY app.py .

# Expose port 5000
EXPOSE 5000

# The command to run your app
CMD ["python", "app.py"]