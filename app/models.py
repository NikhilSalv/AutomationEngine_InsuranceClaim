# models.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Patient:
    patient_id: str
    insurance_provider_id: str
    eligible: bool
    previous_procedures: List[str]  # CPT codes
    last_procedure_dates: dict  # {CPT_code: datetime}
    diagnosis_codes: List[str]  # ICD-10 codes

@dataclass
class ProcedureRequest:
    procedure_code: str  # CPT code
    diagnosis_code: str  # ICD-10
    urgent: bool
    physician_id: str
    clinical_summary: str
    timestamp: datetime

@dataclass
class RuleResult:
    status: str  # 'pass', 'fail', 'warn'
    reason: Optional[str] = None
