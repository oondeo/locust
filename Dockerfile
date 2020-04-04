FROM locustio/locust


ADD locustfile.py /

# todo: install scrapy
RUN pip install bs4