# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

colors = {
    'background': '#172D13',
    'text': '#ffffff'
}

app = Dash(__name__,
           external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# labInfo = pd.read_csv(r'/Users/gnickles/Desktop/UWMadison-FungalSupergroup/LabInfo_Sheet_Updated2023_Programs.csv', sep=',')
# fig = px.sunburst(
#         labInfo, path=["Category", 'Group Leader Name'],
#         values='NumberStudents',
#         color="Category"
#         )

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
            }),
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
    ),
    
])

@app.callback(
    Output("UW-Madison Fungal Supergroup Faculty", "figure"), 
    Input("fileSource", "value"), # this postion is important relative to the slider, it defines which variable is called in the update function
    )

def update_hovermode(fileSource):
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
    # fig.update_layout(
    #     margin=dict(l=20, r=20, t=20, b=20)
    #     )
    # fig.update_layout(width=int(width), height=int(width))

    return fig

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})


if __name__ == '__main__':
    app.run(debug=True)