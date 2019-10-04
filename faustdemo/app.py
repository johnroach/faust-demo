import os
import faust

from simple_settings import settings
from logging.config import dictConfig


app = faust.App(
    version=1,  # fmt: off
    autodiscover=True,
    origin="faustdemo",
    id="1",
    broker=settings.KAFKA_BROKER,
    store=settings.STORE_URI,
    logging_config=dictConfig(settings.LOGGING),
)


def main() -> None:
    app.main()