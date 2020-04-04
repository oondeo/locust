
* https://docs.locust.io/en/stable/running-locust-docker.html

# USING
Launch one slave for each 100 users. Locustfile is already included. You can force a host ip to test development pages.

```
docker run --name locustmaster --add-host www.xxx.com:51.77.30.179 -e TARGET_URL=https://www.xxx.com -e LOCUST_OPTS="--step-load" -e LOCUST_MODE=master -e LOCUST_MASTER_PORT=5557 --rm -ti -p 8089:8089 -v $PWD/locustfile.py:/locustfile.py  oondeo/locust
docker run --link locustmaster --add-host www.xxx.com:51.77.30.179 -e TARGET_URL=https://www.xxx.com -e LOCUST_MODE=slave -e LOCUST_MASTER_HOST=locustmaster -e LOCUST_MASTER_PORT=5557 --rm -d -v $PWD/locustfile.py:/locustfile.py oondeo/locust
```
