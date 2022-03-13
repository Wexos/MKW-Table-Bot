from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import api.api_channelbot_interface as cb_interface
from api import api_data_builder
from api.api_common import *

app = None


def initialize(app_: FastAPI):
    global app
    app = app_
    app.mount("/css", StaticFiles(directory="./api/css"))


    @app.get(TEAM_SCORES_HTML_ENDPOINT + "{table_id}", response_class=HTMLResponse)
    def get_team_scores_html(
        table_id: int,
        style: Optional[str] = Query(None, max_length=15),
        background_picture: Optional[str] = Query(None),
        background_color: Optional[str] = Query(None),
        text_color: Optional[str] = Query(None),
        font: Optional[str] = Query(None),
        border_color: Optional[str] = Query(None)
    ):
        table_bot = cb_interface.get_table_bot(table_id)
        if table_bot is None:
            raise HTTPException(
                status_code=404,
                detail="Table ID not found. Either the table has been reset, or the table ID given does not exist. Table Bot gave you a table ID when you started the table. Use that.",
            )
        return api_data_builder.build_team_html(
            cb_interface.get_team_score_data(table_bot), style, background_picture, background_color, text_color, font, border_color
        )

    @app.get(FULL_TABLE_HTML_ENDPOINT + "{table_id}", response_class=HTMLResponse)
    def get_full_table_html(
        table_id: int,
        style: Optional[str] = Query(None, max_length=15),
        background_picture: Optional[str] = Query(None),
        background_color: Optional[str] = Query(None),
        text_color: Optional[str] = Query(None),
        font: Optional[str] = Query(None),
        border_color: Optional[str] = Query(None)
    ):
        table_bot = cb_interface.get_table_bot(table_id)
        if table_bot is None:
            raise HTTPException(
                status_code=404,
                detail="Table ID not found. Either the table has been reset, or the table ID given does not exist. Table Bot gave you a table ID when you started the table. Use that.",
            )
        return api_data_builder.build_full_table_html(
            cb_interface.get_team_score_data(table_bot), style, background_picture, background_color, text_color, font, border_color
        )

    @app.get(TEAM_SCORES_JSON_ENDPOINT + "{table_id}")
    def get_team_scores_json(table_id: int):
        table_bot = cb_interface.get_table_bot(table_id)
        if table_bot is None:
            raise HTTPException(
                status_code=404,
                detail="Table ID not found. Either the table has been reset, or the table ID given does not exist. Table Bot gave you a table ID when you started the table. Use that.",
            )
        return cb_interface.get_team_score_data(table_bot)

    @app.get(INFO_ENDPOINT + "{table_id}", response_class=HTMLResponse)
    def info_page(table_id: int):
        return api_data_builder.build_info_page_html(table_id)