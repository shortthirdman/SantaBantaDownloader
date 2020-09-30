FROM python:3.8.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUTF8 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
COPY main.py .
COPY util.py .
COPY pcloud_client.py .
COPY ./static ./static
COPY ./templates ./templates

RUN pip install -r requirements.txt --no-cache-dir
RUN export FLASK_APP=main
RUN export FLASK_ENV=production
RUN export FLASK_DEBUG=0
RUN export FLASK_RUN_PORT=5000

EXPOSE 5000
#ENTRYPOINT [ "python" ] 
#CMD [ "demo.py" ] 

#CMD ["python", "main.py"]
CMD ["flask", "run"]