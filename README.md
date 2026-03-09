# AIProject
AI project implementing plant species classification using transfer learning and a semantic ontology system for botanical knowledge representation and reasoning.


# Automated Plant Recognition and Botanical Knowledge Representation

This repository contains two Artificial Intelligence project components:

1. **Deep Learning System for Automated Plant Recognition**
2. **Knowledge Representation System for Botanical Data**

The project demonstrates both **data-driven AI (Deep Learning)** and **symbolic AI (Ontology-based Knowledge Representation)**.

---


### File description

| File | Description |
|-----|-------------|
| PlantRecognition.ipynb | Deep learning notebook for plant recognition |
| botany.py | Script that loads ontology, maps database data, and runs reasoning |
| Botany.rdf | OWL ontology describing plants, habitats, and regions |
| botany_entities.db | SQLite database with plant entities |
| requirements.txt | Python dependencies |

---

# Part 1 — Deep Learning System

## Goal
Develop a system that can **recognize plant species from leaf images** using deep learning.

## Method
The model uses **transfer learning with MobileNetV2**.

Main steps:

1. Load leaf image dataset
2. Preprocess images
3. Apply data augmentation
4. Use MobileNetV2 as a pretrained feature extractor
5. Add classification layers
6. Train the model
7. Fine-tune upper layers
8. Evaluate predictions

### Techniques Used

- Transfer Learning
- Convolutional Neural Networks
- Data Augmentation
- Model Fine-Tuning

### Frameworks

- TensorFlow
- Keras

---

# Part 2 — Knowledge Representation System

## Goal
Represent botanical knowledge using **semantic ontologies** and perform automated reasoning.

## Method

The system combines:

- OWL ontology
- SQLite database
- Python integration using Owlready2

## Workflow

1. Create database tables
2. Load ontology file
3. Convert database rows to ontology individuals
4. Create relationships between plants, habitats, and regions
5. Run ontology reasoner
6. Save enriched ontology

---

# Installation

## 1 Clone repository

```
git clone https://github.com/your-username/ArtificialIntelligenceProject.git
cd ArtificialIntelligenceProject
```

## 2 Create virtual environment

Windows

```
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```
python3 -m venv venv
source venv/bin/activate
```

## 3 Install dependencies

```
pip install -r requirements.txt
```

---

# Running the Project

## Deep Learning

Open the notebook:

```
jupyter notebook
```

Run

```
Untitled9 (1).ipynb
```

The notebook performs:

- dataset loading
- preprocessing
- training
- fine-tuning
- evaluation
- prediction visualization

---

## Knowledge Representation

### Step 1 Create database

```
python sql.py
```

### Step 2 Run ontology integration

```
python botany.py
```

Expected output:

```
botany_final.owl
```

---

# Results

## Deep Learning

The model:

- recognizes plant species using leaf images
- uses MobileNetV2 transfer learning
- produces classification predictions

Outputs include:

- training curves
- confusion matrix
- prediction examples

## Knowledge Representation

The ontology:

- represents plants, habitats, and regions
- maps relational database data to ontology individuals
- performs automated reasoning

---

# Dependencies

Main libraries:

- TensorFlow
- NumPy
- Matplotlib
- Pillow
- Owlready2
- Jupyter Notebook

Standard Python libraries used:

- sqlite3
- os
- sys
- re

---

# Author

Lina Babayan

French University in Armenia  
M1 Artificial Intelligence Project

---
