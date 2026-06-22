"""SQLite query logic for patient database."""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "patients.db"

PSORIASIS_AUTOIMMUNE_MARKERS = [
    "Crohn",
    "rheumatoid",
    "inflammatory bowel",
    "lupus",
    "psoriatic arthritis",
]

RISK_LABEL_MAP = {
    "family_history": "family history of psoriasis",
    "hla_cw6": "HLA-Cw6 genetic marker",
    "Crohn": "Crohn's disease (autoimmune)",
    "rheumatoid": "rheumatoid arthritis (autoimmune)",
    "inflammatory bowel": "inflammatory bowel disease (autoimmune)",
    "lupus": "lupus (autoimmune)",
    "psoriatic arthritis": "psoriatic arthritis (autoimmune)",
}


def _build_risk_factors(row: sqlite3.Row) -> list[str]:
    factors: list[str] = []
    if row["family_history_psoriasis"]:
        factors.append(RISK_LABEL_MAP["family_history"])
    if row["hla_cw6_marker"]:
        factors.append(RISK_LABEL_MAP["hla_cw6"])
    autoimmune: list[str] = json.loads(row["autoimmune_conditions"])
    for marker in PSORIASIS_AUTOIMMUNE_MARKERS:
        if any(marker.lower() in c.lower() for c in autoimmune):
            factors.append(RISK_LABEL_MAP[marker])
    return factors


def query_psoriasis_at_risk(db_path: Path = DB_PATH) -> list[dict]:  # type: ignore[type-arg]
    like_clauses = " OR ".join(
        f"autoimmune_conditions LIKE '%{m}%'" for m in PSORIASIS_AUTOIMMUNE_MARKERS
    )
    sql = f"""
        SELECT * FROM patients
        WHERE family_history_psoriasis = 1
           OR hla_cw6_marker = 1
           OR {like_clauses}
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "patient_id": row["patient_id"],
            "age": row["age"],
            "risk_factors": _build_risk_factors(row),
        }
        for row in rows
    ]


def query_by_skin_condition(disease: str, db_path: Path = DB_PATH) -> list[dict]:  # type: ignore[type-arg]
    sql = "SELECT * FROM patients WHERE skin_conditions LIKE ?"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, (f"%{disease}%",))
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "patient_id": row["patient_id"],
            "age": row["age"],
            "risk_factors": [f"existing skin condition: {disease}"],
        }
        for row in rows
    ]


def total_patients(db_path: Path = DB_PATH) -> int:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM patients")
    count: int = cur.fetchone()[0]
    conn.close()
    return count
