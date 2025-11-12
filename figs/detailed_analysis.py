#!/usr/bin/env python3
"""
详细的对比分析脚本
生成更多有用的图表用于论文
"""

import os
import re
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# 设置字体和样式
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

def parse_nnsmith_timeline(log_file):
    """解析NNSmith日志，提取bug发现时间线"""
    timeline = []
    bug_count = 0
    
    log_path = Path(log_file)
    if not log_path.exists():
        return timeline
    
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # 查找bug相关的日志
                if 'bug' in line.lower() or 'error' in line.lower():
                    # 提取时间戳
                    time_match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                    if time_match:
                        try:
                            timestamp = datetime.strptime(time_match.group(1), '%Y-%m-%d %H:%M:%S')
                            bug_count += 1
                            timeline.append((timestamp, bug_count))
                        except:
                            pass
    except Exception as e:
        print(f"Error parsing NNSmith timeline: {e}")
    
    return timeline

def parse_gpufuzz_timeline(log_dir):
    """解析GPU-Fuzz日志，提取bug发现时间线"""
    timeline = []
    bug_count = 0
    
    log_path = Path(log_dir)
    if not log_path.exists():
        return timeline
    
    # 按文件名排序（假设文件名包含序号）
    log_files = sorted(log_path.glob('log*.txt'), key=lambda x: int(re.search(r'(\d+)', x.name).group(1)) if re.search(r'(\d+)', x.name) else 0)
    
    error_patterns = [
        r'Invalid __global__ write',
        r'Invalid __global__ read',
        r'Invalid __shared__ write',
        r'Invalid __shared__ read',
        r'cudaErrorInvalidConfiguration'
    ]
    
    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # 检查是否有真实错误（排除OOM）
            has_real_error = False
            for pattern in error_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    has_real_error = True
                    break
            
            if has_real_error:
                bug_count += 1
                # 使用文件修改时间作为时间戳（近似）
                timestamp = datetime.fromtimestamp(log_file.stat().st_mtime)
                timeline.append((timestamp, bug_count))
        except Exception as e:
            pass
    
    return timeline

def plot_bug_discovery_timeline(nnsmith_timeline, gpufuzz_timeline):
    """绘制bug发现时间线"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 归一化时间到0-4小时
    if nnsmith_timeline:
        start_time = nnsmith_timeline[0][0]
        nnsmith_x = [(t - start_time).total_seconds() / 3600.0 for t, _ in nnsmith_timeline]
        nnsmith_y = [count for _, count in nnsmith_timeline]
    else:
        nnsmith_x, nnsmith_y = [], []
    
    if gpufuzz_timeline:
        start_time = gpufuzz_timeline[0][0]
        gpufuzz_x = [(t - start_time).total_seconds() / 3600.0 for t, _ in gpufuzz_timeline]
        gpufuzz_y = [count for _, count in gpufuzz_timeline]
    else:
        gpufuzz_x, gpufuzz_y = [], []
    
    # 绘制曲线
    if nnsmith_x:
        ax.plot(nnsmith_x, nnsmith_y, label='NNSmith', linewidth=2, color='#808080', marker='o', markersize=3)
    if gpufuzz_x:
        ax.plot(gpufuzz_x, gpufuzz_y, label='GPU-Fuzz', linewidth=2, color='#404040', marker='s', markersize=3)
    
    ax.set_xlabel('Time (hours)', fontsize=12)
    ax.set_ylabel('Cumulative Bugs Found', fontsize=12)
    ax.set_title('Bug Discovery Timeline', fontsize=14, fontweight='bold', pad=10)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(left=0)
    
    plt.tight_layout()
    plt.savefig('bug_discovery_timeline.pdf', dpi=300, bbox_inches='tight')
    print("Saved: bug_discovery_timeline.pdf")
    plt.close()

def plot_bug_severity_comparison(nnsmith_stats, gpufuzz_stats):
    """绘制bug严重程度对比"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 分类bug严重程度
    categories = ['Critical\n(Memory Errors)', 'High\n(Config Errors)', 'Medium\n(Inconsistency)', 'Low\n(Other)']
    
    # NNSmith: INCONSISTENCY算Medium，EXCEPTION算Low
    nnsmith_counts = [
        0,  # Critical
        0,  # High
        nnsmith_stats['bug_types'].get('INCONSISTENCY', 0),  # Medium
        nnsmith_stats['bug_types'].get('EXCEPTION', 0)  # Low
    ]
    
    # GPU-Fuzz: Memory errors算Critical，Config errors算High
    gpufuzz_counts = [
        gpufuzz_stats['memory_errors'],  # Critical
        gpufuzz_stats['config_errors'],  # High
        0,  # Medium
        0   # Low
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, nnsmith_counts, width, label='NNSmith', 
                   color='#808080', alpha=0.8, edgecolor='black', linewidth=1.2)
    bars2 = ax.bar(x + width/2, gpufuzz_counts, width, label='GPU-Fuzz', 
                   color='#404040', alpha=0.8, edgecolor='black', linewidth=1.2)
    
    # 添加数值标签
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_ylabel('Number of Bugs', fontsize=12)
    ax.set_title('Bug Severity Distribution', fontsize=14, fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('bug_severity_comparison.pdf', dpi=300, bbox_inches='tight')
    print("Saved: bug_severity_comparison.pdf")
    plt.close()

def plot_test_case_efficiency(nnsmith_stats, gpufuzz_stats):
    """绘制测试用例效率对比"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    tools = ['NNSmith', 'GPU-Fuzz']
    
    # 计算每个测试用例发现的bug数
    nnsmith_efficiency = nnsmith_stats['total_bugs'] / nnsmith_stats['total_testcases'] if nnsmith_stats['total_testcases'] > 0 else 0
    gpufuzz_real_bugs = gpufuzz_stats['memory_errors'] + gpufuzz_stats['config_errors']
    # 使用实际测试用例数，不是日志文件数
    gpufuzz_efficiency = gpufuzz_real_bugs / gpufuzz_stats['total_testcases'] if gpufuzz_stats['total_testcases'] > 0 else 0
    
    efficiencies = [nnsmith_efficiency, gpufuzz_efficiency]
    colors = ['#808080', '#404040']
    
    bars = ax.bar(tools, efficiencies, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5, width=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{height:.3f}', ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.set_ylabel('Bugs per Test Case', fontsize=12)
    ax.set_title('Test Case Efficiency', fontsize=14, fontweight='bold', pad=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(efficiencies) * 1.2)
    
    plt.tight_layout()
    plt.savefig('test_case_efficiency.pdf', dpi=300, bbox_inches='tight')
    print("Saved: test_case_efficiency.pdf")
    plt.close()

def analyze_memory_errors_detail(log_dir):
    """详细分析内存错误"""
    log_path = Path(log_dir)
    if not log_path.exists():
        return {}
    
    stats = {
        'invalid_global_write': 0,
        'invalid_global_read': 0,
        'invalid_shared_write': 0,
        'invalid_shared_read': 0,
        'operators': {}
    }
    
    patterns = {
        'invalid_global_write': r'Invalid __global__ write',
        'invalid_global_read': r'Invalid __global__ read',
        'invalid_shared_write': r'Invalid __shared__ write',
        'invalid_shared_read': r'Invalid __shared__ read'
    }
    
    operator_pattern = r'at::native::.*?::(\w+)'
    
    for log_file in log_path.glob('*.txt'):
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            for error_type, pattern in patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    stats[error_type] += 1
                    
                    # 提取算子名称
                    op_match = re.search(operator_pattern, content)
                    if op_match:
                        op_name = op_match.group(1)
                        stats['operators'][op_name] = stats['operators'].get(op_name, 0) + 1
                    break
        except:
            pass
    
    return stats

def plot_memory_error_details(memory_stats):
    """绘制内存错误详细分析"""
    if not memory_stats or sum([memory_stats.get(k, 0) for k in ['invalid_global_write', 'invalid_global_read', 'invalid_shared_write', 'invalid_shared_read']]) == 0:
        print("No memory errors to plot")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 子图1: 错误类型分布
    ax1 = axes[0]
    error_types = ['Global Write', 'Global Read', 'Shared Write', 'Shared Read']
    error_counts = [
        memory_stats.get('invalid_global_write', 0),
        memory_stats.get('invalid_global_read', 0),
        memory_stats.get('invalid_shared_write', 0),
        memory_stats.get('invalid_shared_read', 0)
    ]
    
    # 过滤掉0值
    filtered_types = [t for t, c in zip(error_types, error_counts) if c > 0]
    filtered_counts = [c for c in error_counts if c > 0]
    
    colors = ['#2C2C2C', '#4C4C4C', '#6C6C6C', '#8C8C8C']
    bars = ax1.bar(filtered_types, filtered_counts, color=colors[:len(filtered_types)], 
                   alpha=0.8, edgecolor='black', linewidth=1.2)
    
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax1.set_ylabel('Number of Errors', fontsize=12)
    ax1.set_title('(a) Memory Error Types', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 子图2: 涉及的算子（如果有数据）
    ax2 = axes[1]
    if memory_stats.get('operators'):
        operators = list(memory_stats['operators'].keys())[:10]  # 最多显示10个
        op_counts = [memory_stats['operators'][op] for op in operators]
        
        bars = ax2.barh(operators, op_counts, color='#404040', alpha=0.8, edgecolor='black', linewidth=1.2)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2.,
                    f'{int(width)}', ha='left', va='center', fontsize=10, fontweight='bold')
        
        ax2.set_xlabel('Number of Errors', fontsize=12)
        ax2.set_title('(b) Affected Operators', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3, linestyle='--')
    else:
        ax2.text(0.5, 0.5, 'No operator data available', 
                ha='center', va='center', transform=ax2.transAxes, fontsize=12)
        ax2.set_title('(b) Affected Operators', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('memory_error_details.pdf', dpi=300, bbox_inches='tight')
    print("Saved: memory_error_details.pdf")
    plt.close()

if __name__ == '__main__':
    from compare_nnsmith_gpufuzz import analyze_nnsmith_results, analyze_gpufuzz_logs
    
    # 路径配置
    nnsmith_bug_dir = '/home/lzh/projects/nnsmithout/pytorch8'
    nnsmith_log_file = '/home/lzh/projects/nnsmithout/outputs/2025-11-06/21-40-49/fuzz.log'
    gpufuzz_log_dir = '/home/lzh/projects/gpu_fuzz/gpu_logs/log20251101'
    
    print("Analyzing data...")
    nnsmith_stats = analyze_nnsmith_results(nnsmith_bug_dir, nnsmith_log_file)
    gpufuzz_stats = analyze_gpufuzz_logs(gpufuzz_log_dir)
    
    print("Generating detailed plots...")
    
    # 解析时间线
    print("  - Parsing timelines...")
    nnsmith_timeline = parse_nnsmith_timeline(nnsmith_log_file)
    gpufuzz_timeline = parse_gpufuzz_timeline(gpufuzz_log_dir)
    
    # 生成图表
    print("  - Plotting bug discovery timeline...")
    plot_bug_discovery_timeline(nnsmith_timeline, gpufuzz_timeline)
    
    print("  - Plotting bug severity comparison...")
    plot_bug_severity_comparison(nnsmith_stats, gpufuzz_stats)
    
    print("  - Plotting test case efficiency...")
    plot_test_case_efficiency(nnsmith_stats, gpufuzz_stats)
    
    print("  - Analyzing memory error details...")
    memory_stats = analyze_memory_errors_detail(gpufuzz_log_dir)
    plot_memory_error_details(memory_stats)
    
    print("\nAll detailed plots generated!")

