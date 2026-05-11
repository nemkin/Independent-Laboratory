UI_OVERLAY = """
<div id="ui-layer" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999;">
    <div id="legend-wrapper" style="position: absolute; top: 20px; left: 20px; pointer-events: auto;">
        <button class="ui-btn" onclick="toggleDisplay('legend-content')">Toggle Legend</button>
        <div id="legend-content" style="display: block; margin-top: 10px; background: rgba(0, 0, 0, 0.85); color: white; padding: 20px; border-radius: 10px; border: 1px solid #444; min-width: 250px; font-family: sans-serif; font-size: 14px;">
            <h3 style="margin-top: 0; border-bottom: 1px solid #666; padding-bottom: 5px;">Network Legend</h3>
            <div style="margin-bottom: 15px;">
                <strong>Node Shapes (Blood Type):</strong><br>
                ○ Circle: Type O | □ Square: Type A | △ Triangle: Type B | ◇ Diamond: Type AB
            </div>
            <div style="margin-bottom: 15px;">
                <strong>Node Colors (Sensitivity):</strong><br>
                <span style="color:#39ff14">■</span> Altruistic Donor (NDD)<br>
                <span style="color:#97c2fc">■</span> Low cPRA | <span style="color:#00008B">■</span> High cPRA
            </div>
            <div><strong>Visual Cues:</strong> Size = Compatibility | Thickness = Score</div>
        </div>
    </div>
    <button id="config-btn" class="ui-btn" onclick="toggleConfig()" style="position: absolute; top: 20px; right: 20px; pointer-events: auto;">⚙ Settings</button>
</div>
<style>
    .ui-btn { background: #333; color: white; border: 1px solid #555; padding: 8px 15px; border-radius: 5px; cursor: pointer; }
    .vis-configuration-wrapper { position: absolute !important; top: 70px !important; right: 20px !important; z-index: 10000 !important; display: none; background: rgba(255, 255, 255, 0.9) !important; }
    body, html { margin: 0; padding: 0; overflow: hidden; background-color: #222; }
</style>
<script>
    function toggleDisplay(id) { const el = document.getElementById(id); el.style.display = (el.style.display === 'none') ? 'block' : 'none'; }
    function toggleConfig() { const config = document.querySelector('.vis-configuration-wrapper'); if (config) { config.style.display = (config.style.display === 'none' || config.style.display === '') ? 'block' : 'none'; } }
</script>
"""

def inject_ui(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('<body>', f'<body>{UI_OVERLAY}')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)