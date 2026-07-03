import matplotlib.pyplot as plt
import numpy as np
import config

def plot_labour_cost_comparison(ga24_metrics, mip24_metrics, ga65_metrics, mip65_metrics):
    '''
    Plot labour cost comparison between GA and MIP.
    '''

    algorithms = ['GA', 'MIP']

    cost_24 = [ga24_metrics['Labour Cost'], mip24_metrics['Labour Cost']]

    cost_65 = [ga65_metrics['Labour Cost'], mip65_metrics['Labour Cost']]

    x = np.arange(len(algorithms))
    width = 0.35

    plt.figure(figsize=(7,5))

    bars1 = plt.bar(x - width/2, cost_24, width, label='24 Employees')
    bars2 = plt.bar(x + width/2, cost_65, width, label='65 Employees')

    plt.xticks(x, algorithms)
    plt.ylabel('Labour Cost')
    plt.title('Comparison of Labour Cost between GA and MIP')
    plt.legend()

    # Display values on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height(),
                f'{bar.get_height():.0f}',
                ha='center',
                va='bottom',
                fontsize=9
            )

    plt.tight_layout()

    # save figure 
    plt.savefig(config.EXC_TIME_GRAPH, dpi = 300, bbox_inches = 'tight')

    plt.show()

def plot_execution_time_comparison(ga24_metrics, mip24_metrics, ga65_metrics, mip65_metrics):
    '''
    Plot execution time comparison between GA and MIP.
    '''

    algorithms = ['GA', 'MIP']

    time_24 = [ga24_metrics['execution_time'],  mip24_metrics['execution_time']]

    time_65 = [ga65_metrics['execution_time'],  mip65_metrics['execution_time']]

    x = np.arange(len(algorithms))
    width = 0.35

    plt.figure(figsize=(7,5))

    bars1 = plt.bar(x - width/2, time_24, width, label='24 Employees')
    bars2 = plt.bar(x + width/2, time_65, width, label='65 Employees')

    plt.xticks(x, algorithms)
    plt.ylabel('Execution Time (Seconds)')
    plt.title('Comparison of Execution Time between GA and MIP')
    plt.legend()

    for bars in [bars1, bars2]:
        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height(),
                f'{bar.get_height():.2f}',
                ha='center',
                va='bottom',
                fontsize=9
            )

    plt.tight_layout()

    # save figure 
    plt.savefig(config.LABOUR_COST_GRAPH, dpi = 300, bbox_inches = 'tight')
    plt.show()