import json
import gurobipy as gp
from gurobipy import GRB

def solve_kep(alt, size, run, K=3):
    # Fájlnév összeállítása
    alt_str = f"{alt:.2f}" 
    file_name = f"./KEP_Survey_Experimentation_Instances/uk_2019_splitpra_bandxmatch_pra0_pdd_{alt_str}_{size}_{run}.json"
    
    try:
        with open(file_name, 'r') as f:
            content = json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_name} file not found.")
        return

    data = content['data']
    
    # Csak azokat a donorokat tartjuk meg, akik NEM altruisták (van source-uk)
    nodes = [node_id for node_id, d in data.items() if "sources" in d and len(d["sources"]) > 0]
    
    # Élek (donor -> recipient) és súlyok kigyűjtése
    edges = {}
    for donor_id in nodes:
        if 'matches' in data[donor_id]:
            for match in data[donor_id]['matches']:
                rec_id = str(match['recipient'])
                # Csak akkor él, ha a célszemély is a rendszerben lévő páros tagja
                if rec_id in nodes:
                    edges[(donor_id, rec_id)] = match['score']

    # KÖRKERESÉS (K=2 és K=3)
    cycles = []
    
    # 2-es körök: A -> B -> A
    for i, u in enumerate(nodes):
        for v in nodes[i+1:]:
            if (u, v) in edges and (v, u) in edges:
                weight = edges[(u, v)] + edges[(v, u)]
                cycles.append({'nodes': [u, v], 'weight': weight, 'length': 2})

    # 3-as körök: A -> B -> C -> A
    if K >= 3:
        for i, u in enumerate(nodes):
            for j, v in enumerate(nodes):
                if i == j: continue
                for k, w in enumerate(nodes):
                    if k <= i or k <= j: continue # Ismétlések elkerülése
                    
                    # Lehetséges irányok: u->v->w->u vagy u->w->v->u
                    perms = [(u, v, w), (u, w, v)]
                    for p1, p2, p3 in perms:
                        if (p1, p2) in edges and (p2, p3) in edges and (p3, p1) in edges:
                            weight = edges[(p1, p2)] + edges[(p2, p3)] + edges[(p3, p1)]
                            # Csak egyszer adjuk hozzá a kört (rendezett tuple-ként tárolva a csomópontokat)
                            cycles.append({'nodes': [p1, p2, p3], 'weight': weight, 'length': 3})

    # --- ÖSSZES KÖR MEGJELENÍTÉSE ---
    print("\n" + "="*60)
    print(f" ALL POSSIBLE CYCLES ({len(cycles)})")
    print("="*60)
    for idx, c in enumerate(cycles):
        nodes_path = " -> ".join(c['nodes']) + " -> " + c['nodes'][0]
        print(f" #{idx+1:2} | Length: {c['length']} | Weight: {c['weight']:4} | Path: {nodes_path}")

    # OPTIMALIZÁLÁS (Gurobi)
    model = gp.Model("KidneyExchange_CyclesOnly")
    model.Params.OutputFlag = 0 # Ne írja tele a képernyőt logokkal
    
    x = model.addVars(len(cycles), vtype=GRB.BINARY, name="c")
    model.setObjective(gp.quicksum(x[i] * cycles[i]['weight'] for i in range(len(cycles))), GRB.MAXIMIZE)
    
    # Minden páciens legfeljebb egy körben
    for node in nodes:
        model.addConstr(gp.quicksum(x[i] for i in range(len(cycles)) if node in cycles[i]['nodes']) <= 1)
    
    model.optimize()

    # --- EREDMÉNYEK KIÍRÁSA ---
    used_nodes = set()
    if model.status == GRB.OPTIMAL:
        print("\n" + "="*60)
        print(" CHOOSEN CYCLES")
        print(f"FILE: {file_name}")
        print("="*60)
        selected_count = 0
        for i in range(len(cycles)):
            if x[i].X > 0.5:
                selected_count += 1
                used_nodes.update(cycles[i]['nodes'])
                nodes_path = " -> ".join(cycles[i]['nodes']) + " -> " + cycles[i]['nodes'][0]
                print(f" Cycle: {nodes_path} | Weight: {cycles[i]['weight']}")
        
        print("-" * 60)
        print(f" MAX WEIGHT: {model.ObjVal}")
        print(f" Number of choosen cycles: {selected_count} from {len(cycles)}.")
        
        # --- KIMARADT CSÚCSOK ÉS KAPCSOLATAIK ---
        remaining_nodes = [n for n in nodes if n not in used_nodes]
        print("\n" + "="*60)
        print(f" UNUSED NODES AND THEIR INTERNAL CONNECTIONS ({len(remaining_nodes)} nodes)")
        print("="*60)
        
        # Megnézzük, van-e bármilyen él a kimaradt csúcsok között
        found_connection = False
        for u in remaining_nodes:
            for v in remaining_nodes:
                if (u, v) in edges:
                    found_connection = True
                    print(f" Connection: {u} -> {v} (Weight: {edges[(u, v)]})")
        
        if not found_connection:
            print(" No connections found between unused nodes.")
        else:
            print("\n (Note: If no cycles appear here, the model is working perfectly.)")
            
    else:
        print("No solution found.")
    
    print("-" * 60)
    print(f"Parameters: alt={alt}, size={size}, run={run}, K={K}")
    print("="*60 + "\n")

# --- HASZNÁLAT ---
# alt: 0.05, 0.10 vagy 0.20
# size: 50, 100, 200, 500, 750, 1000
# run: a fájl végi szám (0-9)
solve_kep(alt=0.05, size=100, run=7, K=3)