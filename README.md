\### qml-cybersecurity-hybrid



\#### Quantum-Enhanced Intrusion Detection on UNSW-NB15 (Hybrid QML + DL)



A CPU-friendly, leakage-safe, quantum-classical hybrid pipeline for network intrusion detection on UNSW-NB15. It standardizes continuous features, encodes them via a compact quantum feature map simulated with Qiskit (Statevector, RY + CZ chain), and trains lightweight PyTorch heads. Includes a strong scikit-learn classical baseline for fair comparison, unified metrics, ROC/PR curves, and saved artifacts for reproducibility.



\#### Key Features

\- Dataset: UNSW-NB15 (~2.54M rows, 49 features), split into train/val/test with a balanced 60k training subset for speed on CPU.

\- Quantum encoding: 5-qubit, depth-1 RY data reuploading + CZ entanglement; extract Z-expectations as quantum features.

\- Models:

&nbsp; - Classical Baseline: LogisticRegression reference on standardized continuous features (+ optional categorical channel).

&nbsp; - Quantum-Encoded Sim-Hybrid (Cell 6): On-the-fly quantum features -> 2-layer MLP head.

&nbsp; - Variational Hybrid with Precomputed Quantum Features (Cell 7): Precompute quantum features once, train a compact head for 50 fast epochs.

\- Evaluation: Accuracy, precision/recall/F1, ROC-AUC; threshold tuning for high-recall vs balanced operating modes.

\- Artifacts: Metrics table, confusion matrices, ROC/PR plots, model weights, scaler and meta config.



\#### Repo Layout

\- data/            Raw/processed data (not committed by default)

\- notebooks/       Exploratory notebooks and experiments

\- results/         Generated plots, tables, reports

\- src/             Source code (data loading, features, models, training)

\- artifacts\_unsw\_qdl/  Saved metrics, figures, models, scalers, metadata (created at runtime)





\#### Getting Started



1\) Python environment

\- Python 3.10+ recommended.

\- Install dependencies:

```bash

pip install -r requirements.txt



2)Data

-Place UNSW-NB15 CSV splits in a local directory (as in the examples).

-Update paths in your scripts/notebooks as needed (e.g., DATA\_DIR).

3)Run the baseline and quantum hybrids

-Baseline (LogisticRegression) on standardized continuous features.

-Quantum-Encoded Sim-Hybrid (Cell 6): 5-qubit feature map simulated on CPU, two hidden layers (e.g., 32 -> 16), fixed epochs.

-Variational Hybrid (Cell 7): Precompute quantum features (train/val/test), train a small head for 50 epochs in seconds on CPU.

4)Threshold tuning

-Compute validation precision-recall curve and select threshold to maximize F1 or to meet a minimum precision target.

-Re-evaluate on test with tuned threshold.

5)Example Metrics (test set, untuned unless noted)

-Baseline: Acc ≈ 0.989, F1\_pos ≈ 0.957, ROC-AUC ≈ 0.9968

-Q-Encoded Sim-Hybrid (5q): Acc ≈ 0.982–0.985, F1\_pos ≈ 0.932–0.956, ROC-AUC ≈ 0.998–0.999

\-Variational Hybrid (5q): Acc ≈ 0.987, F1\_pos ≈ 0.949, ROC-AUC ≈ 0.999

-Tuned thresholds further improve precision/F1 while ROC-AUC remains unchanged.

6)Reproducibility

-Seeds fixed.

-StandardScaler saved to artifacts.

-Meta file logs key hyperparameters (qubits, depth, batch sizes, feature lists, seed).

7)Notes on Leakage Safety

-Avoid label-derived signals in feature engineering.

-Use a neutral angle-channel one-hot; do not encode labels.

-Keep validation/test untouched; downsample only the training subset.

8)Next Steps

-Increase qubits/depth if GPU/accelerators available (e.g., 6–8 qubits, depth 2–3).

\-Explore alternative encodings (RX/RY mixing, learned classical projection).

\-Integrate a differentiable variational circuit if compute allows.

\-Extend to multiclass attack categories once robust joins are established.

