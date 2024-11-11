# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the app directory contents into the container at /app
COPY app .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the Flask app
CMD ["python3", "app.py"]