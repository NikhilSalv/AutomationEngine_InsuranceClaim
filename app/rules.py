# rules.py
from typing import List


def is_procedure_covered(insurance_id: str, procedure_code: str) -> bool:
    # Placeholder for insurance provider logic or DB lookup
    return procedure_code not in ['CPT9999']  # Simulated blacklist

def requires_specialist_referral(procedure_code: str) -> bool:
    # High-cost procedures require referral
    return procedure_code in ['MRI123', 'CT456']

def has_specialist_referral(physician_id: str, procedure_code: str) -> bool:
    # Placeholder: Check if referring physician is specialist
    return physician_id.startswith('NEURO')  # Simulated check

def has_required_prior_procedures(prev_procedures: List[str], procedure_code: str) -> bool:
    # Simulated logic
    if procedure_code == 'MRI123' and 'CT456' not in prev_procedures:
        return False
    return True
