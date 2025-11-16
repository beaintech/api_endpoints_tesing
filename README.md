# Pipedrive Local Playground (FastAPI)

A fully local sandbox for simulating Pipedrive API calls using mocked data. This playground is designed for demonstrating how Pipedrive → Reonic integrations work without requiring any real credentials.

---

## Installation

pip install fastapi "uvicorn[standard]" python-dotenv

---

## Run Locally

uvicorn main:app --reload --port 8000

Server starts at:

http://localhost:8000

---

## Test Endpoints

OAuth Callback Test:
http://localhost:8000/callback?code=test

Mock Data Endpoints:
http://localhost:8000/mock/pipedrive
http://localhost:8000/mock/saas

Pipedrive Mock Endpoints:
http://localhost:8000/get_leads

Swagger UI:
http://localhost:8000/docs

---

## POST Examples

### Create a Lead (POST /create_lead)

Go to Swagger UI:
http://localhost:8000/docs

Open POST /create_lead → “Try it out” → paste:

{
  "title": "Lead 158",
  "amount": 3000,
  "currency": "USD",
  "owner_id": 13293848,
  "label_ids": ["f981d20f-cd00-4e30-a406-06576a92058b"],
  "person_id": 1,
  "organization_id": 1,
  "expected_close_date": "2025-07-12",
  "visible_to": "1",
  "was_seen": true
}

---

## Sync Leads (Pipedrive → Reonic)

Trigger the sync:
http://localhost:8000/sync_leads

This endpoint does NOT require a request body.

---

## Notes

• All responses are mocked – no real requests are sent to Pipedrive.  
• URL structure and payload format match real Pipedrive API behavior.  
• Safe for demos, onboarding, and planning integrations.  

