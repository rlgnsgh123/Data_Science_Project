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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
print(spacex_df.columns)
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                               
                                html.Div([
                                    dcc.Dropdown(id='site_dropdown',
                                        options=[
                                            {'label': 'All Sites', 'value': 'All Sites'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                            ],
                                        value='All Sites',
                                        placeholder="Select Launch Site!!",
                                        searchable=True
                                        ),]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (kg):"),
                               
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id = 'payload_slider',
                                    min = 0,
                                    max = 10000,
                                    step = 1000,
                                    marks = {
                                            0: {'label': '0 kg'},
                                            1000: {'label': '1000 kg'},
                                            2000: {'label': '2000 kg'},
                                            3000: {'label': '3000 kg'},
                                            4000: {'label': '4000 kg'},
                                            5000: {'label': '5000 kg'},
                                            6000: {'label': '6000 kg'},
                                            7000: {'label': '7000 kg'},
                                            8000: {'label': '8000 kg'},
                                            9000: {'label': '9000 kg'},
                                            10000: {'label': '10000 kg'},
                                            },
                                    value = [min_payload,max_payload]
                                ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for site-dropdown as input, success-pie-chart as output

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site_dropdown', 'value')
)
def update_chart(site_dropdown):
    if site_dropdown == 'All Sites':
        fig = px.pie(
            spacex_df, 
            values='class',
            names='Launch Site',
            title='Total Success Launches by All Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f"Success and Failure for {site_dropdown}"
        )
    return fig


# TASK 4:
# Add a callback function for site-dropdown and payload-slider as inputs, success-payload-scatter-chart as output

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site_dropdown', 'value'), 
     Input('payload_slider', 'value')]
)
def update_scatter_chart(site_dropdown, payload_slider):

    if site_dropdown == 'All Sites':
        low, high = payload_slider
        df  = spacex_df
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    else:
        low, high = payload_slider
        df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mask], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
