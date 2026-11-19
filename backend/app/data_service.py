
from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT_DIR / "data" / "students.csv"


def load_students() -> pd.DataFrame:
    """Load synthetic student data from the CSV file."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Student dataset not found at {DATA_FILE}. "
            "Run: python ml/generate_dataset.py"
        )

    df = pd.read_csv(DATA_FILE)

    required_columns = {
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
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Student dataset is missing columns: {sorted(missing)}"
        )

    return df


def get_summary(df: pd.DataFrame) -> dict:
    """Calculate basic campus-level academic statistics."""
    return {
        "total_students": int(len(df)),
        "average_attendance": round(
            float(df["attendance_percentage"].mean()), 2
        ),
        "average_gpa": round(float(df["previous_gpa"].mean()), 2),
        "students_at_risk": int(
            (df["academic_risk"] == "At Risk").sum()
        ),
        "departments": int(df["department"].nunique()),
    }

