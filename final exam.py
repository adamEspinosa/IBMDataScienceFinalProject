# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#creates dropdown options for place

dropdown_options= [
             {'label': 'All Sites', 'value': 'ALL'}
         ]
unique_place = spacex_df['Launch Site'].unique()

unique_place=dict(enumerate(unique_place))

for key in unique_place:
    my_dict = {'label':unique_place[key],'value': unique_place[key]}
    dropdown_options.append( my_dict )

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=dropdown_options,
                                placeholder='Select a Launch Site here',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={ 0: '0',
                                            100: '100'},
                                    value=[min_payload, max_payload]
                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        fig = px.pie(filtered_df, values='class', 
            names='Launch Site', 
            title='Total Success Launches by site'
            ) 
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site ]
        frecuency = filtered_df['class'].value_counts().reset_index()
        frecuency.columns = ['Class', 'tot']
        fig = px.pie(frecuency, values='tot', 
            names='Class', 
            title='Total Success Launches by {}'.format(entered_site)
            ) 
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site, entered_mass) :
    if entered_site == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0])
        &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        fig = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        filtered_data = filtered_df[(filtered_df['Payload Mass (kg)']>=entered_mass[0])
        &(spacex_df['Payload Mass (kg)']<=entered_mass[1])]
        fig = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class", 
        color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
