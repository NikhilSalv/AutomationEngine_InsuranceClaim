# tests/test_rules.py

from rules import is_procedure_covered, requires_specialist_referral, has_required_prior_procedures

def test_covered_procedure():
    assert is_procedure_covered("INS001", "MRI123") is True
    assert is_procedure_covered("INS001", "CPT9999") is False

def test_requires_specialist():
    assert requires_specialist_referral("MRI123") is True
    assert requires_specialist_referral("XRAY789") is False

def test_required_pre_reqs():
    assert has_required_prior_procedures(["CT456"], "MRI123") is True
    assert has_required_prior_procedures([], "MRI123") is False
