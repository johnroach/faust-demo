service=faustdemo
worker=faustdemo.app
partitions=1
replication-factor=1

bash:
	docker-compose run --user=$(shell id -u) ${service} bash

# Build docker image
build:
	docker-compose build

restart:
	docker-compose restart ${service}

run:
	docker-compose up

logs:
	docker-compose logs

# Removes old containers, free's up some space
remove:
	# Try this if this fails: docker rm -f $(docker ps -a -q)
	docker-compose rm --force -v

remove-network:
	docker network rm faustdemo_default

stop:
	docker-compose stop

run-dev: build run

clean: stop remove remove-network

# Kafka related
list-topics:
	docker-compose exec kafka kafka-topics --list --zookeeper zookeeper:32181

create-topic:
	docker-compose exec kafka kafka-topics --create --zookeeper zookeeper:32181 --replication-factor ${replication-factor} --partitions ${partitions} --topic ${topic-name}

# Faust commands related
send-page-view-event:
	docker-compose exec -e SIMPLE_SETTINGS=faustdemo.settings ${service} faust -A ${worker} send page_views '${payload}'

list-agents:
	docker-compose exec -e SIMPLE_SETTINGS=faustdemo.settings ${service} faust -A ${worker} agents

docker-build:
	docker build -t faustdemo .

docker-run:
	docker run faustdemo

native-run:
	FAUST_DATADIR=.data1 SIMPLE_SETTINGS=faustdemo.settings poetry run faustdemo worker --web-port=8088