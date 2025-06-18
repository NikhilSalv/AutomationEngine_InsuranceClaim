# tests/test_api.py

import json
# from app import app
from datetime import datetime, timedelta

def test_authorize_api_approved():
    # client = app.test_client()

    data = {
        "patient": {
            "patient_id": "P001",
            "insurance_provider_id": "INS123",
            "eligible": True,
            "previous_procedures": ["CT456"],
            "last_procedure_dates": {"MRI123": (datetime.now() - timedelta(days=200)).isoformat()},
            "diagnosis_codes": ["DIA001"]
        },
        "procedure": {
            "procedure_code": "MRI123",
            "diagnosis_code": "DIA001",
            "urgent": False,
            "physician_id": "NEURO01",
            "clinical_summary": "Severe headache",
        }
    }

    response = client.post("/authorize", data=json.dumps(data), content_type='application/json')
    body = response.get_json()
    assert response.status_code == 200
    assert body["decision"] == "Approved"
