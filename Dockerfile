# Use a smaller base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy project files
COPY ./api/ api/
COPY requirements.txt requirements.txt
COPY ollama_functions.py ollama_functions.py
COPY user_products.csv user_products.csv

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Ollama
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# Start Ollama serve and pull the model
RUN ollama serve & \
    sleep 10 && \
    ollama pull phi3

# Move the customized Ollama functions
RUN mv ollama_functions.py /usr/local/lib/python3.9/site-packages/langchain_experimental/llms/ollama_functions.py

# Expose the application port
EXPOSE 8001

# Run the main application file on container startup
CMD ["python", "api/app.py"]