# 🩺 Automated Prior Authorization Engine

> Backend microservice to automate insurance prior authorization decisions for diagnostic procedures such as MRI, CT scans, etc.


Link : https://automationengineensuranceelaim-8437e9c4d0ee.herokuapp.com/ 


## 💼 Business Context

In the health insurance industry, **prior authorization** is a critical step required before certain medical procedures, treatments, or prescriptions can be carried out. One common example is an MRI (Magnetic Resonance Imaging), which is often expensive and needs to be medically justified.

Before performing such a procedure, the treating physician must submit a request for authorization to the patient’s health insurance provider. The insurer then evaluates whether the procedure is medically necessary, covered under the patient’s plan, and compliant with policy guidelines.

This process involves multiple stakeholders:

Physicians, who must provide supporting medical documentation.

Insurance providers, who must assess the request based on clinical criteria.

Patients, whose care may be delayed or denied based on the outcome.

The business goal is to streamline and automate the prior authorization process, making it faster, more transparent, and less burdensome for providers, insurers, and patients. This reduces administrative costs, minimizes delays in patient care, and improves overall efficiency in the healthcare system.

This system automates decision-making using structured and unstructured patient data, reducing turnaround time from days to seconds.

---

## ✅ Key Features

- ✅ Rule-based decision engine for prior authorizations
- 🧠 Modular, testable business rules
- 🧾 Audit logging with rule traceability
- 🔐 HIPAA compliance and immutable logs
- 🔄 JSON-based API for easy integration
- 📦 Flask microservice architecture

---

## 🧱 Components in Your System

- Patient & ProcedureRequest Data Models (models.py)

- Business Rules (rules.py)

- Decision Engine (engine.py)

- (Optional) External Data Sources (e.g., Insurance DB, Referral Directory)

- (Optional) Frontend or API to accept user input and show results

- (Optional) Logging / Monitoring / Auditing Layer

## 👨🏻‍💻 Technical Architecture 

                ┌────────────────────┐
                │  User/API Client   │
                └────────┬───────────┘
                         │
                         ▼
                ┌────────────────────┐
                │ Procedure Request  │
                │  + Patient Info    │
                └────────┬───────────┘
                         ▼
               ┌──────────────────────┐
               │  Authorization Engine│  ←────┐
               │     (engine.py)      │       │
               └────────┬─────────────┘       │
                        ▼                     │
         ┌────────────────────────────┐       │
         │  Rule Evaluation Layer     │       │
         │     (rules.py)             │       │
         └────────┬───────────────┬───┘       │
                  │               │           │
        ┌─────────▼───┐   ┌───────▼────────┐   │
        │ Coverage DB │   │ Referral Logic │───┘
        └─────────────┘   └────────────────┘
                  │
        ┌─────────▼──────────┐
        │ Diagnostic History │
        └────────────────────┘

                         │
                         ▼
               ┌───────────────────────┐
               │  Decision Builder     │
               │   (build_response)    │
               └────────┬──────────────┘
                        ▼
               ┌───────────────────────┐
               │  JSON Response Output │
               └───────────────────────┘


## 🔧 How Your Engine Uses This


Your rules in engine.py follow this logic:

- Check eligibility. If eligible is false, instantly reject.

- Check procedure coverage
Use insurance_provider_id + procedure_code

- Time constraint
If procedure already done recently (last_procedure_dates), reject unless urgent = true

- Specialist referral required?
If yes, then ensure physician_id is a specialist or has a referral

- Check prerequisites
Use previous_procedures to verify pre-steps

- Return decision
'Approved', 'Rejected', or 'Pending Review'
Along with which rules triggered the decision


## 📥 Schema Design

The system expects a JSON payload with the following structure:

```json
{
  "patient": {
    "patient_id": "P12345",
    "insurance_provider_id": "INS456",
    "eligible": true,
    "previous_procedures": ["XRAY001", "CT456"],
    "last_procedure_dates": {
      "MRI123": "2024-02-15T00:00:00"
    },
    "diagnosis_codes": ["R51", "G44"]
  },
  "procedure": {
    "procedure_code": "MRI123",
    "diagnosis_code": "R51",
    "urgent": false,
    "physician_id": "NEURO987",
    "clinical_summary": "Patient reports persistent headache."
  }
}

```

## 🔍 Patient Object (Real-life Context)

| **Field**              | **Meaning**                                            | **Why It Matters**                                                  |
|------------------------|--------------------------------------------------------|----------------------------------------------------------------------|
| `patient_id`           | Unique patient ID (e.g., medical record number)       | Needed to identify patient                                           |
| `insurance_provider_id`| Which insurance company covers the patient            | Determines coverage rules                                            |
| `eligible`             | `true` or `false` — is the patient covered currently? | If false, auto-reject claim                                          |
| `previous_procedures`  | List of prior procedures like X-ray, CT               | Used for dependency or prerequisite rule-checks                      |
| `last_procedure_dates` | Dict of procedure codes → date last done              | Checks time-based rules (e.g., MRI once in 6 months)                |
| `diagnosis_codes`      | ICD-10 codes (e.g., R51 = headache)                   | Used to validate medical necessity of procedure                      |


### 🔍 Procedure Object (Current Request Context)

| **Field**          | **Meaning**                                      | **Why It Matters**                                                  |
|--------------------|--------------------------------------------------|----------------------------------------------------------------------|
| `procedure_code`   | CPT code (e.g., MRI123) for the requested procedure | Key for rule-matching and coverage validation                    |
| `diagnosis_code`   | ICD-10 code relevant to the condition            | Ensures procedure matches diagnosis                                 |
| `urgent`           | If the doctor marks this as urgent               | Overrides time-window constraints                                   |
| `physician_id`     | ID of doctor making the request                  | May determine if specialist referral is needed                      |
| `clinical_summary` | Free-text from doctor explaining condition       | Provides context for manual or AI-based decision support            |

## PyTest

## ✅ Testing & Code Coverage

This project follows a robust testing approach using **`pytest`** to ensure correctness and confidence across all critical logic components such as the authorization engine, business rules, and API endpoints.

### 🧪 Test Structure

Tests are organized under the `app/tests/` directory and cover:

| **Test File**                | **Description**                                                                 |
|-----------------------------|---------------------------------------------------------------------------------|
| `test_api.py`               | End-to-end test for the `/authorize` API route using Flask test client          |
| `test_engine.py`            | Unit tests for the core authorization engine (`engine.py`) and rule flow logic |
| `test_rules.py`             | Tests for individual rule utility functions in `rules.py`                      |
| `__init__.py`               | Marks directories as test modules                                               |


## ✅ Testing & Code Coverage

This project follows a robust testing approach using **`pytest`** to ensure correctness and confidence across all critical logic components such as the authorization engine, business rules, and API endpoints.

### 🧪 Test Structure

Tests are organized under the `app/tests/` directory and cover:

| **Test File**                | **Description**                                                                 |
|-----------------------------|---------------------------------------------------------------------------------|
| `test_api.py`               | End-to-end test for the `/authorize` API route using Flask test client          |
| `test_engine.py`            | Unit tests for the core authorization engine (`engine.py`) and rule flow logic |
| `test_rules.py`             | Tests for individual rule utility functions in `rules.py`                      |
| `__init__.py`               | Marks directories as test modules                                               |

### 🛠️ Test Coverage

### 📊 Test Coverage Report

| **File**                    | **Statements** | **Missed** | **Coverage** |
|----------------------------|----------------|------------|--------------|
| `app.py`                   | 0              | 0          | 100%         |
| `app/__init__.py`          | 14             | 1          | 93%          |
| `app/engine.py`            | 31             | 4          | 87%          |
| `app/models.py`            | 23             | 0          | 100%         |
| `app/routes.py`            | 44             | 6          | 86%          |
| `app/rules.py`             | 11             | 0          | 100%         |
| `app/tests/__init_.py`     | 0              | 0          | 100%         |
| `app/tests/__init__.py`    | 0              | 0          | 100%         |
| `app/tests/test_api.py`    | 14             | 0          | 100%         |
| `app/tests/test_engine.py` | 76             | 0          | 100%         |
| `app/tests/test_rules.py`  | 10             | 0          | 100%         |
| `run.py`                   | 4              | 4          | 0%           |
| **Total**                  | **227**        | **15**     | **93%**      |


This report shows that **93%** of the total codebase is covered by tests. All critical components like the **authorization engine**, **rule logic**, and **API routes** have strong coverage. The only uncovered lines are in `run.py`, which serves as the entry-point script and typically has minimal logic.

> ✅ Most modules have 100% test coverage, ensuring high reliability and confidence in rule-based decisions.


You can run all tests using:

```bash
pytest
```


## Deployment and CI/CD.

This project uses **GitHub Actions** to automate testing, linting, and deployment to a **Heroku staging environment**.

### 🔄 CI/CD Pipeline Overview

The GitHub Actions workflow (`.github/workflows/python-app.yml`) is triggered on:

- Every push to the `main` branch
- Every pull request targeting the `main` branch

### ✅ What the Workflow Does

1. **Checkout Code**  
   Uses the `actions/checkout` action to pull the latest code.

2. **Set Up Python Environment**  
   Configures Python 3.10 using `actions/setup-python`.

3. **Install Dependencies**  
   Installs required packages from `requirements.txt`, including `flake8` for linting.

4. **Run Code Linting**  
   Runs `flake8` in two passes:
   - First to catch critical errors (`E9`, `F63`, etc.)
   - Second for style and complexity reporting (but doesn't fail the pipeline)

5. **Run Unit Tests**  
   Executes `pytest` to run all test cases and ensure the code works as expected.

6. **Deploy to Heroku (Staging)**  
   If all lint and test steps pass, it:
   - Installs the Heroku CLI
   - Deploys the app using `akhileshns/heroku-deploy` action
   - Uses the following secrets:
     - `HEROKU_API_KEY`
     - `HEROKU_APP_NAME`
     - `HEROKU_EMAIL`

### 🌐 Live Environment

The project is automatically deployed to a **Heroku staging environment**.  Below is the link.

https://automationengineensuranceelaim-8437e9c4d0ee.herokuapp.com/

You can configure production deployment in a similar way by adding a new job or modifying the app name and environment variables.

> Make sure you set the required secrets in your GitHub repository under **Settings → Secrets and variab**
