# 🩺 Automated Prior Authorization Engine

> Backend microservice to automate insurance prior authorization decisions for diagnostic procedures such as MRI, CT scans, etc.

## 🎯 Goal

Automate the prior authorization process to reduce manual workload, avoid delays in patient care, and improve accuracy based on defined insurance, clinical, and eligibility rules.

---

## 💼 Business Context

In healthcare, **prior authorization** is often required by insurers before performing costly procedures. This system automates decision-making using structured and unstructured patient data, reducing turnaround time from days to seconds.

---

## ✅ Key Features

- ✅ Rule-based decision engine for prior authorizations
- 🧠 Modular, testable business rules
- 🧾 Audit logging with rule traceability
- 🔐 HIPAA compliance and immutable logs
- 🔄 JSON-based API for easy integration
- 📦 Flask microservice architecture

---

## 📥 Inputs

The system expects a JSON payload with the following structure:

```json
{
  "patient_id": "P123",
  "procedure_code": "MRI123",
  "diagnosis_code": "G40.9",
  "referring_physician_id": "NEURO456",
  "insurance_provider_id": "INS789",
  "previous_procedures": ["XRAY001", "CT002"],
  "clinical_notes_summary": "Patient has long-term migraines...",
  "urgent_flag": false
}
