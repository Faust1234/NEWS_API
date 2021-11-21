FROM python:3.9

RUN pip install --upgrade pip

COPY . /app
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]