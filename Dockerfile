FROM python:3.10

WORKDIR /fundup

RUN apt-get update

RUN apt install -y libgl1-mesa-glx

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./app

EXPOSE 5000

CMD ["python", "./app/main.py"]
