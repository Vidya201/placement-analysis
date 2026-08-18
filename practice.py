import pandas as pd
df=pd.read_csv(r"C:\Users\vidya\OneDrive\Desktop\Sample.csv")
df2=pd.read_csv(r"C:\Users\vidya\OneDrive\Desktop\indian_student_placement_data.csv")
import pandas as pd


df['Internship'] = df['Internships(Y/N)'].map({'Yes': 1, 'No': 0})
df['Placed'] = df['Placement(Y/N)?'].map({'Placed': 1, 'Not Placed': 0})
df['Backlog'] = df['Backlog in 5th sem'].map({'Yes': 1, 'No': 0})
df['Project'] = df['Innovative Project(Y/N)'].map({'Yes': 1, 'No': 0})
df['Tech_Course'] = df['Technical Course(Y/N)'].map({'Yes': 1, 'No': 0})
df['Training'] = df['Training(Y/N)'].map({'Yes': 1, 'No': 0})

print(df[['Internship', 'Placed', 'Backlog', 'Project', 'Tech_Course', 'Training', 'Cgpa']].corr()['Placed'].sort_values(ascending=False))


with_internship = df[df['Internship']==1]['Placed'].mean() * 100
without_internship = df[df['Internship']==0]['Placed'].mean() * 100

print(f"Placed WITH internship: {with_internship:.1f}%")
print(f"Placed WITHOUT internship: {without_internship:.1f}%")


with_project = df[df['Project']==1]['Placed'].mean() * 100
without_project = df[df['Project']==0]['Placed'].mean() * 100

print(f"Placed WITH project: {with_project:.1f}%")
print(f"Placed WITHOUT project: {without_project:.1f}%")

print(df.groupby('Internship')['Backlog'].mean())

print(df.groupby('Internship')['Cgpa'].mean())

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
        "Industry recognized cert": 25
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

score = placement_score(
    "Deployed project",
    "NPTEL/Coursera certificate",
    "No backlog",
    8.5,
    "Startup internship with stipend",
    "Good"
)

print("Placement Score:", score)