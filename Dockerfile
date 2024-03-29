FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -U scikit-learn
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "main.py" ]
