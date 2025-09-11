import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

reader = csv.reader(open('opt.csv', 'r'))

rows = []
for row in reader:
    rows.append(row)

y1 = []
y2 = []

for row in rows[1:]:
    y1.append(float(row[1]))
    y2.append(float(row[2]))

paired = sorted(zip(y1, y2), key=lambda p: 1 - p[1] / p[0])
y1, y2 = zip(*paired)
y1 = np.array(list(y1))
y2 = np.array(list(y2))
matplotlib.rcParams.update({
    "text.usetex": True,
    "font.size": 12,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "axes.unicode_minus": False  # 让负号正常显示
})

plt.figure(figsize=(5, 2))
x = np.array(range(len(y1)))
plt.ylim(0, 50)
plt.xlim(0, len(y1) - 1)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.plot(x, (1 - y2 / y1) * 100, color="0.5", label="Optimized \\%")
plt.fill_between(x, (1 - y2 / y1) * 100, color="0.5", alpha=0.3)

plt.axhline(y=np.average((1 - y2 / y1) * 100), color='0.0', linestyle='--', linewidth=0.8, label='Average \\%')
plt.text(x=0.5, y=21, s="Average: {:.2f}\\%".format(np.average((1 - y2 / y1) * 100)))
plt.legend(loc='upper left', fontsize=12)

plt.ylabel('Optimized \\%')
plt.xlabel('Benchmarks')

plt.savefig('opt.pdf', bbox_inches='tight')
