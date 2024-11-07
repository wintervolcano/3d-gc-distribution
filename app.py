import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np
import re
import os

# Initialize the Dash app
app = dash.Dash(__name__)

# Load and parse the catalog file
file_path = 'harris_catalogue.txt'
cluster_names = []
coordinates_x = []
coordinates_y = []
coordinates_z = []

# Parsing the catalog for coordinates
with open(file_path, 'r') as file:
    lines = file.readlines()

part_i_pattern = re.compile(
    r'^\s*(?P<id>\w+)\s+(?P<name>[\w\s]+?)\s+\d{2}\s+\d{2}\s+\d{2}\.?\d*\s+[-+]?\d{2}\s+\d{2}\s+\d{2}\.?\d*\s+'
    r'[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+(?P<x>[-+]?\d+\.\d+)\s+'
    r'(?P<y>[-+]?\d+\.\d+)\s+(?P<z>[-+]?\d+\.\d+)'
)

for line in lines:
    match = part_i_pattern.search(line)
    if match:
        cluster_names.append(f"{match.group('id')} {match.group('name').strip()}")
        coordinates_x.append(float(match.group("x")))
        coordinates_y.append(float(match.group("y")))
        coordinates_z.append(float(match.group("z")))

# Create the initial figure
fig = go.Figure()

# Add the globular clusters
fig.add_trace(go.Scatter3d(
    x=coordinates_x,
    y=coordinates_y,
    z=coordinates_z,
    mode='markers',
    marker=dict(
        size=4,
        color='purple',
        opacity=0.9,
    ),
    text=cluster_names,
    hoverinfo='text',
    name="Globular Clusters"
))

# Add the galactic disk
disk_x = np.random.normal(0, 13.4, 3000)
disk_y = np.random.normal(0, 13.4, 3000)
disk_z = np.random.normal(0, 1, 2000)
fig.add_trace(go.Scatter3d(
    x=disk_x,
    y=disk_y,
    z=disk_z,
    mode='markers',
    marker=dict(
        size=2,
        color='lightblue',
        opacity=0.2,
    ),
    hoverinfo='skip',
    name="Galactic Disk"
))

# Add solar system and galactic center markers with corrected positions
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers', marker=dict(size=5, color='yellow'), name='Solar System'))
fig.add_trace(go.Scatter3d(x=[8.0], y=[0], z=[0], mode='markers', marker=dict(size=10, color='white'), name='Galactic Center'))

# Update layout for a black background and internal legend positioning
fig.update_layout(
    scene=dict(
        xaxis=dict(showbackground=False, showgrid=False, visible=False),
        yaxis=dict(showbackground=False, showgrid=False, visible=False),
        zaxis=dict(showbackground=False, showgrid=False, visible=False),
    ),
    paper_bgcolor="black",
    plot_bgcolor="black",
    scene_camera=dict(eye=dict(x=2, y=2, z=0.1)),  # Focus on the solar system
    legend=dict(
        font=dict(size=12, color='white'),
        bgcolor="rgba(0,0,0,0)",  # Transparent legend background
        orientation="h",  # Horizontal legend inside plot
        x=0.02,  # Adjust position within the plot window
        y=0.95
    ),
    title=dict(
        text="3D Globular Clusters Visualization",
        font=dict(size=24, color='white'),
        x=0.5,
        xanchor='center',
        yanchor='top'
    )
)

# Full-screen app layout with enforced CSS
app.layout = html.Div(
    style={
        'backgroundColor': 'black',
        'height': '100vh',
        'width': '100vw',
        'color': 'black',
        'margin': '0',
        'padding': '0',
        'overflow': 'hidden'
    },
    children=[
        html.H1("", style={
            'text-align': 'center',
            'font-family': 'Arial, sans-serif',
            'font-weight': 'bold',
            'color': 'white',
            'margin': '0',
            'padding': '20px',
        }),
        
        dcc.Graph(
            id='3d-plot',
            figure=fig,
            style={'height': '100vh', 'width': '100vw'},
            config={
                'displayModeBar': True,  # Show mode bar
                'displaylogo': False,  # Remove Plotly logo
                'modeBarButtonsToRemove': [
                    'toImage', 'lasso2d', 'select2d', 'zoomIn2d', 'zoomOut2d', 
                    'resetScale2d', 'hoverCompareCartesian', 'hoverClosestCartesian'
                ]  # Customize mode bar options
            }
        )
    ]
)

if __name__ == '__main__':
    # Run the app on the specified host and port
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
