from components.functions import update_pie, age_client, date_emploi_client, type_emploi_client, debt_ratio_client, education_type_client, gender_client, update_feat_graph, update_output_drop, update_radar, _force_plot_html
from dash.dependencies import Input, Output
from app import app




# Met à jour le pieplot de la solvabilité du client dont l'id est choisie
@app.callback(
    Output('pie_solvability', 'figure'),
    [Input('id-client', 'value')])
def update_publishing_pie(id_client):
    fig = update_pie(id_client)
    return fig


@app.callback(
   Output('feat_graph', 'figure'),
   [Input('id-client', 'value'),
   Input('feature', 'value')])
def update_feat_graph_client(id_client, feature):
	fig = update_feat_graph(id_client, feature)
	return fig

@app.callback(
    Output('output_drop', 'children'),
   [Input('id-client', 'value'),
   Input('feature', 'value')])
def update_output(id_client, feature):
   client = update_output_drop(id_client, feature)
   return f'Feature: {feature}, Client:{client}'

@app.callback(
   Output('age_client_select', 'children'),
   [Input('id-client', 'value')])
def update_age_client(id_client):
	age = age_client(id_client)
	return f'{age} Ans'

@app.callback(
   Output('date_emploi_client_select', 'children'),
   [Input('id-client', 'value')])
def update_date_emploi_client(id_client):
	date = date_emploi_client(id_client)
	return f'{date} Ans'

@app.callback(
   Output('type_emploi_client_select', 'children'),
   [Input('id-client', 'value')])
def update_date_emploi_client(id_client):
	emploi = type_emploi_client(id_client)
	return emploi

@app.callback(
   Output('debt_ratio_client_select', 'children'),
   [Input('id-client', 'value')])
def update_date_emploi_client(id_client):
	debt = debt_ratio_client(id_client)
	return f'{debt} %'

@app.callback(
   Output('education_type_client_select', 'children'),
   [Input('id-client', 'value')])
def update_education_type_client(id_client):
	edu = education_type_client(id_client)
	return edu

@app.callback(
   Output('gender_client_select', 'children'),
   [Input('id-client', 'value')])
def update_gender_client(id_client):
	gender = gender_client(id_client)
	return gender

@app.callback(
    Output('shap_explainer', 'children'),
    [Input('id-client', 'value')])
def update_shap_client(id_client):
    fig = _force_plot_html(id_client)
    return fig

@app.callback(
    Output('radar_graph', 'figure'),
   [Input('id-client', 'value')])
def update_output(id_client):
   fig = update_radar(id_client)
   return fig