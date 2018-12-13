import dash
import dash_core_components as dcc
import dash_html_components as html
import sqlite3
from sensor_reader import Mocker, Measurer
from pyA20.gpio import port
from datetime import timedelta

DHT22_PIN = port.PA13


# def retrieve_data(num_of_days):
#     conn = sqlite3.connect('measurement_db.db', detect_types=sqlite3.PARSE_DECLTYPES)
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     cur.execute(f"SELECT measurement_date, temperature, humidity FROM measurements WHERE measurement_date > datetime('now', '-{num_of_days} days')")
#     data = cur.fetchall()
#     conn.close()
#     # df = pandas.read_sql_query(sql=f"SELECT measurement_date, temperature, humidity FROM measurements WHERE measurement_date > datetime('now', '-{num_of_days} days')",
#     #                 con=conn, parse_dates=['measurement_date'])
#     print([type(item['measurement_date']) for item in data])


conn = sqlite3.connect('measurement_db.db')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Mighty thermometer'),

    html.Div(children='''
        Lucinka`s thermometer for easier orientation !
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [],
            'layout': {
                'title': 'Our temperature & humidity'
            }
        },
    ),
    dcc.Slider(
        id='slider',
        min=1,
        max=10,
        value=1,
        marks={str(year): str(year) for year in range(10)}
    )
])


@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('slider', 'value')]
)
def update_graph(num_of_days):
    # conn = sqlite3.connect('measurement_db.db')
    # df = pandas.read_sql_query(sql=f"SELECT measurement_date, temperature, humidity FROM measurements WHERE measurement_date > datetime('now', '-{num_of_days} minutes')",
    #                 con=conn, parse_dates=['measurement_date'])
    # conn.close()

    # timestamps = [item for item in df.measurement_date]
    # temperature = [item for item in df.temperature]
    # humidity = [item for item in df.humidity]

    conn = sqlite3.connect('measurement_db.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT measurement_date, temperature, humidity FROM measurements WHERE measurement_date > datetime('now', '-{num} days')".format(num=num_of_days))
    data = cur.fetchall()
    delta = timedelta(hours=1)
    timestamps = [item['measurement_date'] + delta for item in data]
    temperature = [item['temperature'] for item in data]
    humidity = [item['humidity'] for item in data]
    conn.close()

    return {
            'data': [
                {'x': timestamps, 'y': temperature, 'name': 'temperature'},
                {'x': timestamps, 'y': humidity, 'name': 'humidity'},
            ],
            'layout': {
                'title': 'Our temperature & humidity'
            }
        }


meas = Measurer(DHT22_PIN) #Mocker(0)
meas.spawn_process()
