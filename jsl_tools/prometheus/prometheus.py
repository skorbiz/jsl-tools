import argparse
import os

IMAGE_PROMETHEUS = "prom/prometheus"
IMAGE_GRAFANA = "grafana/grafana"

def start_prometheus(args):
    from subprocess import check_call
    check_call("docker pull {}".format(IMAGE_PROMETHEUS).split())
    
    config_file = os.path.join(os.path.dirname(__file__), "prometheus.yml")
    cmd = ("docker run" 
           " --name prometheus"
           " --detach"
           " --rm"
           " --network host"
           " -v {config_file}:/etc/prometheus/prometheus.yml"
        # -v prometheus-data:/prometheus \ 
           " -p 9090:9090"
           " {image}").format(config_file=config_file, image=IMAGE_PROMETHEUS)
    print(cmd)
    check_call(cmd.split())

    cmd = ("docker run" 
           " --name grafana"
           " --detach"
           " --rm"
           " --network host"
           " -p 3000:3000"
           " {image}").format(image=IMAGE_GRAFANA)    
    print(cmd)
    check_call(cmd.split())
    # More graphana options here:
    #  https://collabnix.com/run-and-configure-grafana-docker-image/


def checkprometheus_is_running(args):
    # docker cp elastic:/usr/share/elasticsearch/config/certs/http_ca.crt .
    # export ELASTIC_PASSWORD="123456"
    # curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
    pass


def stop_prometheus(args):
    from subprocess import call
    call("docker stop prometheus".split())
    call("docker rm prometheus".split())
    call("docker stop grafana".split())
    call("docker rm grafana".split())


def push_example_data(args):
    #pip install prometheus-client
    # https://github.com/prometheus/client_python#exporting-to-a-pushgateway

    from prometheus_client import Summary, Counter, Gauge, Histogram, start_http_server
    import random
    import time

    # Create a metric to track time spent and requests made.
    REQUEST_TIME = Summary('my_summary', 'Time spent processing request')
    UPDATE_COUNT = Counter('my_update_count', 'Number of updates')
    GAUGE = Gauge('my_gauge', 'This is my gauge')
    HISTOGRAM = Histogram('my_histogram', 'This is my histogram')



    # Decorate function with metric.
    @REQUEST_TIME.time()
    def process_request(t):
        """A dummy function that takes some time."""
        time.sleep(t)

    start_http_server(8000)

    while True:
        UPDATE_COUNT.inc(random.randint(1, 100))
        GAUGE.set(random.random() * 15 - 5)
        HISTOGRAM.observe(random.random() * 10)
        process_request(random.random())





def open_in_browser(args):
    import webbrowser
    webbrowser.open('http://localhost:3000')

    print("\n\n*** Login credentials ***\n\n")
    print("Username: admin")
    print("Password: admin")

    print("Add data source -> Prometheus -> http://localhost:9090")
    print("Prometheus webpage: http://localhost:9090/")

   

def add_parsers(parser):
    prometheus_parser = parser.add_parser('prometheus', help='Start and stop and prometheus container for data logging', formatter_class=argparse.RawTextHelpFormatter)
    prometheus_parser.set_defaults(func=lambda x: prometheus_parser.print_help())
    sub_parser = prometheus_parser.add_subparsers()

    start_parser = sub_parser.add_parser('start', help="Start an prometheus container")
    start_parser.set_defaults(func=start_prometheus)

    start_parser = sub_parser.add_parser('stop', help="Start an prometheus container")
    start_parser.set_defaults(func=stop_prometheus)

    open_parser = sub_parser.add_parser('open_in_browser', help="Open an kibana in the browser")
    open_parser.set_defaults(func=open_in_browser)

    push_parser = sub_parser.add_parser('push_data', help="Example of how to push data to elastic")
    push_parser.set_defaults(func=push_example_data)