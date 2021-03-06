
### Variables globales del sistema

import pandas as pd
from dataclasses import dataclass

#Globals dataframes
# @dataclass
# class DFInfo:
#     DF = pd.DataFrame
#     DFF = pd.DataFrame

# DataFrames Collection
DfC = {}

DATE_S = pd.to_datetime("01-01-2021")
DATE_F = pd.to_datetime("01-01-2021")
BASE_TAMPLATE = 'plotly_white'
BASE_LAYOUT = dict(
                xaxis=dict(
                    zeroline=False,
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)'),
                ),
                yaxis=dict(
                    zeroline=False,
                    showline=True,
                    showgrid=True,
                    showticklabels=True,
                    linecolor='rgb(204, 204, 204)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Arial',
                        size=12,
                        color='rgb(82, 82, 82)'),
                ),
                margin=dict(l=10, r=10, b=10, t=30, pad=5),
                template=BASE_TAMPLATE
            )

