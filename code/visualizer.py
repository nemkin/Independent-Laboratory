import os
import json
from pyvis.network import Network
from utils import load_instance_data, build_adjacency_and_degrees, calculate_topological_levels
from styles import get_node_style, get_graph_options
from ui_templates import inject_ui

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, '..', 'KEP_Survey_Experimentation_Instances', 'uk_2019_splitpra_bandxmatch_pra0_pdd_0.05_50_0.json')
OUTPUT_PATH = os.path.join(BASE_DIR, 'out', 'kidney_exchange_graph.html')

def run_visualization():
    # 1. Data Preparation
    donors = load_instance_data(JSON_FILE)
    adj, in_degree, out_degree = build_adjacency_and_degrees(donors)
    levels = calculate_topological_levels(donors, adj, in_degree, out_degree)

    # 2. Network Initialization
    net = Network(height='100vh', width='100%', bgcolor='#222222', font_color='white', directed=True)

    # 3. Add Nodes
    for d_id, info in donors.items():
        style = get_node_style(d_id, info, out_degree[d_id], levels[d_id])
        net.add_node(d_id, **style)

    # 4. Add Edges
    for d_id, targets in adj.items():
        for target_id, score in targets:
            width = max(1, min(5, score / 20))
            net.add_edge(d_id, target_id, width=width, color="rgba(200,200,200,0.5)")

    # 5. Options and Save
    net.set_options(json.dumps(get_graph_options()))
    
    out_dir = os.path.dirname(OUTPUT_PATH)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    net.save_graph(OUTPUT_PATH)
    
    # 6. UI Injection
    inject_ui(OUTPUT_PATH)
    print(f"Success! Graph generated at: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_visualization()