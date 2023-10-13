# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
from dash import html, dcc, dash_table
import plotly.express as px
import pandas as pd
import pdb

# external CSS stylesheets and colors dictionary
colors = {
    'background': '#172D13',
    'text': '#ffffff'
}

app = dash.Dash(__name__)

path = ["Category", 'Group Leader Name']

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    #The top banner
    html.H1(children='Mycology Labs at UW-Madison', 
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'backgroundColor': '#D76F30',
                'margin': '10px auto',
                'width': '80%',
                'height': '100%',
                'display': 'flex',
                'flex-direction': 'column',
                'justify-content': 'center'
            }),
    #The subtitle
    html.H4(children='Click on the options to change the filtering criteria',
        style={
                'textAlign': 'center',
                'color': '#ffffff'
        }
    ),
        #The button toggels for department vs graduate program
    dcc.RadioItems(
        id='fileSource',
        inline=True,
        value='Graduate Program',
        style={
            'textAlign': 'center',
            'color': colors['text']
        },
        options=[
            {
                'label': html.H4('Graduate Program', style={'color': 'White'}),
                'value': 'Graduate Program'
            },
            {
                'label': html.H4('Department', style={'color': 'White'}),
                'value': 'Department'
            }
        ]
    ),
    #The sunburst plot
    dcc.Graph(
        id='UW-Madison Fungal Supergroup Faculty'
    )
    # #The table
    # dash_table.DataTable(id='table')
])

@app.callback(
    Output("UW-Madison Fungal Supergroup Faculty", "figure"),
    Input("fileSource", "value")
)
def update_figure_and_table(fileSource):
    ####
    # Making the sunbirst plot
    ####
    if fileSource == 'Graduate Program':
        labInfo = pd.read_csv(r'/Users/gnickles/Desktop/UWMadison-FungalSupergroup/LabInfo_Sheet_Updated2023_Programs.csv', sep=',')
    elif fileSource == 'Department':
        labInfo = pd.read_csv(r'/Users/gnickles/Desktop/UWMadison-FungalSupergroup/LabInfo_Sheet_Updated2023_Departments.csv', sep=',')
    fig = px.sunburst(
        labInfo, 
        path=["Category", 'Group Leader Name'],
        values='NumberStudents',
        color="Category"
        )
    fig.update_layout(
        autosize=False,
        minreducedwidth=500,
        minreducedheight=500,
        width=1000,
        height=1000,
        )
    
    return fig

@app.callback(
    Output('datatable','data'),
    Input("sunbirst", "value"),
    prevent_initial_call=True
)
def update_table(sunbirst):
    
    
#     pdb.set_trace() #FOR DEBUGGING LATER
#     ####
#     # Making the updated table based on what the user clicks on
#     ####
    
#     click_path = "ALL"
#     root = False

#     if clickData:
#         pdb.set_trace() #FOR DEBUGGING LATER

#     data = labInfo.to_dict('rows')
#     columns =  [{"name": i, "id": i,} for i in (labInfo.columns)]

#     return fig, html.Div([
#         dt.DataTable(data=data, columns=columns)
#     ])


if __name__ == "__main__":
    app.run_server(debug=True)