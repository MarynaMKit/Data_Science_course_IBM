import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt
import pandas as pd

#Create app
app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the wildfire data into pandas dataframe
spacex_df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')


app.layout = html.Div(children=[html.H1(html.H1('SpaceX Launch Record Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26})),
                                html.Div([
                                    html.Div([
                                            dcc.Dropdown(id='site-dropdown',
                                                            options=[
                                                                {'label': 'All Sites', 'value': 'ALL'},
                                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},                                                            
                                                                    ],
                                                            value='ALL',
                                                            placeholder="choose Launch Site",
                                                            searchable=True
                                                            ),
                                        ]),
                                    html.Div([
                                       html.Div(dcc.Graph(id='success-pie-chart'))
                                    ])  
                                ]),
                                html.Div([
                                        dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0',
                                              1000: '1000',
                                              2000: '2000',
                                              3000: '3000',
                                              4000: '4000',
                                              5000: '5000',
                                              6000: '6000',
                                              7000: '7000',
                                              8000: '8000',
                                              9000: '9000',
                                              10000: '10000'},
                                        value=[0, 10000])
                                    ]),
                                    html.Div([
                                       html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                    ])  
                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        sucsess_lunches = spacex_df[spacex_df['class']==1]
        fig = px.pie(values=sucsess_lunches['class'], names=sucsess_lunches['Launch Site'], title='Total success launches by site')
    else:
        filtered_by_site = spacex_df[spacex_df['Launch Site']==entered_site]
        sucsess_by_site = filtered_by_site.groupby(['class'])['class'].count()
        fig = px.pie(values=sucsess_by_site, names=[0,1], title=f'Total success launches for site {entered_site}')

    return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, slider_value):
    df_by_mass = spacex_df[(spacex_df['Payload Mass (kg)']<=slider_value[1])&(spacex_df['Payload Mass (kg)']>=slider_value[0])]
    if entered_site == 'ALL':
        fig = px.scatter(df_by_mass, 
                        x='Payload Mass (kg)', 
                        y='class', 
                        color='Booster Version Category', 
                        title=f'Correlation between Payload and Success for all Sites for Payload mass {slider_value[0]} to {slider_value[1]} kg',
                        )
    else:
        sorted_by_mass_by_site = df_by_mass[df_by_mass['Launch Site']==entered_site]
        fig = px.scatter(sorted_by_mass_by_site, 
                x='Payload Mass (kg)', 
                y='class', 
                color='Booster Version Category', 
                title=f'Correlation between Payload and Success for site "{entered_site}" for Payload mass {slider_value[0]} to {slider_value[1]} kg',
                )
    return fig

if __name__ == '__main__':
    app.run_server()