import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv('traffic1.csv')


app.layout = html.Div([
    dcc.Graph(
        id='Frames',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['Frames'] == i]['Frames'],
                    y=df[df['Vehicles'] == i]['Vehicles'],
                    text=df[df['Frames'] == i]['Frames'],
                    mode='markers',
                    opacity=0.8,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.Frames.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'Frames'},
                yaxis={'title': 'Vehicles'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server()