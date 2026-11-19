
from fastapi import FastAPI, HTTPException, Query

from backend.app.data_service import get_summary, load_students


app = FastAPI(
    title="Smart Campus & OBE API",
    description=(
        "API for synthetic student records and campus analytics."
    ),
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Smart Campus & OBE API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/summary")
def campus_summary():
    try:
        df = load_students()
        return get_summary(df)
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/students")
def list_students(
    department: str | None = None,
    risk: str | None = Query(default=None, pattern="^(At Risk|On Track)$"),
):
    try:
        df = load_students()
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if department:
        df = df[df["department"] == department]

    if risk:
        df = df[df["academic_risk"] == risk]

    # Convert NumPy scalar values into JSON-compatible Python values.
    return df.to_dict(orient="records")


@app.get("/students/{student_id}")
def get_student(student_id: str):
    try:
        df = load_students()
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    matches = df[df["student_id"] == student_id]

    if matches.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Student {student_id} was not found",
        )

    return matches.iloc[0].to_dict()
