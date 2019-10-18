service=faustdemo
worker=faustdemo.app
partitions=1
replication-factor=1

bash:
	docker-compose run --user=$(shell id -u) ${service} bash

build: ## Builds docker image
	docker-compose build

restart: ## Restarts a singular service. Ex: make restart kafka # will only restart kafka in docker-compose
	docker-compose restart ${service}

run: ## brings docker-compose up
	docker-compose up

logs: ## uses docker-compose to show logs
	docker-compose logs

remove: ## Removes old containers, free's up some space
	# Try this if this fails: docker rm -f $(docker ps -a -q)
	docker-compose rm --force -v

remove-network: ## Removes default networks
	docker network rm faustdemo_default

stop: ## Stops docker-compose
	docker-compose stop

run-dev: build run ## Builds and runs docker-compose

clean: stop remove remove-network ## Cleans up your docker-compose environment and stops docker-compose

# Kafka related
list-topics: ## Lists available topics in Kafka
	docker-compose exec kafka kafka-topics --list --zookeeper zookeeper:32181

create-topic: ## Creates topics in Kafka
	docker-compose exec kafka kafka-topics --create --zookeeper zookeeper:32181 --replication-factor ${replication-factor} --partitions ${partitions} --topic ${topic-name}

# Faust commands related
list-agents: ## Lists running faust agents
	docker-compose exec -e SIMPLE_SETTINGS=faustdemo.settings ${service} faust -A ${worker} agents

docker-build:
	docker build -t faustdemo .

docker-run:
	docker run faustdemo

run-dev-tilt:
	kubectx docker-desktop && tilt up

native-run: ## Native run.
	 poetry update && FAUST_DATADIR=.data1 SIMPLE_SETTINGS=faustdemo.settings poetry run faustdemo worker --web-port=8088

test: ## Runs tests
	SIMPLE_SETTINGS=faustdemo.settings poetry run pytest

# HELP ########################################################################

.PHONY: help
help:
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help