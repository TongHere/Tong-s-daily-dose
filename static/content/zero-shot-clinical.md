# Why 'Zero-Shot' Clinical Predictions Are Risky

**Date:** April 19, 2026

**Source:** [How to interpret 'zero-shot' results from generative EHR models — Nature Medicine](https://www.nature.com/articles/s41591-025-04094-8)

---

## Key Takeaways

- Large Language Models (LLMs) are effective at simulating scenarios, making them useful for generating baseline experiences across different contexts.
- However, true prediction—especially in domains requiring high reliability—demands rigorous calibration and testing to reach "oracle-level" accuracy, which exceeds current LLM capabilities.
- LLMs do not always rely strictly on the input data provided when generating predictions, making it essential to verify which data the model actually used.
- As a result, a new evaluation paradigm is required to responsibly apply LLMs to predictive use cases.

---

## Proposed Evaluation Framework

### Performance by Frequency
Evaluate how well the model performs on rare versus common medical events.

### Calibration
Ensure that predicted probabilities (e.g., 30% risk) align with real-world outcome frequencies.

### Timeline Completion
Measure how often the model fails to generate a complete patient timeline.

### Shortcut Audits
Assess whether the model relies on non-clinical shortcuts (e.g., administrative codes) instead of true medical signals.

### Out-of-Distribution Validation
Test model performance on fundamentally different patient populations without retraining.
