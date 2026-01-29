#!/usr/bin/env python3
"""
生成Bug统计可视化图表
用于GPU-Fuzz论文的Evaluation章节
"""

import matplotlib.pyplot as plt

# 设置字体为 Times New Roman（如果不可用，使用 TeX Gyre Pagella 作为替代）
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'TeX Gyre Pagella', 'DejaVu Serif', 'Noto Serif']
plt.rcParams['axes.unicode_minus'] = False

# Bug数据（基于论文表格，共13个bug）
# poc8/9合并为Bug₈
bug_data = {
    'error_types': {
        'Silent Memory Corruption': 6,  # Bug₂(poc2), Bug₅(poc5), Bug₆(poc6), Bug₇(poc7), Bug₈(poc8), Bug₁₂(poc14)
        'GPU-Level Exception': 5,  # Bug₁(poc1), Bug₄(poc4), Bug₁₀(poc12), Bug₁₁(poc13), Bug₁₃(poc15)
        'CPU-Side Assert': 2  # Bug₃(poc3), Bug₉(poc11)
    }
}

def plot_bug_by_error_type():
    """按错误类型分布的饼图"""
    fig, ax = plt.subplots(figsize=(7, 5))
    error_types = list(bug_data['error_types'].keys())
    # 对长标签进行换行处理
    error_types_labels = []
    for label in error_types:
        if label == 'Silent Memory Corruption':
            error_types_labels.append('Silent Memory\nCorruption')
        elif label == 'GPU-Level Exception':
            error_types_labels.append('GPU-Level\nException')
        else:
            error_types_labels.append(label)
    
    counts = list(bug_data['error_types'].values())
    colors = ['#2C2C2C', '#6C6C6C', '#B0B0B0']  # 深灰、中灰、浅灰
    explode = (0.05, 0.05, 0.1)  # 突出显示CPU-Side Assert
    
    wedges, texts, autotexts = ax.pie(counts, labels=error_types_labels, autopct='%1.1f%%',
                                       colors=colors, explode=explode, startangle=90,
                                       textprops={'fontsize': 15})
    
    # 显式设置所有文本元素的字体大小
    for text in texts:
        text.set_fontsize(15)
    
    # 增强文本显示 - 根据背景颜色调整文字颜色
    for i, autotext in enumerate(autotexts):
        # 深灰色背景用白色文字，浅灰色背景用黑色文字
        if i < 2:  # 前两个是深灰和中灰
            autotext.set_color('white')
        else:  # 最后一个是浅灰
            autotext.set_color('black')
        autotext.set_fontsize(15)
    
    plt.tight_layout()
    plt.savefig('bug_by_error_type.pdf', dpi=300, bbox_inches='tight')
    print("Saved: bug_by_error_type.pdf")

if __name__ == '__main__':
    print("Generating bug statistics plot...")
    plot_bug_by_error_type()
    print("Plot generated!")

