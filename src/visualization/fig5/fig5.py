



import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

G = nx.DiGraph()

nodes = ["Anseriformes", "Galliformes", "Human", "Environment", "Other"]
color_map = ['#4E79A7', '#E15759', '#59A14F', '#BAB0AC', '#B07AA1']

edges = [
    ("Galliformes", "Anseriformes", 8),
    ("Anseriformes", "Galliformes", 6),
    ("Galliformes", "Human", 17),
    ("Human", "Galliformes", 32),
    ("Environment", "Human", 18),
    ("Human", "Environment", 5),
    ("Human", "Anseriformes", 5),
    ("Galliformes", "Environment", 4),
    ("Human", "Other", 4),
    ("Anseriformes", "Other", 6),
    ("Environment", "Anseriformes",6),
]

G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

pos = {
    "Anseriformes": (0.2, 0.8),
    "Galliformes": (0.8, 0.8),
    "Human": (0.8, 0.2),
    "Environment": (0.5, 0.1),
    "Other": (0.2, 0.2),
}

fig = plt.figure(figsize=(8, 8), dpi=300)
ax = fig.add_subplot(111)

node_colors = [color for n, color in zip(nodes, color_map)]
node_edgecolors = [color for n, color in zip(nodes, color_map)]
nx.draw_networkx_nodes(
    G, pos, nodelist=nodes,
    node_size=3000,
    node_color=node_colors,
    edgecolors=node_edgecolors,
    linewidths=2.5,
    alpha=0.9
)

max_width = max([e[2] for e in edges])
for u, v, w in edges:
    nx.draw_networkx_edges(
        G, pos,
        edgelist=[(u, v)],
        width=(0.5 + 1.5 * (w / max_width)) * 20,
        edge_color=color_map[nodes.index(u)],
        alpha=0.7,
        arrowsize=30,
        connectionstyle='arc3,rad=0.15'
    )


plt.axis('off')
plt.gca().set_facecolor('none')

plt.savefig("transmission_network_modified.svg", 
            format="svg", 
            transparent=True,
            bbox_inches='tight',
            pad_inches=0.3)

plt.savefig("transmission_network_modified.png",
            dpi=900,
            transparent=True,
            bbox_inches='tight',
            pad_inches=0.3)
