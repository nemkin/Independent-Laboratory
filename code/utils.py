import json
from collections import deque

def load_instance_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    return content.get('data', {})

def build_adjacency_and_degrees(donors):
    adj = {d_id: [] for d_id in donors}
    in_degree = {d_id: 0 for d_id in donors}
    out_degree = {d_id: len(info.get('matches', [])) for d_id, info in donors.items()}

    for donor_id, info in donors.items():
        for match in info.get('matches', []):
            rec_id = str(match['recipient'])
            if rec_id in donors:
                adj[donor_id].append((rec_id, match.get('score', 1)))
                in_degree[rec_id] += 1
    return adj, in_degree, out_degree

def calculate_topological_levels(donors, adj, in_degree, out_degree):
    levels = {d_id: 0 for d_id in donors}
    queue = deque()
    
    for d_id in donors:
        is_alt = donors[d_id].get('altruistic', False)
        if is_alt or in_degree[d_id] == 0:
            if not (in_degree[d_id] == 0 and out_degree[d_id] == 0):
                levels[d_id] = 1
                queue.append(d_id)
            else:
                levels[d_id] = 0

    temp_in_degree = in_degree.copy()
    while queue:
        u = queue.popleft()
        for v, _ in adj[u]:
            levels[v] = max(levels[v], levels[u] + 1)
            temp_in_degree[v] -= 1
            if temp_in_degree[v] == 0:
                queue.append(v)

    current_max = max(levels.values()) if levels else 1
    for d_id in donors:
        if levels[d_id] == 0 and not (in_degree[d_id] == 0 and out_degree[d_id] == 0):
            levels[d_id] = current_max + 1
            current_max += 1 

    final_depth = max(levels.values()) + 1
    for d_id in donors:
        if out_degree[d_id] == 0 and levels[d_id] != 0:
            levels[d_id] = final_depth
    return levels