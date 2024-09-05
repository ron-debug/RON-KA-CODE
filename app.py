from flask import Flask, render_template, request, jsonify
import networkx as nx
import folium
from collections import deque

app = Flask(__name__)

# Example fantasy graph with imaginary distances and coordinates
fantasy_graph = {
    'Eldoria': {'Stormspire': 10, 'Verdant Hollow': 15, "Dragon's Lair": 30},
    'Stormspire': {'Eldoria': 10, 'Verdant Hollow': 5, 'Obsidian Peaks': 20},
    'Verdant Hollow': {'Eldoria': 15, 'Stormspire': 5, 'Obsidian Peaks': 10, 'Celestia Bay': 25},
    'Obsidian Peaks': {'Stormspire': 20, 'Verdant Hollow': 10, 'Celestia Bay': 15, 'Shadowfen': 50},
    'Celestia Bay': {'Verdant Hollow': 25, 'Obsidian Peaks': 15, 'Shadowfen': 10},
    'Shadowfen': {'Obsidian Peaks': 10, 'Celestia Bay': 10},
    "Dragon's Lair": {'Eldoria': 30}
}

# Coordinates for the fantasy locations (latitude, longitude)
location_coords = {
    'Eldoria': [37.7749, -122.4194],      # Example: San Francisco
    'Stormspire': [34.0522, -118.2437],   # Example: Los Angeles
    'Verdant Hollow': [36.1699, -115.1398],  # Example: Las Vegas
    'Obsidian Peaks': [40.7128, -74.0060],   # Example: New York
    'Celestia Bay': [25.7617, -80.1918],     # Example: Miami
    'Shadowfen': [47.6062, -122.3321],       # Example: Seattle
    "Dragon's Lair": [35.6762, 139.6503]     # Example: Tokyo
}

# BFS to find the shortest path
def bfs_shortest_path(graph, start, goal):
    if start not in graph or goal not in graph:
        return None
    
    queue = deque([(start, [start])])
    visited = set()
    
    while queue:
        (current_node, path) = queue.popleft()
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        if current_node == goal:
            return path
        
        for neighbor in graph.get(current_node, {}):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    
    return None

# Create a map with the path marked
def draw_map(graph, path=None):
    # Center the map at a default location (Eldoria)
    m = folium.Map(location=location_coords['Eldoria'], zoom_start=4)

    # Add nodes (locations) to the map
    for location, coords in location_coords.items():
        folium.Marker(location=coords, popup=location).add_to(m)

    # If there is a path, draw it on the map
    if path:
        route_coords = [location_coords[loc] for loc in path]
        folium.PolyLine(route_coords, color="red", weight=2.5, opacity=1).add_to(m)

    # Return the map as HTML
    return m._repr_html_()

@app.route('/')
def index():
    locations = list(fantasy_graph.keys())
    return render_template('index.html', locations=locations)

@app.route('/find_route', methods=['POST'])
def find_route():
    start = request.form.get('start')
    goal = request.form.get('goal')
    
    # Validate the input
    if start not in fantasy_graph or goal not in fantasy_graph:
        return jsonify({"error": "Invalid start or goal location."})
    
    # Find the shortest path using BFS
    route = bfs_shortest_path(fantasy_graph, start, goal)
    
    if route:
        route_str = ' -> '.join(route)
        map_html = draw_map(fantasy_graph, route)
        return jsonify({"route": route_str, "map_html": map_html})
    else:
        return jsonify({"route": "No route found.", "map_html": None})

if __name__ == '__main__':
    app.run(debug=True)

