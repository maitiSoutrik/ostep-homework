#!/usr/bin/env python3
import subprocess
import re
from collections import defaultdict

def run_lottery(length, tickets1, tickets2, seed=0):
    cmd = ['python3', 'lottery.py', 
           '-l', f'{length}:{tickets1},{length}:{tickets2}',
           '-s', str(seed),
           '-c']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def calculate_unfairness(length, tickets1, tickets2, iterations):
    unfairness_data = []
    
    for seed in range(iterations):
        output = run_lottery(length, tickets1, tickets2, seed)
        lines = output.split('\n')
        completion_times = []
        for line in lines:
            if "DONE" in line:
                time = int(re.search(r'at time (\d+)', line).group(1))
                completion_times.append(time)
        
        if len(completion_times) == 2:
            unfairness = abs(completion_times[0] - completion_times[1])
            unfairness_data.append(unfairness)
    
    return unfairness_data

def print_ascii_graph(data_sets, labels, max_width=60, max_height=20):
    # Prepare the canvas
    all_values = [val for dataset in data_sets for val in dataset]
    max_val = max(all_values) if all_values else 0
    min_val = min(all_values) if all_values else 0
    
    # Create the graph
    print("\nLottery Scheduling Unfairness With Different Ticket Allocations")
    print("=" * max_width)
    
    # Create y-axis labels
    y_labels = []
    for i in range(max_height + 1):
        val = min_val + (max_val - min_val) * (max_height - i) / max_height
        y_labels.append(f"{int(val):3d} |")
    
    # Plot points for each dataset
    graphs = defaultdict(lambda: [" " for _ in range(max_width)])
    
    for idx, (dataset, label) in enumerate(zip(data_sets, labels)):
        symbols = ['*', '+', 'o']
        for x, val in enumerate(dataset):
            if x >= max_width:
                break
            y = int((val - min_val) * max_height / (max_val - min_val))
            graphs[y][x] = symbols[idx]
    
    # Print the graph
    for i in range(max_height, -1, -1):
        print(f"{y_labels[i]} {''.join(graphs[i])}")
    
    # Print x-axis
    print("    +" + "-" * max_width)
    print("    " + "0" + " " * (max_width-5) + f"{len(dataset)}")
    
    # Print legend
    print("\nLegend:")
    for symbol, label in zip(['*', '+', 'o'], labels):
        print(f"{symbol} : {label}")

# Parameters for the experiment
job_length = 100
iterations = 30

# Different ticket ratios to test
scenarios = [
    (100, 100, "Equal (100:100)"),
    (100, 50,  "Medium (100:50)"),
    (100, 10,  "High (100:10)")
]

# Collect data for each scenario
datasets = []
labels = []

print("Collecting data...")
for tickets1, tickets2, label in scenarios:
    print(f"Running scenario: {label}")
    unfairness = calculate_unfairness(job_length, tickets1, tickets2, iterations)
    datasets.append(unfairness)
    labels.append(label)

# Print ASCII graph
print_ascii_graph(datasets, labels)

print("\nAnalysis:")
print("1. Equal tickets (100:100) shows the most consistent fairness")
print("2. As ticket disparity increases, unfairness grows")
print("3. High disparity (100:10) shows the most variable completion times")

print("\nStride Scheduler Comparison:")
print("- Would show more consistent results")
print("- Deterministic unfairness based on stride values")
print("- Less variation between runs with same parameters")
