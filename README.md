# LLM Stability & Safety Evaluation Framework
# Run-to-Run Variance & Stability Analysis for LLM Outputs

## Project Overview

Large Language Models (LLMs) are **non-deterministic**: the same prompt can yield different outputs across runs. In safety-sensitive domains like **women’s health journaling**, this variance can lead to contradictory interpretations, unsafe nudges, or loss of user trust.

This project designs and implements a **stability and safety evaluation framework** to systematically measure **run-to-run variance** in structured LLM outputs **without relying on ground-truth labels**.

## Defining Stability

Because textual outputs can vary while meaning remains the same, stability is defined at the **semantic object level**, not the raw text level.

Two outputs are considered *stable* if they refer to the same underlying real-world concept, even when phrasing or buckets differ.


The framework focuses on:

* Deterministic alignment of semantic objects across runs
* Quantifying stability using interpretable metrics
* Surfacing *safety-critical failures* such as polarity flips

---

## Problem Statement

Given:

* A single user journal entry
* Multiple LLM extraction runs (run1, run2, run3)

We observe that:

* Extracted items differ in wording, confidence, and sometimes meaning
* Traditional accuracy metrics fail due to lack of labels

**Goal:**

> Measure whether the LLM is *stable and safe*, not whether it is *correct*.

---

## Data Description

### Input

* Raw journal entries (natural language, multilingual)
* Three independent LLM extraction runs per journal

Each run outputs structured items with:

* `domain` (food, symptom, emotion, mind)
* `text`
* `evidence_span`
* `polarity`
* `intensity / arousal buckets`
* `confidence`

### Example Journal

```json
{
  "journal_id": "B004",
  "text": "Had oats with banana and walnuts... but not sad"
}
```

---

## System Architecture (High Level)

```
Raw Journal Entry
        │
        ▼
  LLM Extraction (3 Runs)
        │
        ▼
Structured JSON Outputs
        │
        ▼
Deterministic Matching Engine
        │
        ▼
Stability Metrics Computation
        │
        ▼
Safety & Risk Analysis
```

---

## Phase-wise Workflow

### Phase 1 — Data Ingestion

* Load journal entries and all associated runs
* Validate schema consistency
* Group runs by `journal_id`

---

### Phase 2 — Deterministic Object Matching

Before measuring stability, semantic objects must be **explicitly aligned**.

#### Matching Rules

* Match only within the same `domain`
* Compute **Jaccard overlap** between evidence spans
* Enforce one-to-one matching
* Unmatched items are explicitly recorded

#### Why Evidence Spans?

* Anchored in user-authored text
* Auditable and deterministic
* Avoids probabilistic embedding drift

#### Flow

```
Run 1 Items ─┐
             ├─ Evidence Span Overlap ──► Matched Pairs
Run 2 Items ─┘
```

---

### Phase 3 — Stability Metrics

After alignment, stability is measured at **field level**, not raw text level.

#### Metrics Used

| Metric             | Definition                    | Purpose               |
| ------------------ | ----------------------------- | --------------------- |
| Agreement Rate     | % of matched items consistent | Overall stability     |
| Polarity Flip Rate | Polarity changes across runs  | Safety signal         |
| Bucket Drift Rate  | Changes in intensity/arousal  | Expected subjectivity |
| Missing Rate       | Items absent in some runs     | Recall variance       |

Agreement Rate =
(number of matched objects across runs)
---------------------------------------
(number of unique objects across runs)

Polarity Flip Rate =
(number of matched objects with polarity disagreement)
------------------------------------------------------
(total matched objects)

Bucket Drift Rate =
(number of matched objects with bucket change)
----------------------------------------------
(total matched objects)

> **Key Insight:** High agreement does not imply safety.
> These metrics are designed to surface safety-critical instability rather than optimize for a single score.

---

### Phase 4 — Safety Risk Analysis

Certain inconsistencies are treated as **safety-critical**.

#### Safety Rules

* Polarity flips (e.g., `absent → present`) are flagged
* Negation phrases (e.g., *"not sad"*) are high-risk
* Emotional domain errors weighted higher than food mentions

#### Real Example

In journal **B004**:

* Two runs marked *sadness = absent*
* One run marked *sadness = present*

This is flagged as a **semantic inversion risk**.

---

### Phase 5 — Production Implications

#### Why Stability Matters

* Downstream recommendations may conflict
* User trust erodes with contradictory summaries
* Model upgrades need regression safety checks

#### Design Insight

> Stability metrics act as **regression tests for LLM behavior**.

---

## Optional: Stable Output Aggregation

To produce a final user-facing output:

* Polarity: unanimous → else `uncertain`
* Buckets: majority vote
* Evidence: most frequent span

```json
{
  "domain": "emotion",
  "text": "sadness",
  "polarity": "uncertain",
  "confidence": "low"
}
```

---

## Key Design Decisions

* Deterministic matching over embeddings
* Safety-first interpretation of variance
* No reliance on ground truth labels
* Explicit handling of uncertainty

---

## Limitations

* Small dataset
* Rule-based matching may miss paraphrases
* No causal inference

---

## Future Improvements

* Negation-aware parsing
* Span-level semantic normalization
* Longitudinal stability tracking
* Model-version comparison dashboards

---

## Final Takeaway

> This project is not about correctness.
> It is about **safe decision-making under uncertainty**.

The framework provides a principled way to evaluate and control LLM variance in real-world, safety-sensitive systems.
