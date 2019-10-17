SIMPLE_SETTINGS = {
    "OVERRIDE_BY_ENV": True,
    "CONFIGURE_LOGGING": True,
    "REQUIRED_SETTINGS": ("KAFKA_BROKER",),
}

# You can override the following variables via ENV

KAFKA_BROKER = "kafka://kafka:9092"

# SCHEMA_REGISTRY_URL = "http://schema-registry:8081"

# Production should use rocksdb:// and not memory
# Tilt environment should be using rocksdb and
# relevant kubernetes deployment should be using statefulset
STORE_URI = "memory://"

# TOPIC_PARTITIONS setting defines the maximum number of workers we can distribute
# the workload to (also sometimes referred as the “sharding factor”).
# In this example, we set this to 1, but in a production app, we ideally use a higher number.
TOPIC_PARTITIONS = 1

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {"faustdemo": {"handlers": ["console"], "level": "INFO"}},
}
