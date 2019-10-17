from faustdemo.app import app
from faustdemo.page_views.models import PageView
from datetime import timedelta

# this sample counter exists in-memory only for this demo
# so will be wiped when the worker restarts.
count = [0]

page_views_topic = app.topic("page_views", value_type=PageView)

# defining a tumbling page_view table that expires in 1 minute
# notes:
#   `key_index=True` is needed for debugging and shouldn't be relied
#    on in production environments. Iterating over all the keys in a
#    table will require you to visit all workers, which is highly
#    impractical in a production system.
tumbling_page_view_table = app.Table("views", default=int).tumbling(
    timedelta(minutes=1), expires=timedelta(minutes=5)
)
