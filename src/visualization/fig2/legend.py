import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Arial'

colors = [
    (141/255, 210/255, 198/255),
    (255/255, 255/255, 179/255),
    (189/255, 185/255, 218/255),
    (250/255, 128/255, 113/255),
    (128/255, 176/255, 210/255),
    (252/255, 180/255, 97/255),
    (179/255, 222/255, 105/255),
    (251/255, 205/255, 228/255),
    (217/255, 217/255, 217/255),
    (187/255, 128/255, 188/255),
]

labels = [
    "H7N7",
    "H7N9",
    "H7N3",
    "H7N6",
    "H7N2",
    "H7N1",
    "H7N4",
    "H7N8",
    "H7",
    "H7N5",
]

fig, ax = plt.subplots(figsize=(6, 6))

ax.axis('off')

ax.set_title("Color Legend", fontsize=16, fontweight="bold", pad=20)

for i, (color, label) in enumerate(zip(colors, labels)):
    y_position = len(colors) - i - 1
    ax.add_patch(plt.Rectangle((0, y_position), 1, 1, color=color))
    ax.text(1.2, y_position + 0.5, label, va="center", fontsize=12)

ax.set_xlim(-0.5, 3.5)
ax.set_ylim(-0.5, len(colors) + 0.5)

plt.show()