FROM python:3.9
RUN mkdir -p /src/
WORKDIR /src/
COPY requirements.txt /src/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /src/app
WORKDIR /src/app
ENV APP_ENV development
EXPOSE 8000
#CMD ["uvicorn", "--log-level debug" ,"main:app"]
CMD ["python", "main.py"]