import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    "text.usetex": True,
    "font.size": 12,
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "axes.unicode_minus": False  # 让负号正常显示
})

reader = csv.reader(open('mem.csv', 'r'))
rows = []
max_abs = [(0, "")] * 3
max_per = [(0, "")] * 3

total = [0] * 4

for row in reader:
    print(row)
    if len(row) < 5:
        continue
    name = row[0]
    row = [float(c) for c in row[1:]]
    for i in range(1, 4):
        print(row[i])
        if row[i] - row[0] > max_abs[i - 1][0]:
            max_abs[i - 1] = (row[i] - row[0], name)

        if row[i] / row[0] > max_per[i - 1][0]:
            max_per[i - 1] = (row[i] / row[0], name)

    for i in range(4):
        total[i] += row[i]

for i in range(3):
    print(f"Max absolute difference for column {i + 2}: {max_abs[i][0]} in {max_abs[i][1]}")
    print(f"Max percentage difference for column {i + 2}: {max_per[i][0]} in {max_per[i][1]}")
