import re

# Initialize lists for parsed data
cluster_names = []
coordinates_x = []
coordinates_y = []
coordinates_z = []

# Load and parse the catalog file
file_path = 'harris_catalogue.txt'

# Updated pattern to match only the first two columns as the cluster name, then coordinates
part_i_pattern = re.compile(
    r'^\s*(?P<col1>\w+)\s+(?P<col2>\w+)?\s+\d{2}\s+\d{2}\s+\d{2}\.?\d*\s+[-+]?\d{2}\s+\d{2}\s+\d{2}\.?\d*\s+'
    r'[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+(?P<x>[-+]?\d+\.\d+)\s+'
    r'(?P<y>[-+]?\d+\.\d+)\s+(?P<z>[-+]?\d+\.\d+)'
)

# Read the file and parse each line
with open(file_path, 'r') as file:
    lines = file.readlines()

for line in lines:
    match = part_i_pattern.search(line)
    if match:
        # Combine the first two columns into one cluster name
        col1 = match.group("col1").strip()
        col2 = match.group("col2").strip() if match.group("col2") else ""
        cluster_name = f"{col1} {col2}".strip()  # Join with a space and trim extra spaces
        cluster_names.append(cluster_name)
        
        # Extract coordinates
        coordinates_x.append(float(match.group("x")))
        coordinates_y.append(float(match.group("y")))
        coordinates_z.append(float(match.group("z")))

# Print sample output to verify the full names
print(cluster_names[:10])  # Print the first 10 names to verify
