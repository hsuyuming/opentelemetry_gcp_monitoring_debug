### reproduce step
- step1: python env setup
```cmd
pip install -r requirements.txt
cd prometheus-fastapi-instrumentator
pip3 install -e .
```
- step2: get your machine ip
- step3: replace <your ip> to your ip
```cmd
# File need to be modify
fastapi_example/main.py
fastapi_example/config/prometheus.yml
fastapi_example/config/collector-agent.yml
```
- step4. usgin docker-compose launch collector & prometheus 
```cmd
cd fastapi_example
docker-compose up
```
- step5. open the other terminal to launch fastapi
```cmd
cd fastapi_example
python main.py
```
- endpoint:
```
http://<your ip>:5000/foo
http://<your ip>:5000/bar
http://<your ip>:5005/metrics
http://<your ip>:9090

```