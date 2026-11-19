
import os

import pandas as pd
import requests
import streamlit as st


API_URL = os.getenv("CAMPUS_API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Smart Campus & OBE",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 AI-Driven Smart Campus & OBE Ecosystem")
st.caption(
    "Campus intelligence dashboard | Synthetic demonstration data"
)


@st.cache_data(ttl=15)
def fetch_json(endpoint: str):
    response = requests.get(
        f"{API_URL}{endpoint}",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


try:
    summary = fetch_json("/summary")
    students = fetch_json("/students")
except requests.RequestException as exc:
    st.error(
        "Cannot connect to the FastAPI backend. "
        "Start it in another terminal with:\n\n"
        "uvicorn backend.app.main:app --reload"
    )
    st.caption(f"Connection details: {exc}")
    st.stop()

df = pd.DataFrame(students)

# Sidebar filters
st.sidebar.header("Filters")

departments = ["All"] + sorted(df["department"].unique().tolist())
selected_department = st.sidebar.selectbox(
    "Department",
    departments,
)

risk_options = ["All", "At Risk", "On Track"]
selected_risk = st.sidebar.selectbox(
    "Academic status",
    risk_options,
)

filtered_df = df.copy()

if selected_department != "All":
    filtered_df = filtered_df[
        filtered_df["department"] == selected_department
    ]

if selected_risk != "All":
    filtered_df = filtered_df[
        filtered_df["academic_risk"] == selected_risk
    ]

# Campus-level summary
st.subheader("Campus Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", summary["total_students"])
col2.metric(
    "Average Attendance",
    f'{summary["average_attendance"]:.1f}%',
)
col3.metric("Average Previous GPA", f'{summary["average_gpa"]:.2f}/10')
col4.metric("Students At Risk", summary["students_at_risk"])

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Academic Status Distribution")
    risk_counts = (
        filtered_df["academic_risk"]
        .value_counts()
        .reindex(["At Risk", "On Track"], fill_value=0)
    )
    st.bar_chart(risk_counts)

with right:
    st.subheader("Average Attendance by Department")
    attendance = (
        filtered_df.groupby("department")["attendance_percentage"]
        .mean()
        .round(1)
    )
    st.bar_chart(attendance)

# Student table
st.divider()
st.subheader("Student Records")

st.caption(
    f"Showing {len(filtered_df)} of {len(df)} synthetic student records."
)

display_columns = [
    "student_id",
    "student_name",
    "department",
    "semester",
    "attendance_percentage",
    "assignment_completion",
    "quiz_average",
    "midterm_score",
    "previous_gpa",
    "academic_risk",
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True,
)

# Student detail lookup
st.subheader("Student Detail Lookup")

student_ids = filtered_df["student_id"].tolist()

if student_ids:
    selected_student = st.selectbox(
        "Select a student",
        student_ids,
    )

    try:
        detail = fetch_json(f"/students/{selected_student}")

        a, b, c = st.columns(3)
        a.metric(
            "Attendance",
            f'{detail["attendance_percentage"]}%',
        )
        b.metric(
            "Midterm Score",
            f'{detail["midterm_score"]}/100',
        )
        c.metric(
            "Previous GPA",
            f'{detail["previous_gpa"]}/10',
        )

        st.write(f'**Department:** {detail["department"]}')
        st.write(f'**Semester:** {detail["semester"]}')
        st.write(f'**Synthetic status:** {detail["academic_risk"]}')

    except requests.RequestException as exc:
        st.warning(f"Unable to load student details: {exc}")
else:
    st.info("No students match the selected filters.")

st.divider()
st.caption(
    "Prototype only. Academic records and risk labels are synthetic. "
    "The current dashboard is not an accreditation or decision system."
)
