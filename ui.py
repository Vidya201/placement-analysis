import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Student Placement Readiness Analyzer", page_icon="🎓", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("Sample.csv")
    df['Internship'] = df['Internships(Y/N)'].map({'Yes': 1, 'No': 0})
    df['Placed'] = df['Placement(Y/N)?'].map({'Placed': 1, 'Not Placed': 0})
    df['Backlog'] = df['Backlog in 5th sem'].map({'Yes': 1, 'No': 0})
    df['Project'] = df['Innovative Project(Y/N)'].map({'Yes': 1, 'No': 0})
    df['Tech_Course'] = df['Technical Course(Y/N)'].map({'Yes': 1, 'No': 0})
    df['Training'] = df['Training(Y/N)'].map({'Yes': 1, 'No': 0})
    return df

df = load_data()


def placement_score(project, tech_course, backlog, cgpa, internship, communication):
    score = 0

    project_points = {
        "No project": 0,
        "College assignment": 5,
        "Personal project": 15,
        "Deployed project": 25,
        "GitHub + deployed + real data": 35
    }
    score += project_points.get(project, 0)

    course_points = {
        "No course": 0,
        "Free YouTube course": 5,
        "NPTEL/Coursera certificate": 15,
        "Industry recognized cert (Google/IBM/AWS)": 25
    }
    score += course_points.get(tech_course, 0)

    internship_points = {
        "No internship": 0,
        "Virtual/certificate internship": 2,
        "Startup internship with stipend": 10,
        "Product company internship": 15
    }
    score += internship_points.get(internship, 0)

    if cgpa < 6:
        score += 0
    elif cgpa < 7:
        score += 3
    elif cgpa < 8:
        score += 6
    elif cgpa < 9:
        score += 8
    else:
        score += 10

    backlog_points = {
        "Active backlog": -15,
        "Cleared backlog": -5,
        "No backlog": 0
    }
    score += backlog_points.get(backlog, 0)

    communication_points = {
        "Poor": 0,
        "Average": 3,
        "Good": 6,
        "Excellent": 10
    }
    score += communication_points.get(communication, 0)

    return score

def get_placement_probability(score):
    if score >= 80:
        return 85
    elif score >= 60:
        return 67
    elif score >= 40:
        return 35
    else:
        return 10

def get_feedback(project, tech_course, backlog, internship, communication, score):
    strengths = []
    weaknesses = []

    if project in ["Deployed project", "GitHub + deployed + real data"]:
        strengths.append("✅ Strong project — this is your biggest asset")
    elif project == "Personal project":
        strengths.append("✅ Personal project exists — deploy it to increase score by 10 points")
    else:
        weaknesses.append("❌ No strong project — this is hurting you most (35 points at stake)")

    if tech_course in ["NPTEL/Coursera certificate", "Industry recognized cert (Google/IBM/AWS)"]:
        strengths.append("✅ Good technical certification")
    else:
        weaknesses.append("❌ No recognized certification — enroll in NPTEL free course")

    if backlog == "Active backlog":
        weaknesses.append("❌ Active backlog — clear it immediately, losing 15 points")
    elif backlog == "Cleared backlog":
        weaknesses.append("⚠️ Cleared backlog noted — still affects score slightly")
    else:
        strengths.append("✅ No backlog — clean academic record")

    if internship in ["Startup internship with stipend", "Product company internship"]:
        strengths.append("✅ Real internship experience")
    else:
        weaknesses.append("⚠️ No real internship — apply on Internshala this week")

    if communication == "Excellent":
        strengths.append("✅ Excellent communication skills")
    elif communication == "Poor":
        weaknesses.append("❌ Communication needs urgent improvement")

    return strengths, weaknesses


st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", [
    "🎯 Check My Score",
    "📊 Data Insights",
    "📈 Key Findings"
])


if page == "🎯 Check My Score":
    st.title("🎓 Student Placement Readiness Analyzer")
    st.markdown("*Based on analysis of 401 real student placement records*")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Enter Your Profile")

        project = st.selectbox("Project Type", [
            "No project",
            "College assignment",
            "Personal project",
            "Deployed project",
            "GitHub + deployed + real data"
        ])

        tech_course = st.selectbox("Technical Course/Certification", [
            "No course",
            "Free YouTube course",
            "NPTEL/Coursera certificate",
            "Industry recognized cert (Google/IBM/AWS)"
        ])

        internship = st.selectbox("Internship Experience", [
            "No internship",
            "Virtual/certificate internship",
            "Startup internship with stipend",
            "Product company internship"
        ])

    with col2:
        st.subheader(" ")

        cgpa = st.slider("Your CGPA", 0.0, 10.0, 7.5, 0.1)

        backlog = st.selectbox("Backlog Status", [
            "No backlog",
            "Cleared backlog",
            "Active backlog"
        ])

        communication = st.selectbox("Communication Level", [
            "Poor",
            "Average",
            "Good",
            "Excellent"
        ])

    st.markdown("---")

    if st.button("🚀 Analyze My Placement Readiness", type="primary"):
        score = placement_score(project, tech_course, backlog, cgpa, internship, communication)
        probability = get_placement_probability(score)
        strengths, weaknesses = get_feedback(project, tech_course, backlog, internship, communication, score)

        st.markdown("---")
        st.subheader("Your Results")

        col1, col2, col3 = st.columns(3)
        col1.metric("Placement Readiness Score", f"{score}/95")
        col2.metric("Placement Probability", f"{probability}%")

        if score >= 70:
            col3.metric("Profile Strength", "Strong 💪")
        elif score >= 45:
            col3.metric("Profile Strength", "Average ⚠️")
        else:
            col3.metric("Profile Strength", "Needs Work ❌")

        
        st.progress(score / 95)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Your Strengths")
            if strengths:
                for s in strengths:
                    st.success(s)
            else:
                st.warning("Build some strengths first")

        with col2:
            st.subheader("What's Hurting You")
            if weaknesses:
                for w in weaknesses:
                    st.error(w)
            else:
                st.success("No major weaknesses found!")

        
        st.subheader("Score Breakdown")
        factors = ['Project', 'Tech Course', 'Internship', 'CGPA', 'Backlog', 'Communication']
        
        project_pts = {"No project": 0, "College assignment": 5, "Personal project": 15, "Deployed project": 25, "GitHub + deployed + real data": 35}
        course_pts = {"No course": 0, "Free YouTube course": 5, "NPTEL/Coursera certificate": 15, "Industry recognized cert (Google/IBM/AWS)": 25}
        intern_pts = {"No internship": 0, "Virtual/certificate internship": 2, "Startup internship with stipend": 10, "Product company internship": 15}
        backlog_pts = {"Active backlog": -15, "Cleared backlog": -5, "No backlog": 0}
        comm_pts = {"Poor": 0, "Average": 3, "Good": 6, "Excellent": 10}
        
        cgpa_pt = 0
        if cgpa >= 9: cgpa_pt = 10
        elif cgpa >= 8: cgpa_pt = 8
        elif cgpa >= 7: cgpa_pt = 6
        elif cgpa >= 6: cgpa_pt = 3

        points = [
            project_pts.get(project, 0),
            course_pts.get(tech_course, 0),
            intern_pts.get(internship, 0),
            cgpa_pt,
            backlog_pts.get(backlog, 0),
            comm_pts.get(communication, 0)
        ]

        colors = ['#2ecc71' if p > 0 else '#e74c3c' for p in points]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(factors, points, color=colors)
        ax.set_xlabel('Points')
        ax.set_title('Your Score Breakdown by Factor')
        ax.axvline(x=0, color='black', linewidth=0.5)
        plt.tight_layout()
        st.pyplot(fig)

# ── PAGE 2: DATA INSIGHTS ──
elif page == "📊 Data Insights":
    st.title("📊 What the Data Says About Placements")
    st.markdown("*Analysis of 401 engineering students*")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Project Impact on Placement")
        project_data = df.groupby('Project')['Placed'].mean() * 100
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['No Project', 'Has Project'], project_data.values, color=['#e74c3c', '#2ecc71'])
        for i, v in enumerate(project_data.values):
            ax.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
        ax.set_ylabel('Placement Rate %')
        ax.set_title('Placement Rate: Project vs No Project')
        ax.set_ylim(0, 80)
        plt.tight_layout()
        st.pyplot(fig)
        st.info("Students WITH projects are placed 35x more than those without")

    with col2:
        st.subheader("Backlog Impact on Placement")
        backlog_data = df.groupby('Backlog')['Placed'].mean() * 100
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['No Backlog', 'Has Backlog'], backlog_data.values, color=['#2ecc71', '#e74c3c'])
        for i, v in enumerate(backlog_data.values):
            ax.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
        ax.set_ylabel('Placement Rate %')
        ax.set_title('Placement Rate: Backlog vs No Backlog')
        ax.set_ylim(0, 80)
        plt.tight_layout()
        st.pyplot(fig)
        st.info("Backlogs significantly reduce placement chances")

    st.markdown("---")
    st.subheader("Correlation Heatmap — What Drives Placement?")
    corr = df[['Internship', 'Placed', 'Backlog', 'Project', 'Tech_Course', 'Training', 'Cgpa']].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Between Factors and Placement')
    plt.tight_layout()
    st.pyplot(fig)


elif page == "📈 Key Findings":
    st.title("📈 Key Findings from the Data")
    st.markdown("---")

    st.subheader("🔍 Surprising Discovery — Internships Don't Drive Placement")
    col1, col2 = st.columns(2)
    with col1:
        with_int = df[df['Internship']==1]['Placed'].mean() * 100
        without_int = df[df['Internship']==0]['Placed'].mean() * 100
        st.metric("Placed WITH Internship", f"{with_int:.1f}%")
        st.metric("Placed WITHOUT Internship", f"{without_int:.1f}%")
    with col2:
        st.info("""
        **Contrary to popular belief**, internships show almost zero correlation 
        with placement in this dataset.
        
        Students with internships get placed at **48.9%** — almost identical 
        to those without internships at **50.6%**.
        
        The data suggests **projects and technical courses** matter far more.
        """)

    st.markdown("---")
    st.subheader("🏆 Factor Importance Ranking")

    factors = ['Project', 'Tech Course', 'No Backlog', 'CGPA', 'Internship', 'Training']
    correlations = [0.57, 0.48, 0.45, 0.04, 0.02, 0.09]
    colors = ['#2ecc71' if c > 0.1 else '#f39c12' for c in correlations]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(factors, correlations, color=colors)
    ax.set_xlabel('Correlation with Placement')
    ax.set_title('What Actually Drives Placement? (Data-Backed)')
    ax.axvline(x=0.1, color='red', linestyle='--', alpha=0.5, label='Meaningful threshold')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Students WITH Project placed", "66.4%")
    col2.metric("Students WITHOUT Project placed", "1.9%")
    col3.metric("Project Multiplier Effect", "35x")