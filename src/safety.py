"""
Safety Analysis
---------------
Identifies safety-critical instability in LLM outputs.
"""

def detect_polarity_flips(matched_items):
    """Flag polarity inversions across runs."""
    flags = []
    for a, b in matched_items:
        if a.get('polarity') != b.get('polarity'):
            flags.append({
                'domain': a['domain'],
                'text_a': a['text'],
                'text_b': b['text'],
                'issue': 'POLARITY_FLIP'
            })
    return flags


def summarize_safety(flags):
    return {
        'total_flags': len(flags),
        'flags': flags
    }
