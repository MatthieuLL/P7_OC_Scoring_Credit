from unicodedata import name
from dash import dcc
from dash import html
import pickle
import pandas as pd
from  components.functions import app_test, create_card

import dash_bootstrap_components as dbc

clf_pipe = pickle.load(open('data/finalized_model.pkl', 'rb'))



##########################################bloc déclaration DropdownItems###################
select_client_item = dcc.Dropdown(
    className='client_select',
    id='id-client',
    options=[{'label': i, 'value': i} for i in app_test.index],
    value=app_test.index[0],
    clearable=False
)

filtre_label = html.H2("Entrez Identifiant Client : ",style={'color':'#ffff'})
filtre_line = dbc.Container([
    dbc.Row([
        dbc.Col(
            filtre_label,
            width=10,
            align='center',   
        ),
    ]),
    dbc.Row([
        dbc.Col(
            select_client_item, 
            width=10,
            align='center'
        )
    ]    
)])

###################################Fin bloc déclaration DropdownItems##################

##########@@###### bloc déclaration Pie graph###########################################
piegraph=dcc.Graph(id='pie_solvability')

################################################# fin bloc déclaration Pigraph###########

################################bloc des cartes###########################
#courleurs des cartes
color_l=['info',"secondary","success","warning","danger"]

card1 = create_card("Age du client", html.Div(id='age_client_select'), color_l[1])
card2 = create_card("Employé depuis", html.Div(id='date_emploi_client_select'),color_l[1])
card3 = create_card("Type Emploi", html.Div(id='type_emploi_client_select'),color_l[1])
card4 = create_card("Taux d'endettement", html.Div(id='debt_ratio_client_select'),color_l[1])
card5 = create_card("Education", html.Div(id='education_type_client_select'),color_l[1])
card6 = create_card("Sexe", html.Div(id='gender_client_select'),color_l[1])

card_top = dbc.Row(
    [
        dbc.Row(
            [
                dbc.Col(
                    id='card1', 
                    children=[card1],
                    width=2
                    ),
                dbc.Col(
                    id='card2',
                    children=[card2],
                    width=2
                ),
                dbc.Col(
                    id='card3', 
                    children=[card3],
                    width=2
                ),
                dbc.Col(
                    id='card4', 
                    children=[card4],
                    width=2
                ),
                dbc.Col(
                    id='card5', 
                    children=[card5],
                    width=2
                ),
                dbc.Col(
                    id='card6', 
                    children=[card6],
                    width=2
                ),
            ]
        )
    ]
)


#########################################Fin déclaration cartes######################################
shap = html.Div(id='shap_explainer')
pie_bis = dcc.Graph(id='pie_solvability')

labels = {
    'EXT_SOURCE_1':'Source externe 1',
    'EXT_SOURCE_2': 'Source externe 2',
    'EXT_SOURCE_3': 'Source externe 3',
    'TERM':'Terme crédit',
    'DAYS_EMPLOYED':"Stabilité de l'emploi",
    'DAYS_BIRTH': 'Age',
    'OWN_CAR_AGE':'Propriétaire de voiture (en années)',
    'CODE_GENDER':'Sexe',
    'ORGANIZATION_TYPE':'Type de société employeur',
    'NAME_EDUCATION_TYPE':"Niveau d'étude",
    'BUREAU_AMT_CREDIT_SUM_DEBT_MEAN':'Moyenne des dettes - Crédit Bureau'
}

drop = dcc.Dropdown(
    className='feat_select',
    id='feature',
    options=[{'label': i, 'value': k} for k, i in labels.items()],
    value='DAYS_BIRTH',
    clearable=False
)



feature_graph = dcc.Graph(id='feat_graph')


radar = dcc.Graph(id='radar_graph')

#déclaration footer#####@@@@@#################
footer = dbc.Row(
            dbc.Col(
                html.P(
                    [
                        html.Span('Auteur : Louisy-Louis Matthieu', className='mr-2',style={'color':'#ffff'}),
                        html.A(html.I(className='fab fa-github-square mr-1'), href='https://github.com/'),
                        html.A(html.I(className='fab fa-linkedin mr-1'), href='https://www.linkedin.com/'),
                    ],
                className='lead'
                )
            ,lg=12
            )
        )


#déclaration layout final
layout_dashboard  = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        filtre_line,
                    ]
                ),
                html.Br(),
                html.Br(),
                html.Div(
                    [
                        html.Div(
                            [
                                card_top,
                            ]
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        pie_bis,
                                    ],
                                    className="box",
                                    style={"padding-bottom": "15px"}
                                ),
                                html.Div(
                                    [
                                        shap,
                                    ]
                                ),
                            ],                            
                        )    
                    ]
                ),
                html.Br(),                
                html.Br(),
                dbc.Row(
                    [
                        html.Div(
                            [
                                html.H2("Graphiques des principales features influant sur le score de prédiction", style={'color':'#FFE436'}),
                                html.Div(
                                    [
                                        drop,
                                    ]
                                ),
                                html.Div(id='output_drop')
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [ 
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        feature_graph,
                                    ]
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        radar,
                                    ]
                                ),
                            ],align='center'
                        ),
                    ]
                ),
                html.Br(),
                footer
            ],
            style={"background-color":'#323130',"height": "100vh"}
        )
    ]
)    