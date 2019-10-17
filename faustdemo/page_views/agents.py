from faustdemo.app import app
from faustdemo.page_views import tumbling_page_view_table, page_views_topic
from faustdemo.page_views.sinks import report_sink
from faustdemo.page_views.models import PageView
from datetime import timedelta


@app.agent(page_views_topic, sink=[report_sink])
async def aggregate_page_views(stream, concurrency=1):
    """Aggregates pages views of `/count/` within defined
    time window of 5 minutes and checks past, present and
    current window state.
        “A man sees in the world what he carries in his heart.”
        – Goethe, Faust: First part
    Args:
        stream: A stream is an infinite async iterable, consuming
        messages from a channel/topic.
            > “Everything transitory is but an image.”
            – Goethe, Faust: Part II

        concurrency: Concurrent instances of an agent will process
        the stream out-of-order, so you cannot mutate tables from
        within the agent function:
            An agent having concurrency > 1, can only read from a 
            table, never write.
    """
    async for _, value in stream.items():  # noqa
        # let us keep count of number of events for this table
        tumbling_page_view_table["event_counter"] += 1
        pageview_within_table = tumbling_page_view_table["event_counter"]

        # let us keep count of current total count in general for this table
        tumbling_page_view_table["count"] = value.value
        page_view_count = tumbling_page_view_table["count"]

        report = "Not enough data"
        if pageview_within_table.now() >= 5:
            # Page is trending for current processing time window
            report = "Trending now"

        if pageview_within_table.current() >= 5:
            # Page would be trending in the current event's time window
            report = "Trending when event happened"

        if pageview_within_table.value() >= 5:
            # Page would be trending in the current event's time window
            # according to the relative time set when creating the
            # table.
            report = "Trending when event happened"

        if (
            pageview_within_table.delta(timedelta(minutes=2))
            > pageview_within_table.now()
        ):
            report = "Less popular compared to 2 minutes back"
        yield report, page_view_count.now(), pageview_within_table.now()
