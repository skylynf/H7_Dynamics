import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import font_manager

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

node_colors = {
    "Anseriformes": '#4E79A7',
    "Galliformes": '#E15759',
    "Human": '#59A14F',
    "Environment": '#BAB0AC',
    "Other": '#B07AA1'
}

abbrev_to_full = {
    'G': 'Galliformes',
    'A': 'Anseriformes',
    'H': 'Human',
    'E': 'Environment',
    'O': 'Other'
}

pos = {
    "Anseriformes": (0.2, 0.8),
    "Galliformes": (0.8, 0.8),
    "Human": (0.8, 0.2),
    "Environment": (0.5, 0.1),
    "Other": (0.2, 0.2),
}

graphs = [
    {   # Graph1
        "edges": ["G-A 21", "A-G 39", "G-H 5", "H-G 7", "A-E 23", "A-O 32", "O-A 9"],
        "nodes": ["Anseriformes", "Other", "Environment", "Human", "Galliformes"],
        "sizes": [52.01, 9.47, 3.58, 5.47, 29.47]
    },
    {   # Graph2
        "edges": ["G-A 17", "A-G 8", "A-O 18", "O-A 3"],
        "nodes": ["Anseriformes", "Other", "Environment", "Human", "Galliformes"],
        "sizes": [57.61, 5.79, 0.27, 0, 36.33]
    },
    {   # Graph3
        "edges": ["A-G 21", "G-A 7", "A-E 18", "E-A 5", "A-O 26", "O-A 8"],
        "nodes": ["Anseriformes", "Other", "Environment", "Human", "Galliformes"],
        "sizes": [62.49, 14.38, 8.22, 0.6, 14.32]
    }
]

def parse_edges(edge_strs):
    """解析边数据"""
    edges = []
    for edge_str in edge_strs:
        parts = edge_str.split()
        nodes_part, weight = parts[0], int(parts[1])
        source, target = nodes_part.split('-')
        edges.append((
            abbrev_to_full[source],
            abbrev_to_full[target],
            weight
        ))
    return edges

def draw_transmission_network(graph_data, index):
    """绘制传播网络图"""
    G = nx.DiGraph()
    
    edges = parse_edges(graph_data["edges"])
    nodes = graph_data["nodes"]
    sizes = graph_data["sizes"]
    
    max_size = max(sizes)
    scaling_factor = 3000 / max_size
    node_sizes = [s * scaling_factor for s in sizes]
    
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(edges)
    
    plt.figure(figsize=(8, 8), dpi=300)
    ax = plt.gca()
    
    nx.draw_networkx_nodes(
        G, pos, nodelist=nodes,
        node_size=node_sizes,
        node_color=[node_colors[n] for n in nodes],
        edgecolors=[node_colors[n] for n in nodes],
        linewidths=2.5,
        alpha=0.9
    )
    
    if edges:
        max_weight = max([e[2] for e in edges])
        for u, v, w in edges:
            nx.draw_networkx_edges(
                G, pos, edgelist=[(u, v)],
                width=(0.5 + 1.5 * (w / max_weight)) * 20,
                edge_color=node_colors[u],
                alpha=0.7,
                arrowsize=30,
                connectionstyle='arc3,rad=0.15'
            )
    
    plt.axis('off')
    plt.gca().set_facecolor('none')
    plt.savefig(f"network_{index}.svg", bbox_inches='tight', transparent=True)
    plt.savefig(f"network_{index}.png", dpi=900, transparent=True)
    plt.close()

def draw_doughnut_chart(graph_data, index):
    """绘制环形图"""
    sizes = graph_data["sizes"]
    nodes = graph_data["nodes"]
    
    colors = [node_colors[n] for n in nodes]
    
    plt.figure(figsize=(8, 8))
    wedges, _, autotexts = plt.pie(
        sizes,
        autopct=lambda p: '%1.1f%%' % p if p >= 0.1 else '',
        startangle=90,
        colors=colors,
        pctdistance=0.9,
        textprops={'color': 'black'}
    )
    
    plt.gca().add_artist(plt.Circle((0,0), 0.8, fc='white'))
    
    plt.setp(autotexts, size=10, weight='bold')
    
    plt.savefig(f"donut_tight_{index}.png", dpi=300, bbox_inches='tight')
    plt.savefig(f"donut_tight_{index}.svg", bbox_inches='tight', transparent=True, dpi=600)
    plt.close()

for idx, graph in enumerate(graphs, 1):
    draw_transmission_network(graph, idx)
    draw_doughnut_chart(graph, idx)

print("所有图形已生成完毕！")