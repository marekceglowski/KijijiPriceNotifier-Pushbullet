FROM python

COPY ./src/main.py /
COPY ./src/requirements.txt /

RUN pip3 install -r /requirements.txt

ENTRYPOINT ["python3", "-u", "/main.py"]
