# Use the official Python image as a parent image
FROM public.ecr.aws/docker/library/python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools wheel
# Install project dependencies directly into the container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# If pycurl is not in your requirements.txt, install it separately
RUN pip install pycurl

# Copy entrypoint script and give it execution permissions
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy the rest of the project files into the container
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Use entrypoint.sh to run the server
ENTRYPOINT ["/app/entrypoint.sh"]
