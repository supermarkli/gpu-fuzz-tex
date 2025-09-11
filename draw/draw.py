from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
from csv import reader
import numpy as np

matplotlib.use('qtagg')

reader = reader(open('data.csv', 'r'))
status = "HEADER"

table = {"header": None, "data": []}
for row in reader:
    row = [x.strip() for x in row]
    row = list(filter(lambda x: x != '', row))
    row = [x.split()[0] for x in row]

    if status == "HEADER":
        status = "DATA"
        table["header"] = row
    elif status == "DATA" and len(row) > 0:
        table["data"].append(row)
    elif status == "DATA" and len(row) == 0:
        status = "HEADER"
        break

xticks = np.array(range(0, len(table["header"]) - 1))

x = table["header"]
y_list = np.array([[float(row[i]) for i in range(1, len(row))] for row in table["data"]])

plt.figure(figsize=(20, 3))
cs = plt.get_cmap('gray', 3)
matplotlib.rcParams.update({
    "text.usetex": True,
    "font.size": 15,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "axes.unicode_minus": False  # 让负号正常显示
})
plt.yscale('log')
plt.bar(xticks - 0.3, y_list[0] / y_list[0], label='\\textbf{baseline}', width=0.2, color='0.3')
plt.bar(xticks, y_list[1] / y_list[0], label='\\textbf{\\textsc{CuSan}}', width=0.2, color='0.5')
plt.bar(xticks + 0.3, y_list[2] / y_list[0], label='\\textbf{compute-sanitizer}', width=0.2, color='0.8')

plt.text(x=-0.4, y=0.64, s="\\textbf{Tango}", ha='left', va='top',
         fontsize=12, transform=plt.gca().get_xaxis_transform())
plt.axvline(x=5.5, color='black', linestyle='--', linewidth=0.8)
plt.text(x=5.6, y=0.64, s="\\textbf{Rodinia}", ha='left', va='top',
         fontsize=12, transform=plt.gca().get_xaxis_transform())
plt.axvline(x=22.5, color='black', linestyle='--', linewidth=0.8)
plt.text(x=22.6, y=0.64, s="\\textbf{PolyBench}", ha='left', va='top',
         fontsize=12, transform=plt.gca().get_xaxis_transform())
plt.axvline(x=41.5, color='black', linestyle='--', linewidth=0.8)
plt.text(x=41.6, y=0.64, s="\\textbf{LLaMA}", ha='left', va='top',
         fontsize=12, transform=plt.gca().get_xaxis_transform())

plt.xticks(xticks, labels=table["header"][1:], rotation=30, ha='right')
plt.xlim(-0.5, len(table["header"]) - 1 - 0.5)
plt.legend(fontsize=12)

plt.ylabel('Execution time (s)\n($\\leftarrow$ is better)', fontsize=15)
ylim = plt.ylim()
ax = plt.twinx()
ax.set_ylim(ylim)
ax.set_ylabel('Throughput (tokens/s)\n($\\rightarrow$ better)', fontsize=15)
ax.set_yscale('log')

plt.savefig('draw.pdf', dpi=300, bbox_inches='tight')
