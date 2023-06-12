FROM python:3.9.6
WORKDIR /app

# Download the key.json file using wget
RUN apt-get update && apt-get install -y wget
RUN wget $JSON_KEY

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the key.json file to the working directory
COPY key.json .

# Copy the application code
COPY . .

EXPOSE 5000 
CMD exec gunicorn --bind :5000 main:app --workers 1 --threads 1 --timeout 60
