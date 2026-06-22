"""Generate synthetic patient database for psoriasis risk demo."""

import json
import random
import sqlite3
from pathlib import Path

SEED = 42
NUM_PATIENTS = 80
DB_PATH = Path(__file__).parent / "patients.db"

AUTOIMMUNE_POOL = [
    "Crohn's disease",
    "rheumatoid arthritis",
    "lupus",
    "multiple sclerosis",
    "type 1 diabetes",
    "inflammatory bowel disease",
    "psoriatic arthritis",
    "ankylosing spondylitis",
    "Hashimoto's thyroiditis",
    "celiac disease",
]

SKIN_CONDITIONS_POOL = [
    "eczema",
    "contact dermatitis",
    "rosacea",
    "vitiligo",
    "seborrheic dermatitis",
    "atopic dermatitis",
    "urticaria",
    "acne vulgaris",
]

PSORIASIS_AUTOIMMUNE = frozenset([
    "Crohn's disease",
    "rheumatoid arthritis",
    "inflammatory bowel disease",
    "lupus",
    "psoriatic arthritis",
])


def _random_subset(pool: list[str], rng: random.Random, max_count: int = 3) -> list[str]:
    count = rng.choices([0, 1, 2, 3], weights=[50, 30, 15, 5])[0]
    count = min(count, max_count, len(pool))
    return rng.sample(pool, count)


def generate(num: int = NUM_PATIENTS, seed: int = SEED) -> list[dict]:  # type: ignore[type-arg]
    rng = random.Random(seed)
    patients = []

    for i in range(1, num + 1):
        patient_id = f"P{i:04d}"
        age = rng.randint(18, 85)

        # ~35% family history, ~25% HLA-Cw6
        family_history = rng.random() < 0.35
        hla_cw6 = rng.random() < 0.25

        autoimmune = _random_subset(AUTOIMMUNE_POOL, rng)
        skin = _random_subset(SKIN_CONDITIONS_POOL, rng)

        patients.append({
            "patient_id": patient_id,
            "age": age,
            "family_history_psoriasis": family_history,
            "hla_cw6_marker": hla_cw6,
            "autoimmune_conditions": autoimmune,
            "skin_conditions": skin,
        })

    return patients


def create_db(patients: list[dict], path: Path = DB_PATH) -> None:  # type: ignore[type-arg]
    path.unlink(missing_ok=True)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE patients (
            patient_id TEXT PRIMARY KEY,
            age INTEGER NOT NULL,
            family_history_psoriasis INTEGER NOT NULL,
            hla_cw6_marker INTEGER NOT NULL,
            autoimmune_conditions TEXT NOT NULL,
            skin_conditions TEXT NOT NULL
        )
    """)
    for p in patients:
        cur.execute(
            "INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?)",
            (
                p["patient_id"],
                p["age"],
                int(p["family_history_psoriasis"]),
                int(p["hla_cw6_marker"]),
                json.dumps(p["autoimmune_conditions"]),
                json.dumps(p["skin_conditions"]),
            ),
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    patients = generate()
    create_db(patients)
    at_risk = sum(
        1 for p in patients
        if p["family_history_psoriasis"]
        or p["hla_cw6_marker"]
        or bool(PSORIASIS_AUTOIMMUNE & set(p["autoimmune_conditions"]))
    )
    print(f"Generated {len(patients)} patients, {at_risk} at risk for psoriasis → {DB_PATH}")
