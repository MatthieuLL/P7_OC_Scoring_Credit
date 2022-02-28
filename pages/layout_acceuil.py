from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

######################## START Log action sur site ########################
LOGO = "https://i2.wp.com/ledatascientist.com/wp-content/uploads/2019/01/31934826_632207023790117_7976915477504983040_o.png?fit=1638%2C1638&ssl=1"
html.Img(src=LOGO, height="40px")



body = dbc.Container([
        html.Br(),
        dbc.Row(
                [
                dbc.Col(

                    html.Div(
                        [   html.Br([]),
                            html.H5("Bienvenue!",style={'color':'red','backgroundColor':'white'}),
                            html.Br([]),
                            html.P(
                                "\
                            Vous êtes sur la page d'acceuil du dashbord de Scoring Credit. \
                            Je vous présente ici les données de 'Prêt à depenser'",

                                style={"color": "#000406"},

                            ),
                            html.P(
                                "\
                            Ces données ont par la suite été transformées pour interagir dynamiquement avec des graphiques.",


                                style={"color": "#000406"},

                            ),
                            dbc.Row(
                                [
                                    #Navlink dashbord
                                    dbc.NavLink("Accès Dashbsoard", href="/dashboard",style={'color':'blue'})
                                ])
                            ]
                        )
                ,style={'color':'red','backgroundColor':'white'})
                    ], justify="center", align="center"
                ),
     html.Br(),
],style={"height": "100vh"}
)

layout_acceuil =  html.Div(
    [body],
    style = {
        'background-image': 'url("/assets/bank.jpg")',
        'background-repeat': 'no-repeat',
        'background-size': 'cover',
    }
)
# layout_acceuil=html.Div ([
# ])