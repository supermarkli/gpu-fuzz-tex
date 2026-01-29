#!/usr/bin/env python3
"""
对比分析NNSmith和GPU-Fuzz的fuzzing结果
用于论文的Evaluation章节
"""

import os
import re
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 设置字体
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False

def analyze_gpufuzz_logs(log_dir):
    """分析GPU-Fuzz的日志文件
    
    注意：根据源码分析（controller.py和model_gen.py）：
    - 每个日志文件（log{errid}.txt）对应一次model_gen.py的执行
    - 每次model_gen.py执行会生成多个测试用例（通过while循环）
    - 每个测试用例执行时会打印mat_shapes（格式为[[...]]）
    - 因此，应该统计trace.txt中[[...]]的数量作为实际测试用例数
    """
    log_path = Path(log_dir)
    if not log_path.exists():
        print(f"Warning: {log_dir} does not exist")
        return {}
    
    stats = {
        'total_logs': 0,  # 日志文件数（log*.txt）
        'total_testcases': 0,  # 实际测试用例数（trace.txt中[[...]]的数量）
        'logs_with_errors': 0,
        'memory_errors': 0,  # Invalid write/read
        'config_errors': 0,  # cudaErrorInvalidConfiguration
        'oom_errors': 0,  # cudaErrorMemoryAllocation
        'other_errors': 0,
        'unique_bugs': set()  # 用于去重
    }
    
    # 统计实际测试用例数（从trace.txt中统计[[...]]的数量）
    trace_file = log_path / "trace.txt"
    if trace_file.exists():
        try:
            with open(trace_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # 统计[[...]]的数量，这是每个测试用例执行时打印的mat_shapes
                testcase_pattern = r'^\[\[.*?\]\]'
                matches = re.findall(testcase_pattern, content, re.MULTILINE)
                stats['total_testcases'] = len(matches)
        except Exception as e:
            print(f"Error reading trace.txt: {e}")
    
    # 统计错误类型
    error_patterns = {
        'memory_errors': [
            r'Invalid __global__ write',
            r'Invalid __global__ read',
            r'Invalid __shared__ write',
            r'Invalid __shared__ read',
            r'out of bounds',
            r'misaligned'
        ],
        'config_errors': [
            r'cudaErrorInvalidConfiguration',
            r'invalid configuration argument'
        ],
        'oom_errors': [
            r'cudaErrorMemoryAllocation',
            r'out of memory'
        ]
    }
    
    for log_file in sorted(log_path.glob('*.txt')):
        stats['total_logs'] += 1
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # 检查是否有错误（排除只有COMPUTE-SANITIZER头部的情况）
            if len(content) > 100:  # 大于100字节说明有实际内容
                has_error = False
                bug_signature = []
                
                # 检查各种错误类型
                for error_type, patterns in error_patterns.items():
                    for pattern in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            has_error = True
                            bug_signature.append(f"{error_type}:{pattern}")
                            if error_type == 'memory_errors':
                                stats['memory_errors'] += 1
                            elif error_type == 'config_errors':
                                stats['config_errors'] += 1
                            elif error_type == 'oom_errors':
                                stats['oom_errors'] += 1
                            break
                    if has_error:
                        break
                
                # 检查其他错误
                if has_error:
                    stats['logs_with_errors'] += 1
                    # 创建bug签名用于去重
                    signature = '|'.join(sorted(bug_signature))
                    stats['unique_bugs'].add(signature)
                elif 'ERROR SUMMARY' in content or 'error' in content.lower():
                    stats['other_errors'] += 1
                    stats['logs_with_errors'] += 1
        except Exception as e:
            print(f"Error reading {log_file}: {e}")
    
    stats['unique_bug_count'] = len(stats['unique_bugs'])
    return stats

def analyze_nnsmith_results(bug_dir, log_file):
    """分析NNSmith的结果"""
    stats = {
        'total_bugs': 0,
        'total_testcases': 0,
        'failed_testcases': 0,
        'bug_types': {},
        'runtime_hours': 0
    }
    
    # 统计bug目录
    bug_path = Path(bug_dir)
    if bug_path.exists():
        bug_dirs = list(bug_path.glob('bug-*'))
        stats['total_bugs'] = len(bug_dirs)
        
        # 统计bug类型
        for bug_dir in bug_dirs:
            bug_name = bug_dir.name
            # 提取Symptom类型
            match = re.search(r'Symptom\.([^-]+)', bug_name)
            if match:
                bug_type = match.group(1)
                stats['bug_types'][bug_type] = stats['bug_types'].get(bug_type, 0) + 1
    
    # 从日志文件提取统计信息
    log_path = Path(log_file)
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # 提取测试用例数量
            match = re.search(r'Total (\d+) testcases generated', content)
            if match:
                stats['total_testcases'] = int(match.group(1))
            
            # 提取bug数量
            match = re.search(r'Total (\d+) bugs found', content)
            if match:
                stats['total_bugs'] = int(match.group(1))
            
            # 提取失败数量
            match = re.search(r'Total (\d+) failed to make testcases', content)
            if match:
                stats['failed_testcases'] = int(match.group(1))
            
            # 提取运行时间（从日志时间戳推断）
            time_matches = re.findall(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', content)
            if len(time_matches) >= 2:
                from datetime import datetime
                start_time = datetime.strptime(time_matches[0], '%Y-%m-%d %H:%M:%S')
                end_time = datetime.strptime(time_matches[-1], '%Y-%m-%d %H:%M:%S')
                delta = end_time - start_time
                stats['runtime_hours'] = delta.total_seconds() / 3600.0
        except Exception as e:
            print(f"Error reading log file: {e}")
    
    return stats

def plot_comparison(nnsmith_stats, gpufuzz_stats):
    """生成对比图表（仅饼图）"""
    
    # Bug类型分布对比（饼图）
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # NNSmith的bug类型（饼图）
    ax1 = axes[0]
    nnsmith_types = list(nnsmith_stats['bug_types'].keys())
    nnsmith_counts = list(nnsmith_stats['bug_types'].values())
    colors_nn = ['#808080', '#A0A0A0', '#C0C0C0', '#E0E0E0']
    
    if nnsmith_counts:
        wedges, texts, autotexts = ax1.pie(nnsmith_counts, labels=nnsmith_types, 
                                           colors=colors_nn[:len(nnsmith_types)],
                                           autopct='%1.1f%%', startangle=90,
                                           textprops={'fontsize': 12, 'fontweight': 'bold'},
                                           edgecolor='black', linewidth=1.2)
        ax1.set_title('NNSmith: Bug Types', fontsize=14, fontweight='bold', pad=10)
    else:
        ax1.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)
        ax1.set_title('NNSmith: Bug Types', fontsize=14, fontweight='bold', pad=10)
    
    # GPU-Fuzz的错误类型（饼图）
    ax2 = axes[1]
    gpufuzz_types = ['Memory Errors', 'Config Errors']
    gpufuzz_counts = [gpufuzz_stats['memory_errors'], gpufuzz_stats['config_errors']]
    colors_gf = ['#404040', '#606060']
    
    # 过滤掉为0的项
    filtered_types = []
    filtered_counts = []
    filtered_colors = []
    for i, count in enumerate(gpufuzz_counts):
        if count > 0:
            filtered_types.append(gpufuzz_types[i])
            filtered_counts.append(count)
            filtered_colors.append(colors_gf[i])
    
    if filtered_counts:
        wedges, texts, autotexts = ax2.pie(filtered_counts, labels=filtered_types,
                                           colors=filtered_colors,
                                           autopct='%1.1f%%', startangle=90,
                                           textprops={'fontsize': 12, 'fontweight': 'bold'},
                                           edgecolor='black', linewidth=1.2)
        ax2.set_title('GPU-Fuzz: Error Types', fontsize=14, fontweight='bold', pad=10)
    else:
        ax2.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)
        ax2.set_title('GPU-Fuzz: Error Types', fontsize=14, fontweight='bold', pad=10)
    
    plt.tight_layout()
    plt.savefig('bug_types_comparison.pdf', dpi=300, bbox_inches='tight')
    print("Saved: bug_types_comparison.pdf")
    plt.close()

def print_summary(nnsmith_stats, gpufuzz_stats):
    """打印统计摘要"""
    print("\n" + "="*60)
    print("FUZZING RESULTS COMPARISON")
    print("="*60)
    
    print("\n--- NNSmith Results ---")
    print(f"Total Bugs Found: {nnsmith_stats['total_bugs']}")
    print(f"Total Test Cases: {nnsmith_stats['total_testcases']}")
    print(f"Failed Test Cases: {nnsmith_stats['failed_testcases']}")
    print(f"Bug Types: {nnsmith_stats['bug_types']}")
    if nnsmith_stats['total_testcases'] > 0:
        print(f"Bug Discovery Rate: {nnsmith_stats['total_bugs']/nnsmith_stats['total_testcases']*1000:.2f} bugs per 1000 testcases")
    
    print("\n--- GPU-Fuzz Results ---")
    print(f"Total Log Files: {gpufuzz_stats['total_logs']}")
    print(f"Total Test Cases: {gpufuzz_stats['total_testcases']} (from trace.txt)")
    print(f"Logs with Errors: {gpufuzz_stats['logs_with_errors']}")
    print(f"Memory Errors (Critical): {gpufuzz_stats['memory_errors']}")
    print(f"Configuration Errors: {gpufuzz_stats['config_errors']}")
    print(f"OOM Errors (excluded): {gpufuzz_stats['oom_errors']}")
    print(f"Unique Bug Signatures: {gpufuzz_stats['unique_bug_count']}")
    
    gpufuzz_real_bugs = gpufuzz_stats['memory_errors'] + gpufuzz_stats['config_errors']
    if gpufuzz_stats['total_testcases'] > 0:
        print(f"Bug Discovery Rate: {gpufuzz_real_bugs/gpufuzz_stats['total_testcases']*1000:.2f} bugs per 1000 testcases")
    if gpufuzz_stats['total_logs'] > 0:
        print(f"Average Test Cases per Log: {gpufuzz_stats['total_testcases']/gpufuzz_stats['total_logs']:.1f}")
    
    print("\n--- Key Insights ---")
    print(f"GPU-Fuzz found {gpufuzz_real_bugs} real bugs (excluding OOM)")
    print(f"NNSmith found {nnsmith_stats['total_bugs']} bugs")
    print(f"GPU-Fuzz memory errors: {gpufuzz_stats['memory_errors']}")
    print(f"NNSmith INCONSISTENCY bugs: {nnsmith_stats['bug_types'].get('INCONSISTENCY', 0)}")
    print("="*60 + "\n")

if __name__ == '__main__':
    # 路径配置
    nnsmith_bug_dir = '/home/lzh/projects/nnsmithout/pytorch8'
    nnsmith_log_file = '/home/lzh/projects/nnsmithout/outputs/2025-11-06/21-40-49/fuzz.log'
    gpufuzz_log_dir = '/home/lzh/projects/gpu_fuzz/gpu_logs/log20251101'
    
    print("Analyzing NNSmith results...")
    nnsmith_stats = analyze_nnsmith_results(nnsmith_bug_dir, nnsmith_log_file)
    
    print("Analyzing GPU-Fuzz results...")
    gpufuzz_stats = analyze_gpufuzz_logs(gpufuzz_log_dir)
    
    print_summary(nnsmith_stats, gpufuzz_stats)
    
    print("Generating comparison plots...")
    plot_comparison(nnsmith_stats, gpufuzz_stats)
    
    print("\nAnalysis complete!")

