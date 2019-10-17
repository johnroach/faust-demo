import faust


class PageView(faust.Record, serializer="json"):
    """ Example record. The record is used for 
    JSON dictionaries and describes fields much 
    like the new dataclasses in Python 3.7. Type 
    annotations are used not only for defining static types,
    but also to define how fields are deserialized, 
    and lets you specify models that contains other 
    models, and so on. 
    https://faust.readthedocs.io/en/latest/userguide/models.html#guide-models
    """

    value: int
