🌍 Climate Challenge – Week 0
📌 Project Overview

This repository contains the Week 0 challenge work for the 10 Academy AI Mastery Program.

The project focuses on:

Setting up a reproducible data science environment
Cleaning and exploring climate datasets
Preparing structured data for further analysis

The work supports climate data analysis aligned with COP32 preparation.

🎯 Objectives
Task 1: Environment & Version Control
Set up a clean Python development environment
Implement Git workflow and repository structure
Configure Continuous Integration (CI)
Task 2: Data Profiling & EDA
Clean and preprocess climate datasets
Handle missing values and anomalies
Perform exploratory data analysis (EDA)
Generate initial insights for each country
Task 4: Interactive Dashboard (Bonus)
Build a Streamlit dashboard for visualization
Enable user interaction (filters & selections)
Present insights in a clear and visual format
🌐 Dataset

Data is sourced from the
NASA POWER.

Countries: Ethiopia, Kenya, Sudan, Tanzania, Nigeria
Date Range: January 2015 – March 2026
Frequency: Daily observations

⚠️ Note:
The data/ folder is excluded from version control and not included in this repository.

⚙️ Environment Setup (venv)
# Clone the repository
git clone https://github.com/Lalisecf/climate-challenge-week0.git
cd climate-challenge-week0

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
🚀 How to Run
▶️ Run Notebooks (EDA)
jupyter notebook

Open:

notebooks/<country>_eda.ipynb

Run all cells to reproduce the analysis.

Run Dashboard (Streamlit)
streamlit run app/main.py
Dashboard Features:
🌍 Multi-country selection
📅 Year range filter
🌡 Temperature trend (monthly)
🌧 Precipitation distribution (boxplot)
📊 Summary statistics & ANOVA
🏆 Country ranking


🧪 Run Tests
pytest tests/
🧹 Code Quality Check
flake8 src/ tests/
📁 Project Structure
├── .github/workflows/ci.yml   # CI pipeline
├── app/                      # Streamlit dashboard
│   ├── main.py
│   └── utils.py
├── src/                      # Utility functions
├── notebooks/               # EDA notebooks
├── tests/                   # Unit tests
├── scripts/                 # Supporting scripts
├── requirements.txt
├── README.md
🔄 Workflow
Branching
main → stable code
setup-task → environment setup & CI
eda-<country> → country-specific analysis
dashboard-dev → Streamlit dashboard
Commits

Uses Conventional Commits:

EDA for -<country>  climate dataset
chore: setup environment
ci: configure workflow
⚡ Continuous Integration

GitHub Actions workflow:

Runs on push and pull request
Installs dependencies
Verifies environment setup
Runs linting and tests

📊 Summary of Work
Environment and CI pipeline configured
Data cleaned and standardized
Missing values and outliers handled
Exploratory analysis completed for all countries
Interactive dashboard built

📌 Notes

The following are excluded from the repository:

.venv/
data/
.csv files

👩‍💻 Author

Lalise Fufi