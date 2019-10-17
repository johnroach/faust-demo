from faustdemo.page_views import count, page_views_topic, tumbling_page_view_table
from faustdemo.page_views.models import PageView
from faustdemo.app import app
from faust.sensors import Monitor
from faust.web.views import exceptions


@app.page("/count/")
async def get_count(self, request):
    """ Example endpoint that creates a count.
    Args:
        request: HTTP request object
    Returns:
        json formatted count value
    """
    # update the counter
    count[0] = count[0] + 1

    await page_views_topic.send(value=PageView(value=count[0]))

    # and return it.
    return self.json({"count": count[0]})


@app.page("/report/")
async def get_report(self, request):
    """ An example endpoint that presents a report
    of page view count of `/count/`. Normally this
    wouldn't be handled from here but from the sink
    where the report got generated. Or by using route_table
    More info at https://faust.readthedocs.io/en/latest/userguide/tasks.html#exposing-tables
    """
    return self.json(
        {
            "page_views_within_1_minute": tumbling_page_view_table[
                "event_counter"
            ].now(),
            "count": tumbling_page_view_table["count"].now(),
        }
    )
