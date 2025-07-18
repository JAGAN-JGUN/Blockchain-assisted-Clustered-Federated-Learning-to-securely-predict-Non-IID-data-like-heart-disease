# Blockchain-Assisted Clustered Federated Learning for Heart Disease Prediction

This repository contains the implementation for a Master's thesis project that explores a **privacy-preserving and robust machine learning framework** using **Clustered Federated Learning (CFL)** enhanced with **Blockchain-based storage**. It is tailored to address **non-IID healthcare data** for **heart disease prediction** using decentralized and secure mechanisms.

> 📘 For full methodology, experimental setup, algorithmic details, and discussion, **please refer to the thesis PDF: [`Thesis.pdf`](./Plag4.pdf)** included in this repository.

---

## 🎯 Objective

The system aims to overcome the limitations of:
- **Centralized machine learning**, which exposes raw data
- **Traditional Federated Learning**, which struggles with non-IID client data

To solve this, the framework integrates:
- **Agglomerative clustering** to group clients with similar data distributions
- **Federated training within each cluster** (CFL)
- **Blockchain smart contracts** to securely store model updates on an immutable ledger and communicate within nodes

---

## 🏗️ Key Components

### ✅ Traditional Machine Learning
Used for **baseline performance** and **model selection**. Logistic Regression is used as the core model for all experiments (centralized, FL, CFL, and BC-CFL).

### 🔁 Federated Learning (FL)
Standard FL setup where 11 simulated clients train models locally and send updates to a global aggregator.

### 🧠 Clustered Federated Learning (CFL)
Clients are clustered using **agglomerative hierarchical clustering** (`HC.py`) on selected features (`fbs`, `chol`, `trestbps`, `restecg`) to mitigate the effect of non-IID data before training.

### 🔐 Blockchain Integration
- A **Solidity smart contract** is deployed to an **Ethereum-based Ganache test network**
- Stores Logistic Regression **coefficients and intercept** immutably
- Interfaced via `Web3.py` from Python for model read/write operations

---

## 📁 Repository Structure

```plaintext
.
├── Blockchain CFL/              # BC-CFL implementation (blockchain-backed clustered FL)
├── Cluster Fed Learning/        # CFL without blockchain
├── Fed Learning/                # Vanilla FL baseline
├── Centralized/                 # Centralized training for baseline/model selection
├── HC.py                        # Clustering logic using hierarchical agglomerative method
├── Split.py / Synth.py          # Data splitting and synthetic data generation
├── *.csv                        # Dataset files (heart.csv, train.csv, test.csv)
├── Plag4.pdf                    # Thesis document with complete technical details
