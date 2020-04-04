from locust import HttpLocust, TaskSet, task, between
from bs4 import BeautifulSoup
import random
import logging

import urllib3
urllib3.disable_warnings()

_logger = logging.getLogger(__name__)




class UserBehavior(TaskSet):

    def is_static_file(self,f):
        if f.startswith("/") or f.startswith(self.host):
            return True
        else:
            return False

    def fetch_static_assets(self, response):
        resource_urls = set()
        soup = BeautifulSoup(response.text, "html.parser")

        for res in soup.find_all(src=True):
            url = res['src']
            if self.is_static_file(url):
                resource_urls.add(url)
            else:
                _logger.debug("Skipping: " + url)

        for res in soup.find_all(href=True):
            url = res['href']
            if self.is_static_file(url):
                resource_urls.add(url)
            else:
                _logger.debug( "Skipping: " + url)

        for url in set(resource_urls):
            #Note: If you are going to tag different static file paths differently,
            #this is where I would normally do that.
            self.client.get(url, name="(Static File)")

    def on_start(self):
        self.client.verify = False
        # self.login()
        

    def login(self):
        # GET login page to get csrftoken from it
        response = self.client.get('/accounts/login/')
        csrftoken = response.cookies['csrftoken']
        # POST to login page with csrftoken
        self.client.post('/accounts/login/',
                         {'username': 'username', 'password': 'P455w0rd'},
                         headers={'X-CSRFToken': csrftoken})

    @task(1)
    def index(self):
        response = self.client.get('/')
        self.fetch_static_assets( response)

    # @task(2)
    # def heavy_url(self):
    #     self.client.get('/heavy_url/')

    # @task(2)
    # def another_heavy_ajax_url(self):
    #     # ajax GET
    #     self.client.get('/another_heavy_ajax_url/',
    #     headers={'X-Requested-With': 'XMLHttpRequest'})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)
