# Hilbert-Space Intrusion Classification on UNSW-NB15

A mathematically structured intrusion-detection pipeline that maps network telemetry into a compact nonlinear feature space before classification. The system applies parameterised rotation operators and coupled feature interactions, extracts observable coordinates, and trains lightweight PyTorch decision heads under leakage-safe experimental controls.

The repository investigates whether operator-defined embeddings can improve the separation of benign and malicious network traffic while remaining computationally efficient, reproducible, and compatible with downstream cybersecurity analytics and AI-agent workflows.

## Mathematical Formulation

Given a standardised network-traffic vector

\[
x \in \mathbb{R}^{d},
\]

selected components are embedded through a sequence of parameterised rotations and coupling operators:

\[
U(x)
=
\prod_{\ell=1}^{L}
\left[
U_{\mathrm{couple}}
\prod_{j=1}^{q} R_Y(x_j)
\right],
\]

where:

- \(q=5\) is the latent embedding dimension;
- \(R_Y(x_j)\) applies a nonlinear coordinate-wise transformation;
- \(U_{\mathrm{couple}}\) introduces interactions between neighbouring latent coordinates;
- \(L\) denotes the number of feature-map layers.

The transformed state is projected onto an observable basis:

\[
\phi(x)
=
\left[
\langle Z_1\rangle_x,
\langle Z_2\rangle_x,
\ldots,
\langle Z_q\rangle_x
\right].
\]

This defines a compact Hilbert-space representation

\[
\phi(x)\in[-1,1]^5,
\]

which is supplied to a shallow neural classifier:

\[
\hat{y}
=
f_{\theta}\!\left(\phi(x)\right),
\]

where \(\hat{y}\) is the predicted intrusion probability and \(f_{\theta}\) is a trainable PyTorch decision head.

## Results

- **Dataset:** UNSW-NB15
- **Scale:** approximately 2.54 million network-flow observations and 49 attributes
- **ROC-AUC:** 0.999
- **F1 score:** 0.9496
- **Embedding dimension:** five observable coordinates
- **Evaluation:** leakage-safe train, validation, and test separation
- **Operating modes:** balanced classification and high-recall intrusion detection

## Cybersecurity Relevance

The embedding layer compresses heterogeneous network-flow attributes into a structured representation designed to expose nonlinear dependencies between traffic variables.

The resulting detection component supports:

- network-intrusion scoring;
- anomalous-flow prioritisation;
- alert ranking and triage;
- high-recall threat screening;
- downstream security-agent reasoning;
- integration with rule-based, neural, graph-based, or ensemble detection systems.

The feature map and classifier are modular, allowing the pipeline to augment an existing security architecture without replacing its logging, orchestration, policy, or incident-response infrastructure.

## Implemented Models

### Classical Logistic-Regression Baseline

A reference classifier trained on standardised continuous network-traffic features, with an optional categorical feature channel. It provides a transparent benchmark under the same train, validation, and test partitions.

### Online Hilbert-Space Hybrid

Computes the structured nonlinear embedding during execution and supplies the resulting observable coordinates to a two-layer PyTorch classifier:

\[
x
\longmapsto
U(x)
\longmapsto
\phi(x)
\longmapsto
f_{\theta}\!\left(\phi(x)\right)
\longmapsto
\hat{y}.
\]

This architecture evaluates whether a low-dimensional operator-defined representation preserves sufficient information for accurate attack discrimination.

### Precomputed-Embedding Hybrid

Computes the structured representation once and stores the resulting feature matrix:

\[
\Phi
=
\begin{bmatrix}
\phi(x_1) \\
\phi(x_2) \\
\vdots \\
\phi(x_n)
\end{bmatrix}
\in
\mathbb{R}^{n\times q}.
\]

A compact classifier is then trained directly on \(\Phi\). Precomputation removes repeated feature-map simulation from the optimisation loop, enabling faster training and controlled comparison between decision heads.

## Detection Pipeline

```text
UNSW-NB15 network telemetry
            |
            v
Leakage-safe data partitioning
            |
            v
Train-only feature standardisation
            |
            v
Continuous-feature selection
            |
            v
Parameterised rotation mapping
            |
            v
Coupled nonlinear interactions
            |
            v
Observable-coordinate extraction
            |
            v
Compact Hilbert-space embedding
            |
            v
PyTorch classification head
            |
            v
Threshold-calibrated intrusion score
````

## Decision Rule and Threshold Calibration

For an estimated intrusion probability

[
p_{\theta}(y=1\mid x),
]

the final classification is determined by

[
\hat{y}_{\tau}
==============

\mathbf{1}
\left[
p_{\theta}(y=1\mid x)\geq\tau
\right],
]

where (\tau) is selected on the validation set according to the required security objective.

Supported operating modes include:

* **Balanced mode:** selects a threshold that balances precision and recall.
* **High-recall mode:** prioritises attack coverage and reduces false negatives.
* **Threshold-analysis mode:** measures classifier behaviour across multiple decision boundaries.

This is important in cybersecurity settings because the operational cost of a missed intrusion can be significantly greater than the cost of generating an additional alert.

## Experimental Controls

The evaluation pipeline includes:

* deterministic random seeds;
* explicit train, validation, and test partitions;
* train-only fitting of preprocessing transformations;
* leakage-safe feature standardisation;
* validation-based threshold selection;
* balanced and high-recall operating points;
* unified accuracy, precision, recall, F1, ROC-AUC, and PR-AUC reporting;
* saved preprocessing state;
* saved model parameters;
* cached embedding matrices;
* experiment metadata and configuration tracking.

## Outputs

The pipeline generates and stores:

* classification metric tables;
* confusion matrices;
* ROC curves;
* precision-recall curves;
* threshold-analysis reports;
* trained PyTorch model weights;
* fitted feature scalers;
* precomputed embedding matrices;
* data-partition metadata;
* selected decision thresholds;
* model and experiment configurations.

## Repository Structure

```text
data/
    Raw and processed UNSW-NB15 data

notebooks/
    Exploratory analysis and controlled experiments

src/
    Data loading, preprocessing, structured feature maps,
    classification models, training, and evaluation

results/
    Metric tables, figures, and evaluation reports

artifacts_unsw_qdl/
    Saved models, scalers, embeddings, thresholds,
    metadata, and experiment configurations
```

## Installation

Python 3.10 or later is recommended.

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>

python -m venv .venv
```

Activate the environment on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Main Dependencies

* Python
* NumPy
* pandas
* scikit-learn
* PyTorch
* Qiskit
* Matplotlib

Qiskit is used as the numerical backend for constructing and evaluating the parameterised operator map. The cybersecurity classifier consumes only the resulting observable representation and therefore remains compatible with conventional machine-learning and security infrastructure.

## Reproducibility

All reported results are generated using fixed seeds, explicit data partitions, saved preprocessing state, and validation-derived decision thresholds.

Runtime artefacts include:

* trained model weights;
* fitted feature scalers;
* structured feature embeddings;
* evaluation metric tables;
* ROC and precision-recall figures;
* selected operating thresholds;
* experiment metadata.

The precomputed-embedding architecture separates representation generation from classifier optimisation, allowing the decision-layer experiments to be reproduced without recomputing the full nonlinear map.

## Research Objective

The repository addresses the following question:

> Can an operator-defined, low-dimensional Hilbert-space embedding preserve sufficient nonlinear structure in network telemetry to support accurate and computationally efficient intrusion classification?

The results indicate that compact structured embeddings can achieve strong separation between benign and malicious network traffic while remaining suitable for modular integration into broader cybersecurity detection, investigation, and agentic decision systems.

```
```


