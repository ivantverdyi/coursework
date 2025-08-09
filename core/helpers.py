import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def load_results():
    results = {}

    files = {
        'sync': '../results/result_sync.json',
        'threads': '../results/result_sync_threads.json',
        'async': '../results/result_async_asyncio.json'
    }

    for method, filepath in files.items():
        try:
            with open(filepath, 'r') as f:
                results[method] = json.load(f)
            print(f"Loaded {method} results successfully")
        except FileNotFoundError:
            print(f"Warning: {filepath} not found")
            results[method] = None

    return results


def calculate_metrics(results):
    metrics = {}

    for method, data in results.items():
        if data is None:
            continue

        individual_times = data.get('individual_times', [])

        if method == 'sync':
            workers = 1
        elif method == 'threads':
            workers = 4
        else:
            workers = 100

        metrics[method] = {
            'total_time': data.get('total_time', 0),
            'avg_response_time': np.mean(individual_times),
            'median_response_time': np.median(individual_times),
            'min_response_time': np.min(individual_times),
            'max_response_time': np.max(individual_times),
            'std_response_time': np.std(individual_times),
            'successful_requests': data.get('count_success', 0),
            'failed_requests': data.get('count_failed', 0),
            'success_rate': data.get('count_success', 0) / (
                    data.get('count_success', 0) + data.get('count_failed', 0)) * 100,
            'throughput': data.get('count_success', 0) / data.get('total_time', 1),
        }

    return metrics


def create_total_time_plot(metrics):
    """Create and save total execution time plot"""
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots(figsize=(8, 5))

    # Define colors
    colors = {'sync': '#FF6B6B', 'threads': '#4ECDC4', 'async': '#45B7D1'}
    method_names = {'sync': 'Синхронний', 'threads': 'Потоки', 'async': 'Asyncio'}

    methods = list(metrics.keys())
    total_times = [metrics[method]['total_time'] for method in methods]
    method_labels = [method_names[method] for method in methods]

    bars = ax.bar(method_labels, total_times, color=[colors[m] for m in methods])
    ax.set_title('Загальний час виконання', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Час (секунди)', fontsize=12)
    ax.set_xlabel('Метод', fontsize=12)

    # Add value labels on bars
    for bar, time in zip(bars, total_times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{time:.2f}s', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Improve layout
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/total_time_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()


def create_throughput_plot(metrics):
    """Create and save throughput plot"""
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots(figsize=(8, 5))

    # Define colors
    colors = {'sync': '#FF6B6B', 'threads': '#4ECDC4', 'async': '#45B7D1'}
    method_names = {'sync': 'Синхронний', 'threads': 'Потоки', 'async': 'Asyncio'}

    methods = list(metrics.keys())
    throughputs = [metrics[method]['throughput'] for method in methods]
    method_labels = [method_names[method] for method in methods]

    bars = ax.bar(method_labels, throughputs, color=[colors[m] for m in methods])
    ax.set_title('Пропускна здатність', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Запитів за секунду', fontsize=12)
    ax.set_xlabel('Метод', fontsize=12)

    # Add value labels on bars
    for bar, throughput in zip(bars, throughputs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{throughput:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Improve layout
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/throughput_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()


def create_improvement_plot(metrics):
    """Create and save improvement percentage plot"""
    if 'sync' not in metrics:
        print("Warning: sync method not found, cannot calculate improvements")
        return

    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots(figsize=(8, 5))

    # Define colors
    colors = {'sync': '#FF6B6B', 'threads': '#4ECDC4', 'async': '#45B7D1'}
    method_names = {'sync': 'Синхронний', 'threads': 'Потоки', 'async': 'Asyncio'}

    sync_time = metrics['sync']['total_time']
    improvements = []
    improvement_labels = []
    bar_colors = []

    for method in metrics.keys():
        if method != 'sync':
            improvement = (sync_time - metrics[method]['total_time']) / sync_time * 100
            improvements.append(improvement)
            improvement_labels.append(method_names[method])
            bar_colors.append(colors[method])

    bars = ax.bar(improvement_labels, improvements, color=bar_colors)
    ax.set_title('Покращення відносно синхронного методу', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Покращення (%)', fontsize=12)
    ax.set_xlabel('Метод', fontsize=12)

    # Add value labels on bars
    for bar, imp in zip(bars, improvements):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{imp:.1f}%', ha='center', va='bottom' if imp > 0 else 'top',
                fontsize=11, fontweight='bold')

    # Improve layout
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/improvement_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()


def create_comprehensive_plots(results, metrics):
    """Create all three plots as separate images"""
    print("Creating total execution time plot...")
    create_total_time_plot(metrics)

    print("Creating throughput plot...")
    create_throughput_plot(metrics)

    print("Creating improvement plot...")
    create_improvement_plot(metrics)

    print("All plots saved successfully!")


def create_response_time_distribution_plot(results, metrics):
    """Optional: Create response time distribution plot"""
    plt.style.use('seaborn-v0_8')
    fig, ax = plt.subplots(figsize=(8, 5))

    colors = {'sync': '#FF6B6B', 'threads': '#4ECDC4', 'async': '#45B7D1'}
    method_names = {'sync': 'Синхронний', 'threads': 'Потоки', 'async': 'Asyncio'}

    for i, (method, data) in enumerate(results.items()):
        if data and data['individual_times']:
            times = data['individual_times']
            ax.hist(times, bins=20, alpha=0.7, label=method_names[method],
                    color=colors[method], edgecolor='black', linewidth=0.5)

    ax.set_title('Розподіл часів відповіді', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Час відповіді (секунди)', fontsize=12)
    ax.set_ylabel('Частота', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('../results/response_time_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()


def generate_performance_report(metrics):
    """Generate detailed performance report"""

    report = """
ЗВІТ ПРО ПРОДУКТИВНІСТЬ МОДЕЛЕЙ АСИНХРОННИХ ЗАПИТІВ
==================================================

"""

    for method, data in metrics.items():
        method_name = {'sync': 'СИНХРОННА МОДЕЛЬ',
                       'threads': 'МОДЕЛЬ НА ОСНОВІ ПОТОКІВ',
                       'async': 'АСИНХРОННА МОДЕЛЬ (ASYNCIO)'}[method]

        report += f"""
{method_name}:
{'-' * len(method_name)}
 Загальний час виконання: {data['total_time']:.3f} секунд
 Середній час відповіді: {data['avg_response_time']:.3f} секунд
 Медіанний час відповіді: {data['median_response_time']:.3f} секунд
 Мінімальний час відповіді: {data['min_response_time']:.3f} секунд
 Максимальний час відповіді: {data['max_response_time']:.3f} секунд
 Стандартне відхилення: {data['std_response_time']:.3f} секунд
 Успішні запити: {data['successful_requests']}
 Невдалі запити: {data['failed_requests']}
 Відсоток успіху: {data['success_rate']:.1f}%
 Пропускна здатність: {data['throughput']:.2f} запитів/сек
 Ефективність: {data.get('efficiency', 0) * 100:.1f}%


"""

    # Comparative analysis
    if len(metrics) > 1:
        report += """
ПОРІВНЯЛЬНИЙ АНАЛІЗ:
===================
"""

        sync_time = metrics.get('sync', {}).get('total_time', 0)

        for method, data in metrics.items():
            if method != 'sync' and sync_time > 0:
                improvement = (sync_time - data['total_time']) / sync_time * 100
                speedup = sync_time / data['total_time']

                method_name = {'threads': 'Потоки', 'async': 'Asyncio'}[method]
                report += f"• {method_name}: покращення на {improvement:.1f}%, прискорення в {speedup:.1f} раз\n"

    # Save report
    with open('../results/performance_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)

    print(report)
    return report


def run_complete_analysis():
    results = load_results()

    metrics = calculate_metrics(results)

    create_comprehensive_plots(results, metrics)

    # Optional: Create response time distribution plot
    print("Creating response time distribution plot...")
    create_response_time_distribution_plot(results, metrics)

    report = generate_performance_report(metrics)

    return results, metrics, report


if __name__ == "__main__":
    # Ensure results directory exists
    Path('../results').mkdir(exist_ok=True)

    # Run analysis
    results, metrics, report = run_complete_analysis()