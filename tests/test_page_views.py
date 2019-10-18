import pytest
import os
from faustdemo.app import app
from faustdemo.page_views import tumbling_page_view_table
from faustdemo.page_views.models import PageView
from faustdemo.page_views.agents import aggregate_page_views


@pytest.fixture()
def test_app(event_loop):
    """passing in event_loop helps avoid 'attached to a different loop' error"""
    
    app.finalize()
    app.conf.store = 'memory://'
    app.flow_control.resume()
    return app


@pytest.mark.asyncio()
async def test_aggregate_page_views(test_app):
    async with aggregate_page_views.test_context() as agent:
        page_view = PageView(value='1')
        page_view_2 = PageView(value='2')
        event = await agent.put(page_view)

        # windowed table: we select window relative to the current event
        assert tumbling_page_view_table["count"].now() == '1'
        assert tumbling_page_view_table["event_counter"].now() == 1
