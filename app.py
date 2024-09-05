from flask import Flask, render_template, request, jsonify
import networkx as nx
import folium
from collections import deque

app = Flask(__name__)

# Example fantasy graph with distances between locations
fantasy_graph = {
    'Eldoria': {'Stormspire': 10, 'Verdant Hollow': 15, "Dragon's Lair": 30},
    'Stormspire': {'Eldoria': 10, 'Verdant Hollow': 5, 'Obsidian Peaks': 20},
    'Verdant Hollow': {'Eldoria': 15, 'Stormspire': 5, 'Obsidian Peaks': 10, 'Celestia Bay': 25},
    'Obsidian Peaks': {'Stormspire': 20, 'Verdant Hollow': 10, 'Celestia Bay': 15, 'Shadowfen': 50},
    'Celestia Bay': {'Verdant Hollow': 25, 'Obsidian Peaks': 15, 'Shadowfen': 10},
    'Shadowfen': {'Obsidian Peaks': 10, 'Celestia Bay': 10},
    "Dragon's Lair": {'Eldoria': 30}
}

# Coordinates for fantasy locations (latitude, longitude)
location_coords = {
    'Eldoria': [37.7749, -122.4194],      # Example: San Francisco
    'Stormspire': [34.0522, -118.2437],   # Example: Los Angeles
    'Verdant Hollow': [36.1699, -115.1398],  # Example: Las Vegas
    'Obsidian Peaks': [40.7128, -74.0060],   # Example: New York
    'Celestia Bay': [25.7617, -80.1918],     # Example: Miami
    'Shadowfen': [47.6062, -122.3321],       # Example: Seattle
    "Dragon's Lair": [35.6762, 139.6503]     # Example: Tokyo
}

# BFS function to find the shortest path
def bfs_shortest_path(graph, start, goal):
    if start not in graph or goal not in graph:
        return None
    
    queue = deque([(start, [start])])
    visited = set()
    
    while queue:
        current_node, path = queue.popleft()
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
