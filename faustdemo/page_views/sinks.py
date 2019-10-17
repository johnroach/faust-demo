from faustdemo.app import app
from faustdemo.page_views import tumbling_page_view_table, page_views_topic
from faustdemo.page_views.models import PageView


def report_sink(value):
    """This normally would be where we
    send alerts etc. or if need be update
    metrics to be crawled. However in this demo
    we are simply surfacing this up in `/report/`
    A better defined table wouldn't need a external in memory
    variable to be defined.
    """
    report, page_view_count, pageview_within_table = value
    print(
        "Report: "
        + str(report)
        + ", Number of events in window: "
        + str(pageview_within_table)
        + ", Total page view count: "
        + str(page_view_count)
    )
