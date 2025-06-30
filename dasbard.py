import dash
from dash import dcc, html
import pandas as pd
import os

app = dash.Dash(__name__)
app.title = "IDPS Accuracy Monitor"

def load_accuracy_log():
    if os.path.exists("accuracy_log.csv"):
        return pd.read_csv("accuracy_log.csv")
    return pd.DataFrame(columns=["Timestamp", "Accuracy"])

app.layout = html.Div([
    html.H1("🛡️ IDPS Accuracy Dashboard"),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
    dcc.Graph(id='accuracy-chart')
])

@app.callback(
    dash.dependencies.Output('accuracy-chart', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = load_accuracy_log()
    if df.empty:
        return {
            'data': [],
            'layout': {'title': 'Waiting for accuracy data...'}
        }

    return {
        'data': [{
            'x': df["Timestamp"],
            'y': df["Accuracy"].astype(float),
            'type': 'line',
            'name': 'Accuracy'
        }],
        'layout': {
            'title': 'Real-time Accuracy Over Time',
            'xaxis': {'title': 'Timestamp'},
            'yaxis': {'title': 'Accuracy (%)'},
            'margin': {'l': 60, 'r': 40, 't': 50, 'b': 80},
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
