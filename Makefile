service=faustdemo
worker=faustdemo.app
partitions=1
replication-factor=1

docker-build:
	docker build -t faustdemo .

docker-run:
	docker run faustdemo

native-run:
	FAUST_DATADIR=.data1 SIMPLE_SETTINGS=faustdemo.settings poetry run faustdemo worker --web-port=8088