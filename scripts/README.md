# 🌍 Climate Challenge – Week 0 Setup

## 📌 Project Overview

This repository contains the initial setup for the Climate Challenge project.
The goal of this stage is to establish a clean development environment, version control workflow, and continuous integration (CI) pipeline.

---

## ⚙️ Environment Setup

### 🔹 Option 1: Using `venv`

```bash
# Clone the repository
git clone https://github.com/Lalisecf/climate-challenge-week0.git
cd climate-challenge-week0

# Create virtual environment
python -m venv .venv

# Activate environment
# Windows (PowerShell)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 🔹 Option 2: Using Conda

```bash
# Create environment
conda create -n climate_env python=3.11

# Activate environment
conda activate climate_env

# Install dependencies
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   └── __init__.py
└── scripts/
    ├── __init__.py
    └── README.md
```

---

## 🔄 Git Workflow

### 🌿 Branching Strategy

* `main` → stable branch
* `setup-task` → environment setup and CI configuration

### 📝 Commit Convention (Conventional Commits)



---

## ⚡ Continuous Integration (CI)

This project uses GitHub Actions to ensure the environment is reproducible.

### CI Workflow:

* Runs on every push to `main`
* Installs dependencies using:

```bash
pip install -r requirements.txt
```

* Verifies Python setup

---

## 🚀 How to Run

After setup:

```bash
python --version
```

Or run your scripts from:

```bash
src/
```

---

## 📊 Key Objectives Achieved

* ✅ Version control initialized
* ✅ Virtual environment configured
* ✅ `.gitignore` added
* ✅ Dependencies managed via `requirements.txt`
* ✅ CI pipeline configured
* ✅ Project structure organized

---

## 🤝 Contribution

1. Create a new branch:

```bash
git checkout -b feature-branch
```

2. Commit your changes:

```bash
git commit -m "feat: described changes"
```

3. Push and create a Pull Request

---

## 📌 Notes

* Do not commit:

  * `.venv/`
  * `data/`
  * `.ipynb_checkpoints/`
  * `.csv` files

---

## 👩‍💻 Author

Lalise Fufi
