# tests/test_engine.py

import pytest
from datetime import datetime, timedelta
from app.models import Patient, ProcedureRequest
from app.engine import make_authorization_decision

def mock_patient():
    return Patient(
        patient_id="P001",
        insurance_provider_id="INS123",
        eligible=True,
        previous_procedures=["CT456"],
        last_procedure_dates={"MRI123": datetime.now() - timedelta(days=200)},
        diagnosis_codes=["DIA001"]
    )

def mock_request():
    return ProcedureRequest(
        procedure_code="MRI123",
        diagnosis_code="DIA001",
        urgent=False,
        physician_id="NEURO01",
        clinical_summary="Headache and dizziness.",
        timestamp=datetime.now()
    )

def test_authorization_approved():
    patient = mock_patient()
    request = mock_request()
    decision = make_authorization_decision(patient, request)
    assert decision["decision"] == "Approved"

def test_reject_due_to_eligibility():
    patient = mock_patient()
    patient.eligible = False
    request = mock_request()
    decision = make_authorization_decision(patient, request)
    assert decision["decision"] == "Rejected"
    assert "Patient not eligible for coverage." in decision["rules_triggered"][0]["reason"]

def test_pending_due_to_missing_pre_reqs():
    patient = mock_patient()
    patient.previous_procedures = []  # Missing CT scan before MRI
    request = mock_request()
    decision = make_authorization_decision(patient, request)
    assert decision["decision"] == "Pending Review"

def test_procedure_not_covered(monkeypatch):
    patient = mock_patient()
    request = mock_request()

    # Force the procedure to not be covered
    monkeypatch.setattr("app.rules.is_procedure_covered", lambda *args: False)

    decision = make_authorization_decision(patient, request)
    assert decision["decision"] == "Rejected"
    assert "Procedure not covered by insurance." in decision["rules_triggered"][0]["reason"]

def test_recent_procedure_done():
    patient = mock_patient()
    patient.last_procedure_dates["MRI123"] = datetime.now() - timedelta(days=90)

    request = mock_request()
    decision = make_authorization_decision(patient, request)
    assert decision["decision"] == "Rejected"
    assert "already done in last 6 months" in decision["rules_triggered"][0]["reason"]

def test_referral_required_but_missing(monkeypatch):
    patient = mock_patient()
    request = mock_request()

    monkeypatch.setattr("app.rules.requires_specialist_referral", lambda code: True)
    monkeypatch.setattr("app.rules.has_specialist_referral", lambda physician_id, code: False)

    decision = make_authorization_decision(patient, request)
    assert decision["decision"] == "Rejected"
    assert "Specialist referral required" in decision["rules_triggered"][0]["reason"]

