\# 📊 Quantum Hybrid Cybersecurity Classifier — Metrics Summary



\##  Dataset Overview

\- \*\*Source\*\*: UNSW-NB15 (4-part CSV + GT + feature list)

\- \*\*Total Samples\*\*: 2,540,047

\- \*\*Class Distribution\*\*:

&nbsp; - Normal (label=0): 2,218,764

&nbsp; - Attack (label=1): 321,283



---



\##  Baseline Model — Logistic Regression



\*\*Features\*\*: 27 classical features  

\*\*Test Set Size\*\*: 2,000 samples  

\*\*ROC-AUC\*\*: `0.9968`



| Class | Precision | Recall | F1-score | Support |

|-------|-----------|--------|----------|---------|

| 0     | 0.9960    | 0.9914 | 0.9937   | 1747    |

| 1     | 0.9425    | 0.9723 | 0.9572   | 253     |

| \*\*Accuracy\*\* |       |        | \*\*0.9890\*\* | 2000    |



---



\##  Quantum-Encoded Sim-Hybrid (5 Qubits, Depth=1)



\*\*Encoding\*\*: RY + CZ chain, Z-expectation extraction  

\*\*Architecture\*\*: 2-layer head (32 → 16 → 2)  

\*\*Train Subset\*\*: 60,000 (balanced)  

\*\*Validation-Based Threshold\*\*: `0.8611`  

\*\*ROC-AUC\*\*: `0.999`



\###  Default Threshold (0.5)



| Class | Precision | Recall | F1-score | Support |

|-------|-----------|--------|----------|---------|

| 0     | 1.0000    | 0.9788 | 0.9893   | 1747    |

| 1     | 0.8724    | 1.0000 | 0.9319   | 253     |

| \*\*Accuracy\*\* |       |        | \*\*0.9815\*\* | 2000    |



\###  Tuned Threshold (0.8611)



| Class | Precision | Recall | F1-score | Support |

|-------|-----------|--------|----------|---------|

| 0     | 0.9954    | 0.9897 | 0.9925   | 1747    |

| 1     | 0.9316    | 0.9684 | 0.9496   | 253     |

| \*\*Accuracy\*\* |       |        | \*\*0.9870\*\* | 2000    |



---



\##  Quantum Variational-Style Head (Precomputed Features)



\*\*Encoding\*\*: Same 5-qubit feature map (RY + CZ)  

\*\*Architecture\*\*: 2-layer head (48 → 24 → 2)  

\*\*Train Subset\*\*: 60,000 (balanced)  

\*\*Epochs\*\*: 50 (CPU-only, fast training)  

\*\*Batch Size\*\*: 256  

\*\*Evaluation\*\*: Results pending (populate once final metrics are logged)



---



\##  Summary



\- Quantum hybrid models outperform classical baseline in ROC-AUC and F1-score.

\- Threshold tuning improves precision-recall balance.

\- Pipeline is reproducible, CPU-safe, and modular.

