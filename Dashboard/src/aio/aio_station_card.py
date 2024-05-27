from dash import html, clientside_callback, Input, Output, MATCH
import dash_bootstrap_components as dbc
import datetime as dt
import numpy as np
import pandas as pd
from typing import Tuple
import uuid
from utils.review_util import get_station_image

class StationCardAIO(html.Div):

    class ids:
        close_btn = lambda aio_id: {
            'component': 'StationCardAIO',
            'subcomponent': 'close_btn',
            'aio_id': aio_id
        }

        card = lambda aio_id: {
            'component': 'StationCardAIO',
            'subcomponent': 'card',
            'aio_id': aio_id
        }

    ids = ids

    def __init__(
        self,
        station_df: pd.DataFrame,
        aio_id = None
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())

        self.df = station_df
        super().__init__(self.build_layout(aio_id))

    def build_layout(self, aio_id: str):
        scrape_time, latest_prices = self.get_latest_pricing()
        mean_pos, mean_low_price = self.get_mean_card_pos()
        station_street = self.df['StationAddress'].iloc[0].split('|')[0].strip()

        time_note = scrape_time.strftime('%m/%d/%Y %H:%M')
        prices_note_style = {'fontWeight':'bold'}
        if(scrape_time.date() != dt.date.today()):
            prices_note_style['color'] = 'red'
            delta = (dt.date.today() - scrape_time.date()).days
            time_note += f" ({delta} days ago)"

        return dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3(station_street),
                            html.Img(src='./assets/images/closeTile.svg', style={'marginLeft':'auto'}, id=self.ids.close_btn(aio_id))
                        ], className='col-12 d-flex')
                    ], className='row'),
                    html.Div([
                        html.Div([
                            html.Img(src=get_station_image(station_street), style={'width':'100%', 'borderRadius':'10px'})
                        ], className='col-12')
                    ], className='row'),
                    html.Div([
                        html.Div([
                            html.Span(f'Prices as of {time_note}', style=prices_note_style)
                        ], className='col-12')
                    ], className='row mt-1'),
                    html.Div([
                        html.Div([
                            html.Span(f"◼️ Regular: {self.cond_price(latest_prices['regular'])}")
                        ], className='col-4'),
                        html.Div([
                            html.Span(f"◼️ Premium: {self.cond_price(latest_prices['premium'])}")
                        ], className='col-4'),
                        html.Div([
                            html.Span(f"◼️ Diesel: {self.cond_price(latest_prices['diesel'])}")
                        ], className='col-4'),
                    ], className='row mt-1'),
                    html.Div([
                        html.Div([
                            html.Span('Average Station Position', style={'fontWeight':'bold'})
                        ], className='col-12')
                    ], className='row mt-1'),
                    html.Div([
                        html.Div([
                            html.Span(f"◼️ Regular: {self.cond_station_pos(mean_pos['regular'])}")
                        ], className='col-4'),
                        html.Div([
                            html.Span(f"◼️ Premium: {self.cond_station_pos(mean_pos['premium'])}")
                        ], className='col-4'),
                        html.Div([
                            html.Span(f"◼️ Diesel: {self.cond_station_pos(mean_pos['diesel'])}")
                        ], className='col-4')
                    ], className='row mt-1'),
                    html.Div([
                        html.Div([
                            html.Span('Average Low Price Delta', style={'fontWeight':'bold'})
                        ], className='col-12')
                    ], className='row mt-1'),
                    html.Div([
                        html.Div([
                            html.Span(f"◼️ Regular: {self.cond_price(mean_low_price['regular'])}")
                        ], className='col-4'),
                        html.Div([
                            html.Span(f"◼️ Premium: {self.cond_price(mean_low_price['premium'])}")
                        ], className='col-4'),
                        html.Div([
                            html.Span(f"◼️ Diesel: {self.cond_price(mean_low_price['diesel'])}")
                        ], className='col-4')
                    ], className='row mt-1')
                ], className='container-fluid')
            ]), id=self.ids.card(aio_id)
        )

    @property
    def fuel_types(self):
        return ['regular', 'premium', 'diesel']

    def get_latest_pricing(self) -> tuple:
        df_max = self.df[self.df['ScrapeTime'] == self.df['ScrapeTime'].max()].copy()
        scrape_time = df_max['ScrapeTime'].iloc[0].to_pydatetime()
        fuel_prices = {}
        for f_type in self.fuel_types:
            dff = df_max[df_max['FuelType'] == f_type]
            fuel_prices[f_type] = None if dff.shape[0] == 0 else dff['CondPrice'].iloc[0]
        return (scrape_time, fuel_prices)

    def get_mean_card_pos(self) -> Tuple[dict, dict]:
        mean_pos = {}
        mean_low_price_delta = {}
        for f_type in self.fuel_types:
            dff = self.df[self.df['FuelType'] == f_type].copy()
            mean_pos[f_type] = dff['CondCardPos'].mean() + 1 #Convert from 0 to 1 indexed.
            mean_low_price_delta[f_type] = dff['PriceDelta'].mean()
        return mean_pos, mean_low_price_delta

    def cond_price(self, price: float) -> str:
        if price is None or price is np.nan:
            return 'N/A'
        return f"${price:.2f}"

    def cond_station_pos(self, pos: float) -> str:
        if pos > 0:
            return f"{pos:.1f}"
        return 'N/A'

    clientside_callback(
        """function(clicks){
                return "d-none";
            }""",
            Output(ids.card(MATCH), 'className'),
            Input(ids.close_btn(MATCH), 'n_clicks'),
            prevent_initial_call=True
    )