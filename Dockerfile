FROM python:3.11.7-bullseye
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
RUN python -m venv opt/my-venv
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip install -Ur --default-timeout=50000 -r requirements.txt
CMD ["python", "api.py"]