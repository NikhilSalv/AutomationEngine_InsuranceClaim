# app.py

from flask import Flask, request, jsonify
from app.models import Patient, ProcedureRequest, RuleResult
from app.engine import make_authorization_decision
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.mkdir('logs')

# Configure logging
log_file = 'logs/app.log'
file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=5)
file_handler.setLevel(logging.INFO)

# Format logs
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] - %(message)s'
)
file_handler.setFormatter(formatter)

# Add handler to root logger
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)


app = Flask(__name__)

@app.route("/authorize", methods=["POST"])
def authorize():
    data = request.json

    patient_data = data['patient']
    
    # Parse last_procedure_dates from string to datetime
    last_procedure_dates_str = patient_data.get('last_procedure_dates', {})
    last_procedure_dates_dt = {
        k: datetime.fromisoformat(v) for k, v in last_procedure_dates_str.items()
    }
    patient_data['last_procedure_dates'] = last_procedure_dates_dt

    
    patient = Patient(**data['patient'])
    procedure = ProcedureRequest(
        **data['procedure'],
        timestamp=datetime.now()
    )
    logging.info(f'patient data : {patient}')
    
    decision = make_authorization_decision(patient, procedure)
    # return "Test"
    return jsonify(decision)

if __name__ == '__main__':
    app.run(debug=True)