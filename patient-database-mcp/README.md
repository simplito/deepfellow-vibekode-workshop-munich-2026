# patient-database-mcp

MCP server exposing a synthetic patient database for disease risk queries. Designed for psoriasis risk analysis — queries patients by genetic markers, family history, and autoimmune conditions.

## Database

SQLite database (`patients.db`) with 80 synthetic patients. Each patient has:

| Field | Type | Description |
|-------|------|-------------|
| `patient_id` | TEXT | Identifier (`P0001`–`P0080`) |
| `age` | INTEGER | 18–85 |
| `family_history_psoriasis` | BOOL | ~35% of patients |
| `hla_cw6_marker` | BOOL | HLA-Cw6 genetic marker, ~25% of patients |
| `autoimmune_conditions` | JSON array | 0–3 conditions from pool |
| `skin_conditions` | JSON array | 0–3 conditions from pool |

**Autoimmune pool**: Crohn's disease, rheumatoid arthritis, lupus, multiple sclerosis, type 1 diabetes, inflammatory bowel disease, psoriatic arthritis, ankylosing spondylitis, Hashimoto's thyroiditis, celiac disease

**Skin condition pool**: eczema, contact dermatitis, rosacea, vitiligo, seborrheic dermatitis, atopic dermatitis, urticaria, acne vulgaris

### Prepare the database

The database is generated automatically during Docker build. To (re)generate it locally:

```bash
uv run python generate_patients.py
# → Generated 80 patients, N at risk for psoriasis → patients.db
```

The script uses seed `42` — output is deterministic.

## MCP Tool

### `query_patients_at_risk`

Query patients at risk for a given disease.

**Parameter**: `disease: str`

**Behavior**:
- If `disease` contains `"psoriasis"` (case-insensitive): matches patients with any of:
  - `family_history_psoriasis = true`
  - `hla_cw6_marker = true`
  - Autoimmune condition containing: Crohn, rheumatoid, inflammatory bowel, lupus, psoriatic arthritis
- Otherwise: matches patients whose `skin_conditions` contains the disease string (LIKE match)

**Response**:
```json
{
  "disease": "psoriasis",
  "total_patients": 80,
  "at_risk_count": 42,
  "patients": [
    {
      "patient_id": "P0001",
      "age": 34,
      "risk_factors": [
        "family history of psoriasis",
        "HLA-Cw6 genetic marker"
      ]
    }
  ]
}
```

**Risk factor labels**:
| Matched condition | Label in response |
|---|---|
| `family_history_psoriasis` | `family history of psoriasis` |
| `hla_cw6_marker` | `HLA-Cw6 genetic marker` |
| Crohn's disease | `Crohn's disease (autoimmune)` |
| rheumatoid arthritis | `rheumatoid arthritis (autoimmune)` |
| inflammatory bowel disease | `inflammatory bowel disease (autoimmune)` |
| lupus | `lupus (autoimmune)` |
| psoriatic arthritis | `psoriatic arthritis (autoimmune)` |
| skin condition match | `existing skin condition: <disease>` |

## Usage

### Docker Compose

```bash
docker compose up --build
```

Database is generated inside the image at build time — no volume mount needed.

### Local

```bash
uv sync
uv run python generate_patients.py   # create patients.db
uv run uvicorn server:app --host 0.0.0.0 --port 8001
```

### MCP endpoint

```
http://localhost:8001/mcp
```

Port 8001 avoids conflict with DF Server running on 8000.

### Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector http://localhost:8001/mcp
```
