# app.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from beam import Beam
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1('Beam Stress Visualization', className='text-center my-4'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Input Parameters"),
                dbc.CardBody([
                    dbc.Label('Beam Length (m)'),
                    dbc.Input(id='length-input', type='number', value=10, min=1, step=0.5),
                    html.Br(),
                    dbc.Label('Load (N)'),
                    dbc.Input(id='load-input', type='number', value=500, min=0, step=10),
                    html.Br(),
                    dbc.Label('Load Position (m)'),
                    dbc.Input(id='load-position-input', type='number', value=5, min=0, step=0.5),
                    html.Br(),
                    dbc.Label('Support Type'),
                    dcc.Dropdown(
                        id='support-input',
                        options=[
                            {'label': 'Simply Supported', 'value': 'simply_supported'},
                            {'label': 'Cantilever', 'value': 'cantilever'}
                        ],
                        value='simply_supported'
                    ),
                    html.Br(),
                    dbc.Button(
                        'Update', 
                        id='update-button', 
                        color='primary', 
                        className='w-100'  # Add this line
                    ),

                ])
            ])
        ], width=3),

        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label='Beam Visual', tab_id='beam-tab'),
                dbc.Tab(label='Shear Force', tab_id='shear-tab'),
                dbc.Tab(label='Bending Moment', tab_id='moment-tab'),
                dbc.Tab(label='Deflection', tab_id='deflection-tab'),
            ], id='tabs', active_tab='beam-tab'),

            html.Div(id='tab-content', className='p-4'),
        ], width=9),
    ])
])

@app.callback(
    Output('tab-content', 'children'),
    [Input('update-button', 'n_clicks'),
     Input('tabs', 'active_tab')],
    [State('length-input', 'value'),
     State('load-input', 'value'),
     State('load-position-input', 'value'),
     State('support-input', 'value')]
)
def update_plots(n_clicks, active_tab, length, load, load_position, support):
    if None in [length, load, load_position]:
        return html.Div('Please enter all input values.', className='text-danger')

    if load_position > length or load_position < 0:
        return html.Div('Load position must be within the length of the beam.', className='text-danger')

    beam = Beam(length=length, load=load, load_position=load_position, support=support)

    if active_tab == 'beam-tab':
        beam_fig = beam.plot_beam()
        return dcc.Graph(figure=beam_fig)
    elif active_tab == 'shear-tab':
        shear_fig = beam.plot_shear_force()
        return dcc.Graph(figure=shear_fig)
    elif active_tab == 'moment-tab':
        moment_fig = beam.plot_bending_moment()
        return dcc.Graph(figure=moment_fig)
    elif active_tab == 'deflection-tab':
        deflection_fig = beam.plot_deflection()
        return dcc.Graph(figure=deflection_fig)
    else:
        return html.Div('Invalid tab selected.')

if __name__ == '__main__':
    app.run_server(debug=True)
