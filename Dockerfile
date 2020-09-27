FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install fastapi uvicorn requests
EXPOSE 80
COPY ./app /app