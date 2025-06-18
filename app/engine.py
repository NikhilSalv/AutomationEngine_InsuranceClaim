# engine.py

from typing import List
from datetime import datetime, timedelta
from .models import Patient, ProcedureRequest, RuleResult
from .rules import is_procedure_covered, requires_specialist_referral, has_specialist_referral, has_required_prior_procedures
import logging
# from logging.handlers import RotatingFileHandler
# import os

# # Ensure logs directory exists
# if not os.path.exists('logs'):
#     os.mkdir('logs')

def make_authorization_decision(patient: Patient, request: ProcedureRequest) -> dict:
    triggered_rules: List[RuleResult] = []
    
    # Rule 1: Check eligibility
    if not patient.eligible:
        triggered_rules.append(RuleResult(status='fail', reason='Patient not eligible for coverage.'))
        return build_response('Rejected', triggered_rules)

    # Rule 2: Procedure coverage
    if not is_procedure_covered(patient.insurance_provider_id, request.procedure_code):
        triggered_rules.append(RuleResult(status='fail', reason='Procedure not covered by insurance.'))
        return build_response('Rejected', triggered_rules)

    # Rule 3: Time-based constraint (last 6 months)
    if request.procedure_code in patient.last_procedure_dates:
        last_done = patient.last_procedure_dates[request.procedure_code]
        if not request.urgent and (datetime.now() - last_done < timedelta(days=180)):
            diff = datetime.now() - last_done
            print(diff)
            triggered_rules.append(RuleResult(status='fail', reason='Procedure already done in last 6 months.'))
            return build_response('Rejected', triggered_rules)

    # Rule 4: Referral requirement (simulate lookup)
    if requires_specialist_referral(request.procedure_code):
        if not has_specialist_referral(request.physician_id, request.procedure_code):
            triggered_rules.append(RuleResult(status='fail', reason='Specialist referral required.'))
            return build_response('Rejected', triggered_rules)

    # Rule 5: Diagnostic pre-steps
    if not has_required_prior_procedures(patient.previous_procedures, request.procedure_code):
        triggered_rules.append(RuleResult(status='warn', reason='Missing prerequisite procedures.'))
        return build_response('Pending Review', triggered_rules)

    # Passed all rules
    triggered_rules.append(RuleResult(status='pass', reason='All rules passed.'))
    return build_response('Approved', triggered_rules)


def build_response(decision: str, rule_results: List[RuleResult]) -> dict:
    return {
        'decision': decision,
        'timestamp': datetime.now().isoformat(),
        'rules_triggered': [r.__dict__ for r in rule_results]
    }
