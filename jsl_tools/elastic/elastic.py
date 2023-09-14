import argparse

IMAGE_ELASTIC = "docker.elastic.co/elasticsearch/elasticsearch:8.3.3"
IMAGE_KIBANA = "docker.elastic.co/kibana/kibana:8.3.3"

# Version 8.10.0 is broken - running bin/elasticsearch-reset-passwords kills the container. 

def start_elastic(args):
    from subprocess import check_call
    check_call("docker network prune --force".split())
    check_call("docker network create elastic_network".split())
    check_call("docker pull {}".format(IMAGE_ELASTIC).split())
    check_call("docker pull {}".format(IMAGE_KIBANA).split())
    
    
    cmd = ("docker run" 
           " --name elastic"
           " --detach"
        #    " --net elastic_network"
           " --memory 1GB"
        #    " --rm"
           " -p 9200:9200"
           " -p 9300:9300"
           " -e ELASTIC_PASSWORD=123456" # User elastic
        #    " -v /home/jsl/data/elastic/data:/usr/share/elasticsearch/data"
        #    " -v /home/jsl/data/elastic/config:/usr/share/elasticsearch/config"
           " -e 'discovery.type=single-node'"
           " -e 'xpack.security.enabled=false'"
           " {image}").format(image=IMAGE_ELASTIC)
    print(cmd)
    check_call(cmd.split())
    

    cmd = ("docker run"
           " --name kibana"
           " --detach"
        #    " --net elastic_network"
        #    " --rm"
           " -p 5601:5601"
           " -e 'ELASTICSEARCH_HOSTS=http://elastic:9200'"
           " -e 'xpack.security.enabled=false'"
           " {image}").format(image=IMAGE_KIBANA)
    print(cmd)
    check_call(cmd.split())

    # If container exists with 
    # ERROR: Elasticsearch exited unexpectedly, with exit code 78
    # Its due to memory constraints on the host system.
    # Temporary solution is to run sudo sysctl -w vm.max_map_count=262144
    # However this resets after reboot.
    # For a permenent solution configure it in /etc/sysctl.conf.
    # https://stackoverflow.com/questions/56937171/efk-elasticsearch-1-exited-with-code-78-when-install-elasticsearch

    
def check_elastic_is_running(args):
    # docker cp elastic:/usr/share/elasticsearch/config/certs/http_ca.crt .
    # export ELASTIC_PASSWORD="123456"
    # curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
    pass


def stop_elastic(args):
    from subprocess import call
    call("docker stop elastic".split())
    call("docker rm elastic".split())
    call("docker stop kibana".split())
    call("docker rm kibana".split())
    call("docker network rm elastic_network".split())

def push_example_data(args):
    # pip3 install elasticsearch
    from elasticsearch import Elasticsearch

    # docker cp elastic:/usr/share/elasticsearch/config/certs/http_ca.crt .

    es = Elasticsearch(
        "https://localhost:9200",
        ca_certs="/home/johl/http_ca.crt",
        basic_auth=("elastic", "123456")
    )
    
    # pip3 install rich
    from rich import print as pprint
    pprint(es.info().body)

    mappings = {
            "properties": {
                "title": {"type": "text", "analyzer": "english"},
                "director": {"type": "text", "analyzer": "standard"},
                "year": {"type": "integer"},
                "wiki_page": {"type": "keyword"}
        }
    }
    
    es.indices.create(index="movies", mappings=mappings)

    for i in range(1,10000):
        doc = {
            "title": "my_awsome_movie_{}".format(i),
            "director": "a_director_name".format(i),
            "year": 2000+i,
            "wiki_page": "https://en.wikipedia.org/wiki/{}".format(i)
        }
                
        es.index(index="movies", id=i, document=doc)

def push_example_data2(args):
    
    import subprocess
    result = subprocess.run(["ping", "localhost", "-c", "1"], capture_output=True, text=True                    )
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    print_raw = result.stdout
    ping = result.stdout.split("time=")[1].split(" ")[0]
    ping = 42

    from datetime import datetime
    time = datetime.now()

    #time in 10seconds
    import random
    from datetime import timedelta
    time_randomness = datetime.now() + timedelta(seconds=random.randint(0, 100))

    # Random number between 0 and 100
    value = random.randint(0, 100)

    # Random charecter between a and z
    import string
    charecter = random.choice(string.ascii_lowercase)

    # Random word from a list
    words = ["cat", "dog", "mouse", "tiger"]
    word = random.choice(words) 

    from elasticsearch import Elasticsearch
    es = Elasticsearch(
        "https://localhost:9200",
        ca_certs="/home/johl/http_ca.crt",
        basic_auth=("elastic", "123456")
    )

    # pip3 install rich
    from rich import print as pprint
    pprint(es.info().body)
    
    print("Pushing data to elastic... ctrl+c to stop")
    index = 0
    try:
        while True:
            doc = {
                "ping": ping,
                "ping_raw": print_raw,
                "time": time,
                "time_randomness": time_randomness,
                "random_value": value,
                "random_charecter": charecter,
                "random_word": word,
            }
            resp = es.index(index="the_random_collection", id=index, document=doc)
            pprint(resp)
            pprint(resp['result'])
    except KeyboardInterrupt:
        pass


def open_in_browser(args):
    import webbrowser
    webbrowser.open('http://localhost:5601')
    import subprocess

    # Might need -it at some point    
    print("\n\n*** Feching pairing token from elastic container... ***\n\n")
    cmd = "docker exec elastic /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana" 
    subprocess.check_call(cmd.split())
    # print(cmd)

    print("\n\n*** Feching verification code from kibana container... ***\n\n")
    cmd = "docker exec kibana bin/kibana-verification-code"
    subprocess.check_call(cmd.split())
    print(cmd)

    print("\n\n*** Login using credentials ***\n\n")
    print("Username: elastic")
    print("Password: 123456")
    # subprocess.check_call(cmd.split())

   






def add_parsers(parser):
    elastic_parser = parser.add_parser('elastic', help='Start and stop and elastic container for data logging', formatter_class=argparse.RawTextHelpFormatter)
    elastic_parser.set_defaults(func=lambda x: elastic_parser.print_help())
    sub_parser = elastic_parser.add_subparsers()

    start_parser = sub_parser.add_parser('start', help="Start an elastic container")
    start_parser.set_defaults(func=start_elastic)

    start_parser = sub_parser.add_parser('stop', help="Start an elastic container")
    start_parser.set_defaults(func=stop_elastic)

    open_parser = sub_parser.add_parser('open_in_browser', help="Open an kibana in the browser")
    open_parser.set_defaults(func=open_in_browser)

    push_parser = sub_parser.add_parser('push_data', help="Example of how to push data to elastic")
    push_parser.set_defaults(func=push_example_data)

    push2_parser = sub_parser.add_parser('push_data2', help="Example of how to push data to elastic")
    push2_parser.set_defaults(func=push_example_data2)


# echo "GROK pattern -- 
# %{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:loglevel} %{DATA:message} \#\#\[%{DATA:path}\:%{NUMBER:line}\(%{DATA:function}\)\]
# %{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:loglevel} %{DATA:data} \#\#\[%{GREEDYDATA:path}/%{DATA:file}\:%{NUMBER:line}\(%{DATA:function}\)\]
# "
