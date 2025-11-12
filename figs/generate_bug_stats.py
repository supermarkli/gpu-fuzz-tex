#!/usr/bin/env python3
"""
生成Bug统计可视化图表
用于GPU-Fuzz论文的Evaluation章节
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体（如果需要）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Bug数据（基于论文表格，共13个bug）
# poc8/9合并为Bug₈
bug_data = {
    'frameworks': {
        'PyTorch': 7,  # Bug₁(poc1), Bug₂(poc2), Bug₅(poc5), Bug₆(poc6), Bug₇(poc7), Bug₁₂(poc14), Bug₁₃(poc15)
        'TensorFlow': 2,  # Bug₈(poc8/9), Bug₉(poc11)
        'PaddlePaddle': 4  # Bug₃(poc3), Bug₄(poc4), Bug₁₀(poc12), Bug₁₁(poc13)
    },
    'error_types': {
        'Silent Memory Corruption': 6,  # Bug₂(poc2), Bug₅(poc5), Bug₆(poc6), Bug₇(poc7), Bug₈(poc8), Bug₁₂(poc14)
        'GPU-Level Exception': 5,  # Bug₁(poc1), Bug₄(poc4), Bug₁₀(poc12), Bug₁₁(poc13), Bug₁₃(poc15)
        'CPU-Side Assert': 2  # Bug₃(poc3), Bug₉(poc11)
    },
    'operators': {
        'ConvTranspose': 6,  # Bug₁(poc1), Bug₃(poc3), Bug₄(poc4), Bug₁₀(poc12), Bug₁₁(poc13), Bug₁₂(poc14)
        'Conv': 2,  # Bug₈(poc8/9), Bug₉(poc11)
        'Pooling': 2,  # Bug₅(poc5), Bug₇(poc7)
        'Padding': 2  # Bug₆(poc6), Bug₁₃(poc15)
    }
}

def plot_bug_by_framework():
    """按框架分布的柱状图"""
    fig, ax = plt.subplots(figsize=(6, 4))
    frameworks = list(bug_data['frameworks'].keys())
    counts = list(bug_data['frameworks'].values())
    colors = ['#404040', '#808080', '#C0C0C0']  # 深灰、中灰、浅灰
    
    bars = ax.bar(frameworks, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2, width=0.3)
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=14)
    
    ax.set_ylabel('Number of Bugs', fontsize=14)
    ax.set_ylim(0, max(counts) * 1.2)
    ax.tick_params(axis='x', labelsize=14)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('bug_by_framework.pdf', dpi=300, bbox_inches='tight')
    print("Saved: bug_by_framework.pdf")

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

def plot_bug_by_operator():
    """按操作符类型分布的柱状图"""
    fig, ax = plt.subplots(figsize=(6, 4))
    operators = list(bug_data['operators'].keys())
    counts = list(bug_data['operators'].values())
    colors = ['#2C2C2C', '#5C5C5C', '#8C8C8C', '#B8B8B8']  # 深灰到浅灰的渐变
    
    bars = ax.bar(operators, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2, width=0.3)
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=14)
    
    ax.set_ylabel('Number of Bugs', fontsize=14)
    ax.set_ylim(0, max(counts) * 1.3)
    ax.tick_params(axis='x', labelsize=14)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('bug_by_operator.pdf', dpi=300, bbox_inches='tight')
    print("Saved: bug_by_operator.pdf")

def plot_combined():
    """生成包含三个子图的组合图：第一行居中饼图，第二行两个柱状图"""
    fig = plt.figure(figsize=(12, 6))
    
    # 子图1: 按错误类型分布（第一行居中）
    ax1 = plt.subplot(2, 2, (1, 2))
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
    colors = ['#2C2C2C', '#6C6C6C', '#B0B0B0']
    explode = (0.05, 0.05, 0.1)
    wedges, texts, autotexts = ax1.pie(counts, labels=error_types_labels, autopct='%1.1f%%',
                                       colors=colors, explode=explode, startangle=90,
                                       textprops={'fontsize': 11})
    for i, autotext in enumerate(autotexts):
        if i < 2:
            autotext.set_color('white')
        else:
            autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    ax1.set_title('(a) By Error Type', fontsize=12, fontweight='bold', pad=15)
    
    # 子图2: 按框架分布（第二行左）
    ax2 = plt.subplot(2, 2, 3)
    frameworks = list(bug_data['frameworks'].keys())
    counts = list(bug_data['frameworks'].values())
    colors = ['#404040', '#808080', '#C0C0C0']
    bars = ax2.bar(frameworks, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2, width=0.5)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Number of Bugs', fontsize=11)
    ax2.set_xlabel('Framework', fontsize=11)
    ax2.set_title('(b) By Framework', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, max(counts) * 1.2)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 子图3: 按操作符类型分布（第二行右）
    ax3 = plt.subplot(2, 2, 4)
    operators = list(bug_data['operators'].keys())
    counts = list(bug_data['operators'].values())
    colors = ['#2C2C2C', '#5C5C5C', '#8C8C8C', '#B8B8B8']
    bars = ax3.bar(operators, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2, width=0.5)
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Number of Bugs', fontsize=11)
    ax3.set_xlabel('Operator Type', fontsize=11)
    ax3.set_title('(c) By Operator Type', fontsize=12, fontweight='bold')
    ax3.set_ylim(0, max(counts) * 1.3)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.close()

if __name__ == '__main__':
    print("Generating bug statistics plots...")
    plot_bug_by_framework()
    plot_bug_by_error_type()
    plot_bug_by_operator()
    plot_combined()
    print("All plots generated!")

