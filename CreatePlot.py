import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff

### Incorporate data
labInfo = pd.read_csv(r'/Users/gnickles/Desktop/UWMadison-FungalSupergroup/LabInfo_Sheet_Updated2023_Programs.csv', sep=',')

### Build app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H4('Mycology Graduate Programs at UW-Madison'),
    html.P("Select filtering criteria:"),
    dcc.RadioItems(
        id='Path',
        inline=True,
        options=[
            {'label': 'Grad programs', 'value': 'LabInfo_Sheet_Updated2023_Programs.csv'},
            {'label': 'Departments', 'value': 'LabInfo_Sheet_Updated2023_Departments.csv'},
        ],
        value='LabInfo_Sheet_Updated2023_Programs.csv'
    ),
    dcc.Graph(id="graph"),
    dcc.Graph(id='table', figure=table)
])

# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })

@app.callback(
    Output("graph", "figure"), 
    Input("Path", "value"))
def update_order(path):
    labInfo = labInfo.read_csv(path, sep=',')
    print(labInfo.head())
    fig = ff.create_table(labInfo)
    fig.addtrace(px.sunburst((labInfo, 
                              path=["Category", 'Group Leader Name'], 
                              values='NumberStudents', 
                              color=path, 
                              title="Click on the legend items to switch path!")
                              ))
    # fig = px.sunburst(
    #     labInfo, path=["Category", 'Group Leader Name'],
    #     values='NumberStudents',
    #     color=path,
    #     title="Click on the legend items to switch path!")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, serve_locally=False)