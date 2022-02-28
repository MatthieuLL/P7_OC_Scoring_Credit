import dash
from dash import html
from dash import dcc
from dash.dependencies import Input,Output
import plotly.graph_objs as go

import pickle
import pandas as pd
import numpy as np

clf_pipe = pickle.load(open('data/finalized_model.pkl', 'rb'))
app_test = pd.read_csv("data/test_clean.csv")
proba = clf_pipe.predict_proba(app_test)

app = dash.Dash(
    __name__
    )

app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.A(
                            html.Img(
                                className="logo",
                                src=app.get_asset_url("plotly_logo_white.png"),
                            ),
                        ),
                        html.H1("DASHBOARD - Scoring Credit"),
                                                
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        html.H3("Identifiant du Client"),
                                        dcc.Dropdown(
                                            id='id-client',
                                            options=[{'label': i, 'value': i} for i in app_test.index],
                                            value=app_test.index[0]
                                        )
                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        dcc.Markdown(),
                    ],
                ),
                html.Div(
                # Affiche la probabilité de solvabilité d'un client
                # sous forme de pie plot
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        html.H3("Solvabilité du Client "),
                        dcc.Graph(id='pie_solvability'),
                    ]
                ),
            ],
        )
    ]
)
# Met à jour le pieplot de la solvabilité du client dont l'id est choisie
@app.callback(
    Output('pie_solvability', 'figure'),
    [Input('id-client', 'value')])
def proba_pie(id_client):
    layout = go.Layout(
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        font=dict(color="white")
    )
    values = clf_pipe.predict_proba(app_test.drop(columns='SK_ID_CURR'))[id_client]
        
    # Retourne le pie plot mis à jour pour l'id client
    return go.Figure(
        data=[
            go.Pie(
                labels=['Solvable', "Non Solvable"],
                values=values,
                marker_colors=["#2ecc71", "#e74c3c"],
                hole=.5
            )
        ],
    layout=layout,
)

app.run_server(debug=True)
