FROM python:3.11.7-bullseye
# Install system libraries
RUN apt-get update && apt-get install -y libgl1-mesa-glx
WORKDIR /app
# Create a virtual environment
RUN python3 -m venv /opt/my-venv
RUN pip install --upgrade pip
COPY . /app
# Install Flask and other dependencies
RUN pip install --no-cache-dir flask python-dotenv opencv-python pymongo
RUN pip install --no-cache-dir tensorflow
EXPOSE 8080
CMD ["python", "api.py"]