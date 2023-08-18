FROM python:3.11-alpine

WORKDIR /app


COPY . .

RUN cd /app && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple [--timeout=60]

EXPOSE 8000

CMD ["main:app", "--host","0.0.0.0","--port","8000","--reload"]