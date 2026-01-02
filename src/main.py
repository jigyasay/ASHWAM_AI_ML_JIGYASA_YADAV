"""
Main Orchestrator
----------------
Runs the full stability and safety evaluation pipeline.
"""

import json
import itertools
from matcher import match_items
from metrics import compute_all_metrics
from safety import detect_polarity_flips, summarize_safety


def load_run(path):
    with open(path, 'r') as f:
        return json.load(f)['items']


def analyze_journal(run_paths):
    runs = [load_run(p) for p in run_paths]

    all_matches = []
    for run_a, run_b in itertools.combinations(runs, 2):
        all_matches.extend(match_items(run_a, run_b))

    metrics = compute_all_metrics(all_matches)
    safety_flags = detect_polarity_flips(all_matches)

    return {
        'metrics': metrics,
        'safety': summarize_safety(safety_flags)
    }


if __name__ == '__main__':
    print("LLM Stability & Safety Evaluation")
    print("Use analyze_journal([run1.json, run2.json, run3.json])")
