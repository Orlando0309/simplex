# Use an official Python runtime as a parent image
FROM python:3.12.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
     glpk-utils \ 
     glpk-doc\
    libglpk-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install fastapi uvicorn pulp

# Expose the port the app runs on
EXPOSE 8000

# Run app.py when the container launches
CMD ["fastapi", "run", "main.py", "--port", "8000"]