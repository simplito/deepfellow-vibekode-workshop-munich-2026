"""Patient Database MCP Server."""

import logging

from fastmcp import FastMCP
from fastmcp.server.http import StarletteWithLifespan
from pydantic import BaseModel

from database import query_by_skin_condition, query_psoriasis_at_risk, total_patients

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("patient-db-mcp")


class PatientSummary(BaseModel):
    """At-risk patient summary."""

    patient_id: str
    age: int
    risk_factors: list[str]


class QueryResult(BaseModel):
    """Result of a patient risk query."""

    disease: str
    total_patients: int
    at_risk_count: int
    patients: list[PatientSummary]


def create_app() -> StarletteWithLifespan:
    """Create MCP server app for uvicorn."""
    mcp = FastMCP("Patient Database", version="1.0.0")

    @mcp.tool()
    async def query_patients_at_risk(disease: str) -> QueryResult:
        """Query the synthetic patient database for patients at risk for the given disease.

        For 'psoriasis', matches patients with genetic markers, family history,
        or associated autoimmune conditions. For other diseases, matches by skin condition.
        """
        logger.info("Querying patients at risk for: %s", disease)

        rows = query_psoriasis_at_risk() if "psoriasis" in disease.lower() else query_by_skin_condition(disease)

        patients = [PatientSummary(**r) for r in rows]
        total = total_patients()
        logger.info("Found %d/%d patients at risk for %s", len(patients), total, disease)

        return QueryResult(
            disease=disease,
            total_patients=total,
            at_risk_count=len(patients),
            patients=patients,
        )

    return mcp.http_app()


app = create_app()
