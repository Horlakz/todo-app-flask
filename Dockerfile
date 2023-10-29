FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]