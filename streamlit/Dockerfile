
FROM python:3.9

WORKDIR /app

COPY requirements.txt app/requirements.txt

RUN pip install -r app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r app/requirements.txt

COPY . /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501"]