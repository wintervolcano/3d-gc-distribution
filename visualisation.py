import plotly.graph_objects as go
import numpy as np
import re

# Load and parse the catalog file
file_path = 'harris_catalogue.txt'

# Initialize lists for parsed data
cluster_names = []
coordinates_x = []
coordinates_y = []
coordinates_z = []

# Parsing Part I for coordinates
with open(file_path, 'r') as file:
    lines = file.readlines()

# Regex pattern for coordinates
part_i_pattern = re.compile(
    r'^\s*(?P<id>\w+)\s+(?P<name>[\w\s]+?)\s+\d{2}\s+\d{2}\s+\d{2}\.?\d*\s+[-+]?\d{2}\s+\d{2}\s+\d{2}\.?\d*\s+'
    r'[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+(?P<x>[-+]?\d+\.\d+)\s+'
    r'(?P<y>[-+]?\d+\.\d+)\s+(?P<z>[-+]?\d+\.\d+)'
)

# Parse coordinates from Part I of the catalog
for line in lines:
    match = part_i_pattern.search(line)
    if match:
        cluster_names.append(match.group("name").strip())
        coordinates_x.append(float(match.group("x")))
        coordinates_y.append(float(match.group("y")))
        coordinates_z.append(float(match.group("z")))

# Generate data for a wider galactic disk
disk_x = np.random.normal(0, 30, 2000)
disk_y = np.random.normal(0, 30, 2000)
disk_z = np.random.normal(0, 1, 2000)

# Galactic center and solar system positions
galactic_center = [8.0, 0.0, 0.0]
solar_system = [0.0, 0.0, 0.0]

# Create the 3D plot
fig = go.Figure()

# Plot globular clusters with improved hover labels
fig.add_trace(go.Scatter3d(
    x=coordinates_x, y=coordinates_y, z=coordinates_z,
    mode='markers',
    marker=dict(size=4, color='violet'),
    name='Globular Clusters',
    hovertemplate="<b>%{text}</b><br>X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>",
    text=cluster_names  # Add cluster names for hover information
))

# Plot the galactic disk with increased spread
fig.add_trace(go.Scatter3d(
    x=disk_x, y=disk_y, z=disk_z,
    mode='markers',
    marker=dict(size=3, color='lightblue', opacity=0.2),
    name='Galactic Disk',
    hoverinfo='skip'  # No hover info for the disk for a cleaner look
))

# Plot the galactic center
fig.add_trace(go.Scatter3d(
    x=[galactic_center[0]], y=[galactic_center[1]], z=[galactic_center[2]],
    mode='markers',
    marker=dict(size=6, color='orange', symbol='diamond'),
    name='Galactic Center',
    hovertemplate="<b>Galactic Center</b><extra></extra>"
))

# Plot the solar system
fig.add_trace(go.Scatter3d(
    x=[solar_system[0]], y=[solar_system[1]], z=[solar_system[2]],
    mode='markers',
    marker=dict(size=6, color='yellow', symbol='circle'),
    name='Solar System',
    hovertemplate="<b>Solar System</b><extra></extra>"
))

# Update layout with a black background and camera position at the solar system
fig.update_layout(
    scene=dict(
        xaxis=dict(showbackground=False, visible=True),
        yaxis=dict(showbackground=False, visible=True),
        zaxis=dict(showbackground=False, visible= True),
        camera=dict(
            eye=dict(x=2, y=2, z=0.5),  # Adjusted for a view "from" the solar system
            center=dict(x=0, y=0, z=0)
        ),
        bgcolor='black',  # Set the background color of the plot area
    ),
    plot_bgcolor='black',  # Set the background color of the entire plot
    paper_bgcolor='black',  # Set the background color of the surrounding page
    title="Globular Clusters with Galactic Disk, Galactic Center, and Solar System",
    title_x=0.5,
    font=dict(color="white")  # White font for better contrast
)

# Show the plot
fig.show()
