import dash
import pandas as pd
from dash import dash, html, dash_table, Input, Output
from sqlalchemy import create_engine

engine = create_engine('postgresql://aleksei:1905@localhost:5433/countries')

countries = pd.read_sql('SELECT * FROM countries', con=engine)

app = dash.Dash()

app.layout = html.Div([
    html.H2('Countries Table'),

    html.Div([
        dash_table.DataTable(
            id='countries_table',
            data=countries.to_dict(orient='records'),
            columns=[{'name': i, 'id': i} for i in countries.columns],
            row_selectable='single',
            selected_rows=[0],
            page_size=20,
            sort_action='native',
            style_table={'overflowX': 'auto', 'overflowY': 'auto', 'height': '400px'},
            style_cell={'textAlign': 'center', 'fontFamily': 'Times New Roman', 'whiteSpace': 'normal'},
        )
    ], style={'width': '85%', 'height': '400px'}),

    html.Div([
        html.H3('Flag of selected country:'),
        html.Img(id='flag_png'),
    ], style={'width': '85%', 'textAlign': 'center', 'marginTop': '20px'}),
])

@app.callback(
    Output('flag_png', 'src'),
    Input('countries_table', 'selected_rows')
)


def update_flag(selected_rows):
    if selected_rows:
        selected_index = selected_rows[0]
        return countries.iloc[selected_index]['flag_png']
    return None

if __name__ == '__main__':
    app.run(debug=True)
