import dash
import dash_bootstrap_components as dbc
from dash import html

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
OC_LOGO = "https://www.anaf.fr/wp-content/uploads/2020/09/OpenClassroom_LOGO-768x92.png"

navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px"), align='center'),
                        dbc.Col(dbc.NavLink("Acceuil", href="/acceuil",style={'color':'white'}), align='center', width=6, lg=3),
                        dbc.Col(dbc.NavLink("Dashbsoard", href="/dashboard",style={'color':'white'}), align='center', width=10, lg=3),
                        dbc.Col(html.Img(src=OC_LOGO, height="30px"), align='center', width=6, lg=3),
                    ],
                    justify="center",                 
                ),
                href="https://www.openclassrooms.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ],
    color="dark",
    dark=True,
)

navbar_bis = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.NavLink("Acceuil", href="/acceuil",style={'color':'white'}),
            dbc.NavLink("Dashbsoard", href="/dashboard",style={'color':'white'}),
            dbc.Col(html.Img(src=OC_LOGO, height="30px")),
        ]
    ),
    color="dark",
    dark=True,
)
