# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, dash_table, ctx, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import warnings

### Global variables ###
currentTable = "" #global variable to keep track of the current table
labInfo_programs = pd.read_csv(r'./LabInfo_Sheet_Updated2023_Programs.csv', sep=',')
labInfo_departments = pd.read_csv(r'./LabInfo_Sheet_Updated2023_Departments.csv', sep=',')
websites = pd.read_csv(r'./LabWebsites.csv', sep=',')

# external CSS stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#172D13',
    'text': '#ffffff'
}

app = Dash(__name__)
server = app.server

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    #The top banner
    html.H1(children='Mycology Labs at UW-Madison and Madison National Labs', 
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
    #The subtitles
    html.H4(children='''Interested in studying mycology at UW-Madison? You've come to the right place! ''',
        style={
                'textAlign': 'center',
                'color': '#ffffff'
            }),
    html.Div(children='The below data contains information on every mycology research group on campus. You can filter the data by graduate program or department. Clicking on the sunburst plot will filter the figure and table to display only the clicked on deparment or program. To step back up a layer, simply click in the center of the pie chart. Supergroup affiliated mycologists who work at nearby national labs can be found under the Department tab.',
            style={
                'textAlign': 'center',
                'color': '#ffffff',
                'font-size': '14px'
            }),
    #The buttons toggels for department vs graduate program
    
    html.Div([
        html.Button('Graduate Program', id='grad',
                    style={'font-size': '16px', 
                        'backgroundColor': '#6BB77B',
                            'margin': '10px auto',
                            'display': 'inline',
                            'font-family': 'Arial',
                            'color': '#ffffff'
                            }, className='button', 
                            ),
        html.Button('Department', id='dept',
                    style={'font-size': '16px', 
                        'backgroundColor': '#6BB77B',
                            'margin': '10px auto', 
                            'margin-left': '20px',
                            'display': 'inline',
                            'font-family': 'Arial',
                            'color': '#ffffff'  
                            }, className='button'
                            )
    ], style={'textAlign': 'center', 'justify-content': 'center'}),
    #The sunburst plot
    html.Div([
        dcc.Graph(
            id='SunburstPlot',
            style={'textAlign': 'center', 'margin': 'auto'}
        )
    ], style={'display': 'flex', 'align-items': 'center'}),
    #The table
    dash_table.DataTable(id='table', 
                        style_table={'width': '80%', 'margin': 'auto'},
                        style_cell={'textAlign': 'left'},
                        style_as_list_view=True,
                        style_header={
                            'backgroundColor': '#303F4B',
                            'fontWeight': 'bold',
                            'font-family': 'Arial',
                            #increase the font size of the header
                            'fontSize': 16,
                            'color': '#ffffff'
                        },
                        style_data={
                            'color': 'black',
                            'backgroundColor': '#7795A6',
                            'font-family': 'Arial',
                            'color': '#ffffff',
                            'width': '20%',
                            'whiteSpace': 'normal',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 0,
                            'fontSize': 12
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#CED8DF',
                                'color': 'black'
                            },
                        ],
                        css=[{
                            'selector': 'a',
                            'rule': 'color: #D76F30;'
                        }],
    ),

    # Store components for storing global state and data
    dcc.Store(id='currentTable', data="grad"),  # initial value
    dcc.Store(id='labInfo_programs', data=labInfo_programs.to_json(date_format='iso', orient='split')),
    dcc.Store(id='labInfo_departments', data=labInfo_departments.to_json(date_format='iso', orient='split'))
])

#the app callback for the sunburst plot
@app.callback(
    Output("SunburstPlot", "figure"), 
    Input("grad", "n_clicks"), 
    Input("dept", "n_clicks")
    )
def returnPlot(gradButton, deptButton):
    global currentTable # Use the global keyword to access the global variable
    #reading in the file based on the current table value
    if gradButton == None and deptButton == None:
        labInfo = labInfo_programs.copy(deep=True)
    else:
        triggered_id = ctx.triggered_id
        if triggered_id == "grad":
            labInfo = labInfo_programs.copy(deep=True)
            currentTable = "grad"
        elif triggered_id == "dept":
            labInfo = labInfo_departments.copy(deep=True)
            currentTable = "dept"
        else: #TODO this is a debugging else and print statment, remove later 
            print(triggered_id)
            
    fig = px.sunburst(
        labInfo, 
        path=["Category", 'Group Leader Name'],
        values='NumberStudents',
        color_discrete_sequence=px.colors.qualitative.Dark2,
    )
    fig.update_traces(hovertemplate='<b>%{label}</b><br>Mycologist Research Leaders: %{value}<extra></extra></b><br>Click mouse to filter the table')
    fig.update_layout(
        autosize=False,
        minreducedwidth=500,
        minreducedheight=500,
        width=1000,
        height=1000,
        plot_bgcolor='#172D13',
        paper_bgcolor='#172D13',
        hoverlabel=dict(
            font_size=16,
            font_family="Arial"
        )
    )
    fig.update_traces(insidetextfont=dict(size=20))
    return fig

#the app callback for the table
@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('SunburstPlot', 'clickData'),
    Input('labInfo_programs', 'data'),
    Input('labInfo_departments', 'data'),
    Input("grad", "n_clicks"), 
    Input("dept", "n_clicks")
)

def update_table(click_data, labinfo_programs, labinfo_departments, gradButton, deptButton):
    global currentTable # Use the global keyword to access the global variable

    # If there's no clickData, or if it's a top-level click
    if ctx.triggered_id == None:
        labInfo = labInfo_programs.copy(deep=True)  
        filtered_df = labInfo
        currentTable = "grad"
    elif ctx.triggered_id == "grad":
        labInfo = labInfo_programs.copy(deep=True)  
        filtered_df = labInfo
        currentTable = "grad"
    elif ctx.triggered_id == "dept":
        labInfo = labInfo_departments.copy(deep=True) 
        filtered_df = labInfo
        currentTable = "dept"
    #else the sunburst plot was clicked
    elif ctx.triggered_id == "SunburstPlot":
        #reading in the file based on the current table value
        if currentTable == "grad":
            labInfo = labInfo_programs.copy(deep=True)  
        elif currentTable == "dept":
            labInfo = labInfo_departments.copy(deep=True)
            
        # if the user clicked on the top level of the sunburst plot
        if click_data['points'][0]['percentEntry'] == 1:
            filtered_df = labInfo
        #otherwise the user clicked on a department or program name and the table should be filtered
        else:
            filterCategory = click_data['points'][0]['id']
            filtered_df = labInfo[labInfo['Category'] == filterCategory]

    filtered_df = CleanTable(filtered_df)
    columns = [
        {"name": "Group Leader Name", "id": "Group Leader Name"},
        {"name": "Email", "id": "Email"},
        {"name": "Website", "id": "Website", "type": "text", "presentation": "markdown"}
    ]
    return filtered_df.to_dict('records'), columns

#subfunction that helps clean up the table
def CleanTable(labInfo):
    global websites # Use the global keyword to access the global variable
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        #removing the NumberStudents and Institutional Affiliation column from the table
        labInfo.drop(columns=['NumberStudents','Institutional Affilitation', 'Category'], inplace=True)
        #keeping only one professor per table
        labInfo.drop_duplicates(subset=['Group Leader Name'], inplace=True)
        #adding in the website information
        labInfo = labInfo.merge(websites, how = 'left', left_on="Group Leader Email", right_on="Email")
        labInfo.drop(columns=['Email','LastName'], inplace=True)
        labInfo.rename(columns={'Group Leader Email': 'Email'}, inplace=True)
        for index, row in labInfo.iterrows():
            labInfo.loc[index, 'Website'] = '[{}]({})'.format(row['Group Leader Name'],row['Website'])

    return labInfo #returning the cleaned table

### Adding in the google tag
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-R7JFW1HZ2R"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-R7JFW1HZ2R');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

if __name__ == '__main__':
    app.run(debug=True)