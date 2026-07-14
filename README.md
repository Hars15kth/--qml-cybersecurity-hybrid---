# Hilbert-Space Intrusion Classification on UNSW-NB15

A mathematically structured intrusion-detection pipeline that maps network telemetry into a compact nonlinear feature space before classification. The system applies parameterised rotation operators and coupled feature interactions, evaluates the resulting observables, and trains lightweight PyTorch decision heads under leakage-safe experimental controls.

The repository investigates whether structured nonlinear embeddings can improve the separability of benign and malicious network traffic while remaining computationally practical, reproducible, and compatible with downstream cybersecurity analytics and AI-agent workflows.

## Mathematical Formulation

Given a standardised network-traffic vector \(x \in \mathbb{R}^{d}\), selected components are mapped through parameterised rotation and coupling operators:

\[
U(x)=\prod_{\ell=1}^{L}
\left(
U_{\mathrm{couple}}
\prod_{j=1}^{q} R_Y(x_j)
\right),
\]

where \(q=5\), \(R_Y(x_j)\) defines the coordinate-wise nonlinear transformation, and \(U_{\mathrm{couple}}\) introduces interactions between adjacent latent dimensions.

The resulting state is projected onto a low-dimensional observable basis:

\[
\phi(x)=
\left[
\langle Z_1\rangle_x,
\ldots,
\langle Z_q\rangle_x
\right].
\]

This produces a compact Hilbert-space representation \(\phi(x)\in[-1,1]^5\), which is passed to a shallow neural decision layer for binary intrusion classification.

## Results

- **Dataset:** UNSW-NB15
- **Scale:** approximately 2.54 million observations and 49 attributes
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

A reference classifier trained on standardised continuous network-traffic features, with an optional categorical feature channel. This provides a transparent classical benchmark under the same train, validation, and test partitions.

### Online Hilbert-Space Hybrid

Computes the nonlinear structured embedding during execution and passes the resulting observables to a two-layer PyTorch classifier.

\[
x \longmapsto U(x)
\longmapsto \phi(x)
\longmapsto \operatorname{MLP}(\phi(x))
\longmapsto \hat{y}.
\]

This architecture evaluates whether the low-dimensional operator-defined representation preserves sufficient information for accurate attack discrimination.

### Precomputed-Embedding Hybrid

Computes the structured feature representation once, stores the resulting embedding vectors, and trains a compact decision head over the cached feature matrix.

\[
\Phi=
\begin{bmatrix}
\phi(x_1)\\
\phi(x_2)\\
\vdots\\
\phi(x_n)
\end{bmatrix}.
\]

Precomputation removes repeated simulation from the training loop, enabling faster optimisation, controlled comparison, and reproducible experimentation.

## Detection Pipeline

```text
UNSW-NB15 network telemetry
            |
            v
Leakage-safe preprocessing
            |
            v
Continuous-feature standardisation
            |
            v
Feature selection and dimensional reduction
            |
            v
Parameterised rotation mapping
            |
            v
Coupled nonlinear interactions
            |
            v
Observable feature extraction
            |
            v
Compact Hilbert-space embedding
            |
            v
PyTorch classification head
            |
            v
Threshold-calibrated intrusion score

