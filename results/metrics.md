# Quantum-Hybrid Cybersecurity Classifier

## Performance Summary

This document summarises the evaluation of the classical and quantum-inspired intrusion-classification models developed for the UNSW-NB15 dataset.

The comparison examines whether a compact Hilbert-space embedding can preserve the nonlinear structure required for accurate intrusion detection while remaining computationally efficient, modular, and suitable for integration with conventional cybersecurity systems.

---

## Dataset Overview

| Property                |                                                             Value |
| ----------------------- | ----------------------------------------------------------------: |
| **Dataset**             |                                                         UNSW-NB15 |
| **Input format**        | Four traffic CSV files, ground-truth labels, and feature metadata |
| **Total observations**  |                                                         2,540,047 |
| **Normal observations** |                                                         2,218,764 |
| **Attack observations** |                                                           321,283 |
| **Binary target**       |                               Normal traffic vs malicious traffic |

The binary label is defined as

$$
\begin{aligned}
y
&=
\begin{cases}
0, & \text{normal network traffic}, \
1, & \text{malicious network traffic}.
\end{cases}
\end{aligned}
$$

The complete dataset contains

$$
\begin{aligned}
N_{\mathrm{normal}}
&=
2{,}218{,}764,
\
N_{\mathrm{attack}}
&=
321{,}283.
\end{aligned}
$$

The corresponding attack prevalence is approximately

$$
\begin{aligned}
\Pr(y=1)
&\approx
0.1265.
\end{aligned}
$$

---

## Model Comparison

| Model                                | Input representation                                 |                  ROC-AUC |                Attack F1 |
| ------------------------------------ | ---------------------------------------------------- | -----------------------: | -----------------------: |
| **Logistic Regression**              | 27 standardised classical features                   |                   0.9968 |                   0.9572 |
| **Online Sim-Hybrid Classifier**     | Five-dimensional Hilbert-space embedding             |               **0.9990** |                   0.9496 |
| **Precomputed-Embedding Classifier** | Cached five-dimensional Hilbert-space representation | Architecture implemented | Architecture implemented |

The classical baseline achieves the highest attack-class F1 score in the reported comparison, while the online hybrid model achieves the highest ROC-AUC.

The hybrid architecture therefore demonstrates stronger ranking performance while operating on a substantially lower-dimensional representation.

---

# 1. Classical Baseline

## Logistic-Regression Classifier

The reference model is trained on 27 standardised network-flow features.

| Configuration       |                 Value |
| ------------------- | --------------------: |
| **Model**           |   Logistic regression |
| **Input dimension** | 27 classical features |
| **Test-set size**   |                 2,000 |
| **ROC-AUC**         |                0.9968 |
| **Accuracy**        |                0.9890 |

### Classification Performance

| Class                | Precision | Recall |   F1 score |   Support |
| -------------------- | --------: | -----: | ---------: | --------: |
| Normal traffic — 0   |    0.9960 | 0.9914 |     0.9937 |     1,747 |
| Attack traffic — 1   |    0.9425 | 0.9723 |     0.9572 |       253 |
| **Overall accuracy** |           |        | **0.9890** | **2,000** |

The baseline provides a strong reference point, achieving high attack recall, high precision, and near-perfect ranking performance.

---

# 2. Online Quantum-Encoded Sim-Hybrid Model

## Model Configuration

The hybrid model maps selected traffic coordinates into a five-dimensional operator-defined representation.

The feature transformation is constructed from parameterised rotations and coupled interactions:

$$
\begin{aligned}
U(x)
&=
\prod_{\ell=1}^{L}
\left[
U_{\mathrm{couple}}
\prod_{j=1}^{q}
R_Y(x_j)
\right],
\qquad q=5.
\end{aligned}
$$

Observable extraction produces the compact representation

$$
\begin{aligned}
\phi(x)
&=
\begin{bmatrix}
\langle Z_1\rangle_x \
\langle Z_2\rangle_x \
\vdots \
\langle Z_5\rangle_x
\end{bmatrix}
\in
[-1,1]^5.
\end{aligned}
$$

The resulting vector is supplied to a two-layer PyTorch classification head.

| Configuration                    |                                                  Value |
| -------------------------------- | -----------------------------------------------------: |
| **Encoding**                     | Parameterised $R_Y$ rotations with a CZ coupling chain |
| **Observable extraction**        |                           Pauli-$Z$ expectation values |
| **Embedding dimension**          |                                                      5 |
| **Classifier head**              |                                            32 → 16 → 2 |
| **Training subset**              |                           60,000 balanced observations |
| **Test-set size**                |                                                  2,000 |
| **ROC-AUC**                      |                                                 0.9990 |
| **Validation-derived threshold** |                                                 0.8611 |

The model estimates

$$
\begin{aligned}
\hat{p}(x)
&=
p_{\theta}(y=1\mid x).
\end{aligned}
$$

The corresponding binary decision is

$$
\begin{aligned}
\hat{y}_{\tau}(x)
&=
\mathbf{1}
\left[
\hat{p}(x)\geq\tau
\right].
\end{aligned}
$$

---

## Default Operating Point

At the conventional threshold

$$
\begin{aligned}
\tau
&=
0.5,
\end{aligned}
$$

the model prioritises attack coverage.

| Class                | Precision | Recall |   F1 score |   Support |
| -------------------- | --------: | -----: | ---------: | --------: |
| Normal traffic — 0   |    1.0000 | 0.9788 |     0.9893 |     1,747 |
| Attack traffic — 1   |    0.8724 | 1.0000 |     0.9319 |       253 |
| **Overall accuracy** |           |        | **0.9815** | **2,000** |

At this operating point, the model identifies every malicious observation in the test set:

$$
\begin{aligned}
\operatorname{Recall}_{\mathrm{attack}}
&=
1.0000.
\end{aligned}
$$

This configuration is appropriate for high-recall intrusion screening, where missing an attack is considered more costly than escalating additional alerts.

---

## Validation-Calibrated Operating Point

The validation-derived threshold is

$$
\begin{aligned}
\tau^{\ast}
&=
0.8611.
\end{aligned}
$$

| Class                | Precision | Recall |   F1 score |   Support |
| -------------------- | --------: | -----: | ---------: | --------: |
| Normal traffic — 0   |    0.9954 | 0.9897 |     0.9925 |     1,747 |
| Attack traffic — 1   |    0.9316 | 0.9684 |     0.9496 |       253 |
| **Overall accuracy** |           |        | **0.9870** | **2,000** |

Threshold calibration increases attack precision from

$$
\begin{aligned}
0.8724
&\longrightarrow
0.9316,
\end{aligned}
$$

while attack recall changes from

$$
\begin{aligned}
1.0000
&\longrightarrow
0.9684.
\end{aligned}
$$

The calibrated operating point reduces false-positive pressure while preserving strong attack coverage.

---

## Threshold Comparison

| Metric                  |       Default threshold |          Calibrated threshold |
| ----------------------- | ----------------------: | ----------------------------: |
| **Threshold**           |                  0.5000 |                        0.8611 |
| **Attack precision**    |                  0.8724 |                        0.9316 |
| **Attack recall**       |                  1.0000 |                        0.9684 |
| **Attack F1 score**     |                  0.9319 |                        0.9496 |
| **Accuracy**            |                  0.9815 |                        0.9870 |
| **Operating objective** | Maximum attack coverage | Balanced precision and recall |

The validation-derived threshold improves attack-class F1 and overall accuracy relative to the default operating point.

---

# 3. Precomputed-Embedding Classifier

## Variational-Style Decision Head

The second hybrid architecture computes the structured representation once and stores it as a reusable feature matrix:

$$
\begin{aligned}
\Phi
&=
\begin{bmatrix}
\phi(x_1)^{\mathsf T} \
\phi(x_2)^{\mathsf T} \
\vdots \
\phi(x_n)^{\mathsf T}
\end{bmatrix}
\in
\mathbb{R}^{n\times 5}.
\end{aligned}
$$

A compact neural decision head is then trained directly on the cached embedding matrix.

| Configuration       |                                  Value |
| ------------------- | -------------------------------------: |
| **Encoding**        | Five-coordinate $R_Y$ + CZ feature map |
| **Representation**  |          Precomputed observable matrix |
| **Classifier head** |                            48 → 24 → 2 |
| **Training subset** |           60,000 balanced observations |
| **Epochs**          |                                     50 |
| **Batch size**      |                                    256 |
| **Execution mode**  |                         CPU-compatible |

The architecture separates representation generation from classifier optimisation:

$$
\begin{aligned}
x
&\longmapsto
\phi(x),
\
\phi(x)
&\longmapsto
f_{\theta}!\left(\phi(x)\right).
\end{aligned}
$$

This separation removes repeated feature-map evaluation from the training loop and allows multiple decision heads to be compared using the same fixed representation.

The precomputed architecture provides:

* faster classifier optimisation;
* reproducible embedding-level experiments;
* reduced repeated computation;
* independent comparison of decision heads;
* straightforward reuse of the structured representation;
* compatibility with conventional machine-learning pipelines.

---

# Key Findings

## 1. Strong class separation

The online hybrid model achieves

$$
\begin{aligned}
\operatorname{ROC\text{-}AUC}_{\mathrm{hybrid}}
&=
0.9990,
\end{aligned}
$$

compared with

$$
\begin{aligned}
\operatorname{ROC\text{-}AUC}_{\mathrm{baseline}}
&=
0.9968.
\end{aligned}
$$

Both models operate in a near-saturated discrimination regime, but the hybrid model records the stronger ranking score.

---

## 2. Compact representation

The hybrid classifier operates on

$$
\begin{aligned}
\phi(x)
&\in
\mathbb{R}^{5},
\end{aligned}
$$

rather than the 27-feature input used by the classical baseline.

The result indicates that the operator-defined feature map preserves substantial attack-discriminative information within a compact latent representation.

---

## 3. Threshold selection changes operational behaviour

The same trained model supports different cybersecurity objectives through the choice of $\tau$.

A lower threshold prioritises attack coverage:

$$
\begin{aligned}
\tau
&=
0.5
\quad\Longrightarrow\quad
\operatorname{Recall}_{\mathrm{attack}}
=======================================

1.0000.
\end{aligned}
$$

The validation-calibrated threshold produces a more balanced operating point:

$$
\begin{aligned}
\tau^{\ast}
&=
0.8611
\quad\Longrightarrow\quad
F1_{\mathrm{attack}}
====================

0.9496.
\end{aligned}
$$

---

## 4. Modular deployment

The structured representation can operate as:

* an input to a compact neural classifier;
* an additional feature channel for an ensemble model;
* an intrusion-risk signal for a security agent;
* a prioritisation score for alert triage;
* a reusable representation for investigation workflows;
* an intermediate embedding for graph-based or sequential detection systems.

---

# Final Assessment

The results demonstrate that a compact, five-coordinate Hilbert-space representation can support high-quality intrusion classification on UNSW-NB15.

The online hybrid model achieves a ROC-AUC of **0.9990** and supports two distinct operating regimes:

* **High-recall screening:** complete attack recall at the default threshold.
* **Balanced intrusion classification:** attack-class F1 of **0.9496** after validation-derived threshold calibration.

The classical logistic-regression baseline remains exceptionally strong and achieves a slightly higher attack-class F1 score in the reported comparison.

The central contribution of the hybrid architecture is therefore not merely a marginal metric improvement. It is the preservation of near-saturated discrimination performance within a compact, structured, five-dimensional representation that can be cached, reused, and integrated into broader cybersecurity analytics and agentic decision systems.

---

## Implementation Status

| Component                                | Status   |
| ---------------------------------------- | -------- |
| Dataset ingestion                        | Complete |
| Leakage-safe partitioning                | Complete |
| Classical baseline                       | Complete |
| Online hybrid classifier                 | Complete |
| Threshold calibration                    | Complete |
| Precomputed embedding pipeline           | Complete |
| Variational-style decision head          | Complete |
| Saved models and preprocessing artefacts | Complete |
| Evaluation and reporting pipeline        | Complete |

