FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 3000

CMD ["gunicorn" "-b" ":3000" "app:app"]