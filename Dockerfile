FROM locustio/locust



# todo: install scrapy
RUN mkdir -p /app;pip install bs4

ENV LOCUSTFILE_PATH='/app/locustfile.py'
ADD locustfile.py /app/