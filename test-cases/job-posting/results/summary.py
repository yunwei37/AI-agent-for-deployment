import os
import re
import json
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

def parse_stats_line(line):
    # Extract stats using regex
    pattern = r"Duration: (\d+)m (\d+\.\d+)s \| Cost: \$(\d+\.\d+) \| LLMs: (\d+) \| Tools: (\d+)"
    match = re.search(pattern, line)
    if match:
        minutes, seconds, cost, llms, tools = match.groups()
        duration_seconds = float(minutes) * 60 + float(seconds)
        return {
            "duration": duration_seconds,
            "cost": float(cost),
            "llms": int(llms),
            "tools": int(tools)
        }
    return None

def process_experiment(base_path, experiment_name):
    results = []
    
    # Process each run (1,2,3)
    for run in range(1, 4):
        log_path = os.path.join(base_path, experiment_name, str(run), "agentops.log")
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                for line in f:
                    stats = parse_stats_line(line)
                    if stats:
                        results.append(stats)
                        break  # Only need the stats line from each file
    
    # Calculate averages
    if results:
        avg_results = {
            "duration": mean([r["duration"] for r in results]),
            "cost": mean([r["cost"] for r in results]),
            "llms": mean([r["llms"] for r in results]),
            "tools": mean([r["tools"] for r in results])
        }
    else:
        avg_results = None
    
    return {
        "individual_runs": results,
        "averages": avg_results
    }

def process_merged_experiments(base_path, experiment_names):
    results = []
    
    # Process each experiment in the merged group
    for exp_name in experiment_names:
        # Process each run (1,2,3)
        for run in range(1, 4):
            log_path = os.path.join(base_path, exp_name, str(run), "agentops.log")
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    for line in f:
                        stats = parse_stats_line(line)
                        if stats:
                            results.append(stats)
                            break  # Only need the stats line from each file
    
    # Calculate averages
    if results:
        avg_results = {
            "duration": mean([r["duration"] for r in results]),
            "cost": mean([r["cost"] for r in results]),
            "llms": mean([r["llms"] for r in results]),
            "tools": mean([r["tools"] for r in results])
        }
    else:
        avg_results = None
    
    return {
        "individual_runs": results,
        "averages": avg_results
    }

def create_bar_charts(results):
    # Prepare data
    experiments = list(results.keys())
    metrics = {
        'duration': {'values': [], 'title': 'Average Duration (seconds)', 'color': 'blue'},
        'cost': {'values': [], 'title': 'Average Cost ($)', 'color': 'green'}
    }
    
    # Extract average values
    for exp in experiments:
        if results[exp]['averages']:
            for metric in metrics:
                metrics[metric]['values'].append(results[exp]['averages'][metric])
        else:
            for metric in metrics:
                metrics[metric]['values'].append(0)
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    fig.suptitle('Experiment Results Comparison', fontsize=20)
    
    # Plot each metric
    for (metric, data), ax in zip(metrics.items(), [ax1, ax2]):
        bars = ax.bar(experiments, data['values'], color=data['color'], width=0.5)
        ax.set_title(data['title'], fontsize=16)
        ax.set_xticklabels(experiments, rotation=45, ha='right', fontsize=12)
        ax.tick_params(axis='y', labelsize=12)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom',
                   fontsize=14)
    
    plt.tight_layout()
    return fig

def main():
    base_path = "/root/knowledgeCache/AI-agent-for-deployment/test-cases/job-posting/results"
    
    # Define experiment groups
    merged_experiments = ["default-gpt-4o", "default-gpt-4o1", "default-gpt-4o2"]
    other_experiments = [
        "default-gpt-4o-mini",
        "gpt4o-for-search",
        "mini-for-search"
    ]
    
    results = {}
    
    # Process merged experiments
    results["default-gpt-4o-merged"] = process_merged_experiments(base_path, merged_experiments)
    
    # Process other experiments normally
    for exp in other_experiments:
        results[exp] = process_experiment(base_path, exp)
    
    # Save results to JSON file
    output_path = os.path.join(base_path, "experiment_stats.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Create and save bar charts
    fig = create_bar_charts(results)
    chart_path = os.path.join(base_path, "experiment_stats.png")
    fig.savefig(chart_path)
    
    print(f"Results have been saved to {output_path}")
    print(f"Charts have been saved to {chart_path}")

if __name__ == "__main__":
    main()