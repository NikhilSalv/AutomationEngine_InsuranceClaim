# tests/test_api.py

import json
from app import app
from datetime import datetime, timedelta
import pdb

def test_authorize_api_approved():
    client = app.test_client()

    data = {
    "patient": {
            "patient_id": "P001",
            "insurance_provider_id": "INS123",
            "eligible": True,
            "previous_procedures": ["CT456"],
            "last_procedure_dates": {
      "MRI123": "2024-02-15T00:00:00"
    },
            "diagnosis_codes": ["DIA001"]
        },
        "procedure": {
            "procedure_code": "MRI123",
            "diagnosis_code": "DIA001",
            "urgent": True,
            "physician_id": "NEURO01",
            "clinical_summary": "Severe headache"
        }
    }
    data1 = {
    "patient": {
            "patient_id": "P001",
            "insurance_provider_id": "INS123",
            "eligible": True,
            "previous_procedures": ["CT456"],
            "last_procedure_dates": {
      "MRI123": "2024-02-15T00:00:00"
    },
            "diagnosis_codes": ["DIA001"]
        },
        "procedure": {
            "procedure_code": "MRI123",
            "diagnosis_code": "DIA001",
            "urgent": True,
            "physician_id": "NEURO01",
            "clinical_summary": "Severe headache"
        }
    }
    # pdb.set_trace()

    response = client.post("/authorize", data=json.dumps(data), content_type='application/json')
    body = response.get_json()
    print("Status code:", response.status_code)
    print("Response body:", body)
    assert response.status_code == 200
    assert body["decision"] == "Approved"
