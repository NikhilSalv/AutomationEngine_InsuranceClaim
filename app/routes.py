
from flask import Flask, request, jsonify, render_template
from app.models import Patient, ProcedureRequest, RuleResult
from app.engine import make_authorization_decision
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
import pdb
from app import app

import sys

formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Ensure logs directory exists
# if not os.path.exists('logs'):
#     os.mkdir('logs')

# # Configure logging
# log_file = 'logs/app.log'
# file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=5)
# file_handler.setLevel(logging.INFO)

# # Format logs
# formatter = logging.Formatter(
#     '%(asctime)s [%(levelname)s] - %(message)s'
# )
# file_handler.setFormatter(formatter)

# # Add handler to root logger
# logging.getLogger().addHandler(file_handler)
# logging.getLogger().setLevel(logging.INFO)


# app = Flask(__name__)
print("routes.py hit")
@app.route("/", methods=["GET"])
def form():
    logging.info(f"Home page visited at {datetime.now().isoformat()}")
    print("Fiding template")
    return render_template("index.html")

@app.route("/authorize", methods=["POST"])
def authorize():
    # pdb.set_trace()
    data = request.json
    print("API hit in routes.py")
    logging.info(f'API hit in routes.py')

    patient_data = data['patient']
    print(patient_data)
    
    # Parse last_procedure_dates from string to datetime
    last_procedure_dates_str = patient_data.get('last_procedure_dates', {})
    print("Last pricedures ______:", last_procedure_dates_str)
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

@app.route("/test", methods=["GET"])
def test():
    name = request.args.get('name', 'Guest')  # Default to 'Guest' if name not provided
    return f"Hello {name}"


if __name__ == '__main__':
    # print("Hi")
    # app.run(debug=True)
    app.run(debug=True, port=5000)