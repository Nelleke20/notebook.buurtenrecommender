FROM python:3.8

WORKDIR /app

COPY requirements.txt /

RUN apt-get update
RUN apt-get install -y gdal-bin libgdal-dev g++
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app

EXPOSE 8000:8000

CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000", "--reload"]