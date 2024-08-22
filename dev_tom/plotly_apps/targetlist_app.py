"""
Plotly-Dash app to produce an interactive, customized targetlist table
"""
from django.conf import settings
from dash import Dash
from django_plotly_dash import DjangoDash

app = DjangoDash('TargetlistTable')

# Customize this list based on a set of columns declared in the settings.py
table_columns = [dict(name=col, id=col, type=typ) for col,typ in settings.TARGETLIST_COLUMNS]

# Build the table dataset
table_data = []
for t in object_list:
    table_data.append({x:getattr(t,col) for col,typ in settings.TARGETLIST_COLUMNS})

# Create the Plotly output
app.layout = html.Div(
    dash_table.DataTable(
            id='TargetlistTable',
            columns=table_columns,
            data=table_data,
            sort_action="native",
            filter_action="native",
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_cell={'fontSize':18, 'font-family':'sans-serif'},
            )
)