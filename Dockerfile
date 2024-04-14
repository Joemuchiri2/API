# Use the official Python 3.11 image
FROM python:3.11.8

# Set the working directory inside the container
WORKDIR /API

# Copy the requirements.txt file to the container
COPY requirements.txt tmp/requirements.txt

# Install the Python dependencies
RUN python -m pip install --timeout 300000 -r tmp/requirements.txt

# Copy the rest of the application code to the container
COPY . /API/

# Expose port 8077 to the outside world
EXPOSE 8077

# Command to run the application when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8077"]
