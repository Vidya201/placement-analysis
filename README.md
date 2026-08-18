# 🎓 Student Placement Readiness Analyzer

A data-driven web app that analyzes your academic and technical profile and gives you a personalized placement readiness score — based on real student placement data.

## 🚀 Live Demo
[View Live App](https://placement-readiness-analysis.streamlit.app/)

## 📊 Key Findings from the Data
- Students WITH projects get placed **66.4%** of the time vs only **1.9%** without
- **Contrary to popular belief**, internships show almost zero correlation with placement
- Backlogs are the second strongest negative factor (-0.45 correlation)
- Projects are the single most important factor (0.57 correlation)

## 🎯 What This App Does
1. **Placement Score Calculator** — Enter your profile, get a score out of 95 with breakdown
2. **Data Insights** — Visual analysis of what actually drives placement
3. **Key Findings** — Surprising discoveries from 401 student records

## 🛠️ Tech Stack
- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit

## 📁 Dataset
- 401 engineering student records
- Factors: CGPA, Projects, Internships, Backlogs, Technical Courses, Communication
- Target: Placement status (Placed / Not Placed)

## 🔍 How Scoring Works
| Factor | Max Points |
|--------|-----------|
| Project Quality | 35 |
| Technical Certification | 25 |
| Backlog Status | 0 to -15 |
| CGPA | 10 |
| Internship | 15 |
| Communication | 10 |
| **Total** | **95** |

Weights are derived from actual correlation analysis — not assumptions.

## 🚀 Run Locally
```bash
git clone https://github.com/Vidya201/placement-analysis.git
cd placement-analysis
pip install -r requirements.txt
streamlit run ui.py
```

## 📋 Requirements
```
pandas
matplotlib
seaborn
streamlit
```