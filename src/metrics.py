"""
Stability Metrics
-----------------
Computes quantitative stability metrics on matched LLM outputs.
"""

def compute_agreement_rate(matched_items):
    if not matched_items:
        return 0.0
    return len(matched_items) / len(matched_items)


def compute_polarity_flip_rate(matched_items):
    if not matched_items:
        return 0.0
    flips = sum(1 for a, b in matched_items if a.get('polarity') != b.get('polarity'))
    return flips / len(matched_items)


def compute_bucket_drift_rate(matched_items):
    if not matched_items:
        return 0.0

    drift = 0
    checks = 0

    for a, b in matched_items:
        for bucket in ['intensity_bucket', 'arousal_bucket', 'time_bucket']:
            if bucket in a and bucket in b:
                checks += 1
                if a[bucket] != b[bucket]:
                    drift += 1

    return drift / checks if checks else 0.0


def compute_all_metrics(matched_items):
    return {
        'agreement_rate': compute_agreement_rate(matched_items),
        'polarity_flip_rate': compute_polarity_flip_rate(matched_items),
        'bucket_drift_rate': compute_bucket_drift_rate(matched_items)
    }
