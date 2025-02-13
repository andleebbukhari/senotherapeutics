# Import required libraries
import networkx as nx
import matplotlib.pyplot as plt
import textwrap  # For adding line breaks automatically
from matplotlib.patches import Patch

# Define categories with pastel colors and sun-like yellow for Senotherapeutics
categories = {
    "Senolytics": "#A8D5BA",  # Pastel Green
    "Senomorphics": "#F7DCB9",  # Pastel Yellow
    "Senoblockers": "#F4B6C2",  # Pastel Pink
    "Senoreversers": "#CDB4DB",  # Pastel Purple
    "Senotherapeutics": "#FFD700"  # Sun Yellow
}

# Create directed graph
G = nx.DiGraph()

# Define node sizes in hierarchical format
node_sizes = {
    "Senotherapeutics": 25000,  # Largest
    "Senolytics": 15000,  
    "Senomorphics": 15000,
    "Senoblockers": 15000,
    "Senoreversers": 15000
}

# Add main category
G.add_node("Senotherapeutics", size=node_sizes["Senotherapeutics"], color=categories["Senotherapeutics"], subset="center")

# Define drugs and their mechanisms
senotherapeutic_drugs = {
    "Senolytics": [
        ("Dasatinib + Quercetin", "Targets SCAPs"),
        ("ABT-737", "Inhibits BCL-2,\nBCL-XL, BCL-W"),
        ("ABT-263 (Navitoclax)", "Inhibits BCL-2,\nBCL-XL, BCL-W"),
        ("A-1331852", "Inhibits BCL-XL"),
        ("A-1155463", "Inhibits BCL-XL"),
        ("17-DMAG (alvespimycin)", "Disrupts HSP90-AKT"),
        ("Geldanamycin", "Inhibits HSP90"),
        ("17-AAG (tanespimycin)", "Inhibits HSP90"),
        ("Ganetespib", "Inhibits HSP90"),
        ("FOXO4-DRI", "Disrupts FOXO4-p53"),
        ("UBX0101", "Disrupts MDM2/p53"),
        ("RG7112 (RO5045337)", "Disrupts MDM2/p53"),
        ("P5091", "USP7 inhibitor"),
        ("P22077", "USP7 inhibitor"),
        ("Pano", "HDAC inhibitor"),
        ("Proscillaridin A", "Inhibits Na+/K+-ATPase"),
        ("Ouabain", "Inhibits Na+/K+-ATPase,\nup-regulates BCL2-NOXA"),
        ("Digoxin", "Induces apoptosis,\nincreases BAX, BAD,\nBOK, BAK-1, NOXA"),
        ("Fisetin", "Targets BCL-2, PI3K/AKT,\np53, NF-kB"),
        ("EGCG", "mTOR inhibitor"),
        ("Genistein", "mTOR, AMPK,\nERβ modulator"),
        ("EF-24 (curcumin analogue)", "Targets BCL-2")
    ],
    "Senomorphics": [
        ("Apigenin", "Blocks ATM/p38,\nsuppresses iPLA2-PRDX6"),
        ("Kaempferol", "PDK1 inhibition,\nincreases DAF-16/FOXO"),
        ("Oleuropein", "Regulates Cx43,\nhMSC differentiation"),
        ("Rapamycin", "mTOR inhibition"),
        ("Azithromycin", "Induces autophagy\nand glycolysis"),
        ("Roxithromycin", "Targets NOX4"),
        ("Metformin", "Activates AMPK,\ninhibits mTOR"),
        ("Resveratrol", "Activates SIRT1"),
        ("NMN", "Precursor of NAD+"),
        ("Ruxolitinib", "JAK1/2 inhibitor,\nreduces SASP expression"),
        ("KU-55933", "ATM inhibitor"),
        ("KU-60019", "ATM inhibitor"),
        ("Atorvastatin", "HMG-CoA reductase inhibitor"),
        ("Pravastatin", "HMG-CoA reductase inhibitor"),
        ("Pitavastatin", "HMG-CoA reductase inhibitor"),
        ("Simvastatin", "HMG-CoA reductase inhibitor, protein prenylation inhibition"),
        ("Tocilizumab", "Blocks IL-6 receptor"),
        ("Pirfenidone", "Blocks TGF-β signaling"),
        ("Doxycycline", "Inhibits MMPs"),
        ("NSAIDs (aspirin, ibuprofen)", "Reduces prostaglandin production"),
        ("AntagomiRs (anti-miR-146a)", "Blocks miRNAs involved in inflammation"),
        ("Neutralizing antibodies", "Disrupts exosome release")
    ],
    "Senoblockers": [
        ("Metformin", "Activates AMPK"),
        ("Resveratrol", "Activates SIRT1"),
        ("Alisertib", "Inhibits Aurora A kinase")
    ],
    "Senoreversers": [
        ("Reversine", "Inhibits Aurora B kinase"),
        ("miR-302b", "Targets Cdkn1a and Ccng2")
    ]
}

# Function to format labels for better readability
def format_label(name, mechanism, width=20):
    wrapped_text = textwrap.wrap(mechanism, width)  # Wrap the mechanism text
    return f"{name}\n" + "\n".join(wrapped_text)  # Corrected f-string usage

# Add categories and their drugs to the graph
for category, drugs in senotherapeutic_drugs.items():
    G.add_node(category, size=node_sizes[category], color=categories[category], subset="category")
    G.add_edge("Senotherapeutics", category)
    
    for drug, mechanism in drugs:
        formatted_label = format_label(drug, mechanism)  # Auto-wrap text
        G.add_node(drug, size=9000, color=categories[category], subset=category, label=formatted_label)
        G.add_edge(category, drug)

# Define hierarchical layout
pos = nx.multipartite_layout(G, subset_key="subset")

# **Fix: Only Adjust Category Spacing, Not Drugs**
spacing_factor = 2.5  # Increase only for main categories
for key in pos:
    if key in node_sizes:  # Only adjust the category nodes
        pos[key][1] *= spacing_factor

# Draw the graph
plt.figure(figsize=(25, 20))
nx.draw(
    G, pos, with_labels=True, labels={node: G.nodes[node].get("label", node) for node in G.nodes},
    node_size=[G.nodes[node]["size"] for node in G.nodes],
    node_color=[G.nodes[node]["color"] for node in G.nodes],
    font_size=10, font_weight="bold", edge_color="gray"
)

# **Add Legend in Upper Left Corner**
legend_patches = [Patch(color=color, label=category) for category, color in categories.items()]
plt.legend(handles=legend_patches, title="Categories", loc="upper left", fontsize=12, title_fontsize=14, frameon=True)

# **Removed the Title**
# plt.title("Senotherapeutics Hierarchical Visualization")  <-- Removed this line

plt.show()
