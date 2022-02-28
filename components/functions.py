import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import pickle
from functions import category
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import shap

#Import des données
clf = pickle.load(open('data/finalized_model.pkl', 'rb'))
app_test = pd.read_csv("data/test_clean.csv")
data_graph = pd.read_csv("data/features_data.csv")
app_test = category(app_test)

#fonction de mise à  jour de la table


######################## Fonction de mise à jour du graph (line et bar)  ########################


def update_feat_graph(id_client, feature):

    num_feat=['EXT_SOURCE_1','EXT_SOURCE_2','EXT_SOURCE_3','TERM','DAYS_EMPLOYED','DAYS_BIRTH','OWN_CAR_AGE','BUREAU_AMT_CREDIT_SUM_DEBT_MEAN']
    dict_graph={}
    fig = make_subplots()
    y1 = data_graph[data_graph['TARGET'] == 1][feature]
    y0 = data_graph[data_graph['TARGET'] == 0][feature]
    
    if feature in num_feat:

        dict_graph['1']=go.Box(
            y=y1, 
            name='Non Solvable',
            marker_color = 'indianred'
            )
        dict_graph['0']=go.Box(
            y=y0,
            name = 'Solvable',
            marker_color = 'lightseagreen',
            )

        for key, value in dict_graph.items():
            fig.add_traces(value)
            fig.add_hline(
                y=data_graph.iloc[id_client][feature],
                annotation_text='Client sélectionné',
                line_color='#FFE436',
            )    
    else :
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=y0, marker = {'color':'lightseagreen'}))
        fig.add_trace(go.Histogram(x=y1, marker = {'color':'indianred'}))
        fig.update_layout(
            barmode="overlay",
            bargap=0.1
        )

    fig['layout'].update(
                plot_bgcolor = '#323130',
                paper_bgcolor="#323130",
                font_color = "#323130",
                font=dict(color="white"),
            )
    return fig



def update_output_drop(id_client, feature):
    return app_test[feature].iloc[id_client]

######################## Fonction de mise à jour du graph pie  ########################
def update_pie(id_client):

    layout = go.Layout(
        title=dict(text='Prediction du modèle', x=0.5),
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        font=dict(color="white"),
        annotations=[dict(text='THR = Seuil de non-solvabilité', x=0, y=0, font_size=20, showarrow=False)]
    )
    values = clf.predict_proba(app_test.drop(columns='SK_ID_CURR'))[id_client]   
    # Retourne le pie plot mis à jour pour l'id client
    return go.Figure(
        data=[
            go.Pie(
                title=dict(text='THR 20%',font=dict(color='#FFE436', size=26)),
                labels=['Solvable', "Non Solvable"],
                values=values,
                marker_colors=["#2ecc71", "#e74c3c"],
                hole=.5
            )
        ],
    layout=layout,
)
######################## Fin de mise à jour du graph pie  ########################


######################## Fonction de création des cartes########################
def create_card(title, content, color):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H5(title, className="card-title"),
                html.Br(),
                html.H3(content, className="card-subtitle"),
                html.Br(),

                ]
        ),
        color=color, inverse=True
    )
    return(card)

def age_client(id_client):
    return round(app_test['DAYS_BIRTH'].iloc[id_client],2)

def date_emploi_client(id_client):
    return round(app_test['DAYS_EMPLOYED'].iloc[id_client],2)

def type_emploi_client(id_client):
    return app_test['ORGANIZATION_TYPE'].iloc[id_client]

def debt_ratio_client(id_client):
    return round(app_test['DEBT_RATIO'].iloc[id_client],2)

def education_type_client(id_client):
    return app_test['NAME_EDUCATION_TYPE'].iloc[id_client]

def gender_client(id_client):
    return app_test['CODE_GENDER'].iloc[id_client]

######################## Fin de fonctions de création des cartes########################

def _force_plot_html(id_client):
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(app_test.drop(columns=['SK_ID_CURR']))
    shap_graph = shap.force_plot(explainer.expected_value[1], shap_values[1][id_client,:], app_test.drop(columns=['SK_ID_CURR']).iloc[id_client,:], matplotlib=False)
    shap_html = f"<head>{shap.getjs()}</head><body>{shap_graph.html()}</body>"
    return html.Iframe(srcDoc=shap_html,
                       style={"width": "100%", "height": "200px", "border": 0})
                       
def update_radar(id_client):

 
    categories = ['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 'DEBT_RATIO']


    fig = go.Figure(
    data=[
        go.Scatterpolar(theta=categories, name='Client Sélectionné', line=dict(color='#FFE436'), connectgaps=True),
    ],
    layout=go.Layout(
        title=go.layout.Title(text='Client Comparaison'),
        polar={'radialaxis': {'visible': True}},
        showlegend=True
        )
    )
    fig['layout'].update(
        plot_bgcolor = '#323130',
        paper_bgcolor="#323130",
        font_color = "#323130",
        font=dict(color="white"),
    )

    return fig