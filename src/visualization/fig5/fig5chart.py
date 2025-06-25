import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

nodes = ["Anseriformes", "Other", "Environment","Human",  "Galliformes"]
sizes = [35.5,10.47,  22.15, 22.62, 9.25]
color_map = ['#4E79A7', '#B07AA1','#BAB0AC',  '#59A14F', '#E15759']

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(
    sizes, 
    # labels=nodes, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=color_map, 
    pctdistance=0.9
)

centre_circle = plt.Circle((0, 0), 0.80, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.setp(autotexts, size=10, weight="bold")
plt.setp(texts, size=12)

# plt.title('Distribution of Categories', fontsize=16)

plt.tight_layout()
plt.savefig("doughnut_chart.png", format="png", dpi=300)
print("图表已保存为 'doughnut_chart.png'")
plt.savefig("doughnut_chart.svg", format="svg", dpi=600)

plt.show()