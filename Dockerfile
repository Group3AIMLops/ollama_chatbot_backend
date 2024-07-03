# Base image for a Python environment
FROM python:3.9  
# Adjust Python version if needed

# Copy project files
COPY ./api/ api/
COPY requirements.txt requirements.txt
COPY ollama_functions.py ollama_functions.py
COPY user_products.csv user_products.csv
RUN ls

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

RUN mv ollama_functions.py \usr\local\lib\python3.9\site-packages\langchain_experimental\llms\ollama_functions.py

EXPOSE 8001


# Run the main application file on container startup
CMD ["python", "api/app.py"]