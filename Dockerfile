FROM python:3.11-alpine

WORKDIR /app


COPY . .

RUN cd /app && \
    echo 'FUCK GFW' &&\
    pip install -r requirements.txt

EXPOSE 8000

CMD ["main:app", "--host","0.0.0.0","--port","8000","--reload"]