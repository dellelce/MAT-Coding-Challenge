# my personal python3 build by mkit
FROM dellelce/py-base as py

RUN pip3 install --no-cache -U paho-mqtt mysql-connector pip setuptools

COPY src /app/src

CMD ["python3", "-u", "/app/src/storage.py"]
