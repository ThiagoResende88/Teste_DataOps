# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY dashboard_agrofit.py .
COPY process_data.py .
COPY analyze_data.py .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# IMPORTANT: Mount your gcp_credentials.json file as a volume when running the container.
# Example: docker run -v /path/to/your/gcp_credentials.json:/app/gcp_credentials.json your-image-name

# Run the application
CMD ["streamlit", "run", "dashboard_agrofit.py"]
