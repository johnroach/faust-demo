import os
import faust
from faust import web
from simple_settings import settings
from logging.config import dictConfig
from faust.types.enums import ProcessingGuarantee

# readyness should probably be handled better but it is 2AM
# and want to sleep
ready = [0]

app = faust.App(
    version=1,  # fmt: off
    autodiscover=True,
    origin="faustdemo",
    id="1",
    broker=settings.KAFKA_BROKER,
    store=settings.STORE_URI,
    logging_config=dictConfig(settings.LOGGING),
    topic_partitions=settings.TOPIC_PARTITIONS,
    processing_guarantee=ProcessingGuarantee.EXACTLY_ONCE,
    web_in_thread=True,
)


@app.task
async def startup(app):
    ready[0] = 1
    print("FAUST IS NOW READY!!")


@app.page("/ready/")
async def get_ready(self, request):
    if ready[0] != 1:
        return self.json({"status": "NOT-READY"}, status=503)
    else:
        return self.json({"status": "OK"})


def main() -> None:
    app.main()
