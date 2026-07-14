You’re right. Here is the complete README as one continuous block of GitHub-ready Markdown, with no outer code cell.

# Hilbert-Space Intrusion Classification on UNSW-NB15

A mathematically structured intrusion-detection pipeline that maps network telemetry into a compact nonlinear representation before classification. The system applies parameterised rotation operators, coupled feature interactions, observable projection, and lightweight PyTorch decision heads under leakage-safe experimental controls.

The repository investigates whether low-dimensional operator-defined embeddings can preserve the nonlinear structure required to distinguish benign and malicious traffic while remaining computationally efficient, reproducible, and compatible with existing cybersecurity analytics and AI-agent workflows.

## Mathematical Formulation

Let a standardised network-flow observation be represented by

$$
x \in \mathbb{R}^{d}.
$$

Selected coordinates are embedded through a composition of parameterised rotations and coupling operators:

$$
U(x)
====

\prod_{\ell=1}^{L}
\left[
U_{\mathrm{couple}}
\prod_{j=1}^{q} R_Y(x_j)
\right],
$$

where:

* $q=5$ is the latent embedding dimension;
* $R_Y(x_j)$ applies a nonlinear coordinate-dependent rotation;
* $U_{\mathrm{couple}}$ introduces interactions between neighbouring latent coordinates;
* $L$ denotes the number of feature-map layers.

The transformed state is projected onto an observable basis:

$$
\phi(x)
=======

\left[
\langle Z_1\rangle_x,
\langle Z_2\rangle_x,
\ldots,
\langle Z_q\rangle_x
\right].
$$

This defines a compact Hilbert-space representation

$$
\phi(x)\in[-1,1]^5,
$$

which is supplied to a trainable decision function:

$$
\hat{p}(x)
==========

f_{\theta}!\left(\phi(x)\right),
$$

where $\hat{p}(x)$ is the estimated probability that the network-flow observation is malicious and $f_{\theta}$ is a lightweight PyTorch classification head.

## Results

* **Dataset:** UNSW-NB15
* **Scale:** approximately 2.54 million network-flow observations and 49 attributes
* **ROC-AUC:** 0.999
* **F1 score:** 0.9496
* **Embedding dimension:** five observable coordinates
* **Evaluation:** leakage-safe train, validation, and test partitions
* **Operating modes:** balanced classification and high-recall intrusion detection

## Cybersecurity Relevance

The embedding layer compresses heterogeneous network-flow attributes into a structured representation designed to expose nonlinear dependencies between traffic variables.

The resulting detection component supports:

* network-intrusion scoring;
* anomalous-flow prioritisation;
* alert ranking and triage;
* high-recall threat screening;
* downstream security-agent reasoning;
* integration with rule-based, neural, graph-based, or ensemble detection systems.

The representation layer and classifier are modular. They can augment an existing cybersecurity architecture without replacing its logging, orchestration, policy, or incident-response infrastructure.

## Implemented Models

### Classical Logistic-Regression Baseline

A reference classifier trained on standardised continuous network-flow features, with an optional categorical feature channel.

The baseline provides a transparent comparison under the same data partitions, preprocessing constraints, and evaluation protocol as the structured embedding models.

### Online Hilbert-Space Classifier

The online architecture computes the nonlinear representation during execution and supplies the resulting observable coordinates to a two-layer PyTorch classifier:

$$
x
\longmapsto
U(x)
\longmapsto
\phi(x)
\longmapsto
f_{\theta}!\left(\phi(x)\right)
\longmapsto
\hat{p}(x).
$$

This model tests whether a low-dimensional operator-defined representation preserves sufficient information for accurate attack discrimination.

### Precomputed-Embedding Classifier

The second architecture computes the structured representation once and stores the resulting feature matrix:

$$
\Phi
====

\begin{bmatrix}
\phi(x_1) \
\phi(x_2) \
\vdots \
\phi(x_n)
\end{bmatrix}
\in
\mathbb{R}^{n\times q}.
$$

A compact neural classifier is then trained directly on $\Phi$.

Precomputation removes repeated feature-map evaluation from the optimisation loop, enabling faster training, controlled comparison between classification heads, and reproducible experimentation.

## Detection Pipeline

```
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
```

## Decision Rule

Given an estimated malicious-traffic probability

$$
\hat{p}(x)
==========

p_{\theta}(y=1\mid x),
$$

the final binary decision is

$$
\hat{y}_{\tau}
==============

\mathbf{1}
\left[
\hat{p}(x)\geq\tau
\right],
$$

where $\tau$ is a validation-derived operating threshold.

The threshold is not assumed to be fixed at $0.5$. It is selected according to the operational objective of the security system.

Supported modes include:

* **Balanced mode:** balances precision and recall for general intrusion classification.
* **High-recall mode:** prioritises attack coverage and reduces false negatives.
* **Threshold-analysis mode:** evaluates detection behaviour across multiple operating boundaries.

This is important in cybersecurity environments because the cost of a missed intrusion may be substantially greater than the cost of generating an additional alert.

## Experimental Controls

The evaluation pipeline includes:

* deterministic random seeds;
* explicit train, validation, and test partitions;
* train-only fitting of preprocessing transformations;
* leakage-safe feature standardisation;
* validation-derived decision thresholds;
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
* model configurations;
* experiment metadata.

## Repository Structure

```
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

Clone the repository:

```
git clone https://github.com/<username>/<repository>.git
cd <repository>
```

Create a virtual environment:

```
python -m venv .venv
```

Activate the environment on Linux or macOS:

```
source .venv/bin/activate
```

Activate the environment on Windows:

```
.venv\Scripts\activate
```

Install the required packages:

```
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

Qiskit is used as the numerical backend for constructing and evaluating the parameterised operator map.

The cybersecurity classifier consumes the resulting observable representation and therefore remains compatible with conventional machine-learning, detection, and security-orchestration infrastructure.

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

The precomputed-embedding architecture separates representation generation from classifier optimisation. This allows the decision-layer experiments to be reproduced without recomputing the complete nonlinear map.

## Research Objective

The repository addresses the following question:

> Can an operator-defined, low-dimensional Hilbert-space embedding preserve sufficient nonlinear structure in network telemetry to support accurate and computationally efficient intrusion classification?

The results indicate that compact structured embeddings can achieve strong separation between benign and malicious network traffic while remaining suitable for modular integration into broader cybersecurity detection, investigation, and agentic decision systems.





