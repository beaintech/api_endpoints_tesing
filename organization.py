import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

# Basic config for Pipedrive & Reonic
PIPEDRIVE_API_TOKEN = os.getenv("PIPEDRIVE_API_TOKEN", "YOUR_API_TOKEN_HERE")
PIPEDRIVE_COMPANY_DOMAIN = os.getenv("PIPEDRIVE_COMPANY_DOMAIN", "yourcompany")
REONIC_API_BASE = os.getenv("REONIC_API_BASE", "http://localhost:8000")

PIPEDRIVE_BASE_URL = f"https://{PIPEDRIVE_COMPANY_DOMAIN}.pipedrive.com/v1"


class OrganizationCreate(BaseModel):
    """
    Minimal payload for creating an Organization in Pipedrive.
    Mirrors the Node.js tutorial example where only `name` is required.
    You can extend this later with address, label, owner_id, etc.
    """
    name: str
    owner_id: int | None = None
    visible_to: str | None = None
    address: str | None = None


@router.post("/add_organization")
async def add_organization(body: OrganizationCreate):
    """
    Create a (mocked) Pipedrive Organization.

    Tutorial equivalent of:
    POST https://{company}.pipedrive.com/v1/organizations?api_token=TOKEN

    This endpoint does not call the real Pipedrive API.
    It builds the request payload and returns a mocked response
    so you can inspect what would be sent.
    """

    if not PIPEDRIVE_API_TOKEN:
        raise HTTPException(status_code=400, detail="PIPEDRIVE_API_TOKEN is not set.")

    url = f"{PIPEDRIVE_BASE_URL}/organizations"
    params = {"api_token": PIPEDRIVE_API_TOKEN}

    payload = {
        "name": body.name,
        "owner_id": body.owner_id,
        "visible_to": body.visible_to,
        "address": body.address,
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    class MockResponse:
        def __init__(self, payload, status_code=201):
            self._payload = payload
            self.status_code = status_code

        def json(self):
            return self._payload

    mock_body = {
        "success": True,
        "request": {
            "method": "POST",
            "endpoint": url,
            "query_params": params,
            "json_body": payload,
        },
        "data": {
            "id": 301,
            "name": payload.get("name"),
            "owner_id": payload.get("owner_id"),
            "visible_to": payload.get("visible_to") or "3",
            "address": payload.get("address"),
            "created_from": "python-mock-organization-demo",
        },
    }

    resp = MockResponse(mock_body)

    try:
        data = resp.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON in mock Pipedrive response")

    if resp.status_code not in (200, 201) or not data.get("success"):
        raise HTTPException(
            status_code=resp.status_code,
            detail=data.get("error") or "Pipedrive error",
        )

    return JSONResponse(content=data, status_code=resp.status_code)
