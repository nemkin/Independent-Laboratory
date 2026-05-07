def get_node_style(donor_id, info, out_degree, level):
    is_alt = info.get('altruistic', False)
    blood_type = info.get('bloodtype', 'O')
    cpra = info.get('cPRA', 0)
    shapes = {"O": "dot", "A": "square", "B": "triangle", "AB": "diamond"}
    
    node_shape = shapes.get(blood_type, "dot")
    if is_alt:
        node_color = "#39ff14"
    else:
        intensity = int(255 * (1 - cpra))
        node_color = f"rgb({intensity // 2}, {intensity}, 255)"
            
    return {
        "label": f"NDD {donor_id}" if is_alt else f"Pair {donor_id}",
        "color": node_color,
        "shape": node_shape,
        "size": 15 + (out_degree * 2),
        "level": level,
        "title": f"<b>Blood Type:</b> {blood_type}<br><b>cPRA:</b> {cpra:.2%}<br><b>Matches:</b> {out_degree}"
    }

def get_graph_options():
    return {
        "layout": {
            "hierarchical": {
                "enabled": True, "levelSeparation": 600, "nodeSpacing": 300,
                "direction": "LR", "sortMethod": "explicit", "edgeMinimization": True, "parentCentralization": True
            }
        },
        "physics": {
            "enabled": True, "solver": "hierarchicalRepulsion",
            "hierarchicalRepulsion": {"centralGravity": 0.5, "springLength": 250, "nodeDistance": 400, "avoidOverlap": 1}
        },
        "edges": {
            "smooth": {"type": "cubicBezier", "forceDirection": "horizontal"}, 
            "arrows": {"to": {"enabled": True, "scaleFactor": 1.2}}, 
            "width": 2
        },
        "configure": {"enabled": True, "filter": ["physics", "layout"]}
    }