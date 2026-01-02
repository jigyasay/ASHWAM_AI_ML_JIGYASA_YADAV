"""
Deterministic Matcher
--------------------
Aligns semantic objects across LLM runs using evidence-span overlap.
Primary signal: Jaccard similarity over evidence spans.
"""

def jaccard_overlap(span_a: str, span_b: str) -> float:
    set_a = set(span_a.lower().split())
    set_b = set(span_b.lower().split())
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def match_items(run_a, run_b, threshold=0.5):
    """
    Deterministically match items between two runs.
    - Same domain only
    - One-to-one matching
    - Evidence span overlap as primary signal
    """
    matches = []
    used_b = set()

    for item_a in run_a:
        best_item = None
        best_score = 0.0

        for idx, item_b in enumerate(run_b):
            if idx in used_b:
                continue
            if item_a['domain'] != item_b['domain']:
                continue

            score = jaccard_overlap(item_a['evidence_span'], item_b['evidence_span'])
            if score > best_score:
                best_score = score
                best_item = (idx, item_b)

        if best_item and best_score >= threshold:
            used_b.add(best_item[0])
            matches.append((item_a, best_item[1]))

    return matches
