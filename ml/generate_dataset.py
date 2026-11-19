
from pathlib import Path

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
OUTPUT_FILE = DATA_DIR / "students.csv"


def generate_students(number_of_students: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(42)
                                    
    attendance = rng.integers(35, 101, number_of_students)
    assignment_completion = rng.integers(20, 101, number_of_students)
    quiz_average = rng.integers(20, 101, number_of_students)
    midterm_score = rng.integers(15, 101, number_of_students)
    previous_gpa = np.round(
        rng.uniform(4.0, 10.0, number_of_students), 2
    )

    # Synthetic demonstration label, not a validated academic diagnosis.
    risk_score = (
        0.30 * (100 - attendance)
        + 0.25 * (100 - assignment_completion)
        + 0.20 * (100 - quiz_average)
        + 0.25 * (100 - midterm_score)
    )

    academic_risk = np.where(risk_score >= 48, "At Risk", "On Track")

    departments = rng.choice(
        ["Computer Engineering", "Information Technology", "Electronics"],
        number_of_students,
    )

    semesters = rng.integers(1, 9, number_of_students)

    students = pd.DataFrame(
        {
            "student_id": [
                f"STU{i:04d}" for i in range(1, number_of_students + 1)
            ],
            "student_name": [
                f"Student {i:03d}"
                for i in range(1, number_of_students + 1)
            ],
            "department": departments,
            "semester": semesters,
            "attendance_percentage": attendance,
            "assignment_completion": assignment_completion,
            "quiz_average": quiz_average,
            "midterm_score": midterm_score,
            "previous_gpa": previous_gpa,
            "academic_risk": academic_risk,
        }
    )

    return students


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = generate_students()
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Generated {len(df)} synthetic student records.")
    print(f"Saved dataset to: {OUTPUT_FILE}")
    print("\nRisk label distribution:")
    print(df["academic_risk"].value_counts())
    print("\nFirst five records:")
    print(df.head().to_string(index=False))
