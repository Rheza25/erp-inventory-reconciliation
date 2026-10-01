# ERP Inventory Reconciliation & Anomaly Detection Engine

## Executive Summary
Designed and developed a Python-based data reconciliation engine to automate inventory audits across 10 warehouse locations. The tool connects to an SQL database to ingest raw ERP transaction logs, calculates true expected inventory balances, and automatically isolates unauthorized system adjustments causing discrepancies between physical counts and system records.

## The Business Problem
The organization experienced persistent discrepancies between physical warehouse stock and the inventory recorded in the ERP system. After legitimate withdrawals were recorded, subsequent "phantom" transactions caused the ERP balance to unexpectedly increase. Because the ERP lacked a step-by-step transaction tracing workflow, these anomalies resulted in:
* Substantial manual effort from audit and finance teams.
* Delays in identifying the specific system behaviors causing data corruption.
* Misplaced suspicion of physical theft due to a lack of data visibility.

## Technical Architecture & Tools
* **Language/Libraries:** Python, Pandas, SQLite3
* **Environment:** VS Code, Git
* **Database:** Relational SQL database (`erp_system.db`)
* *Note: To protect confidential company information, all data used in this public repository was synthetically generated using a custom Python script, perfectly mimicking the real-world operational problem.*

## Deployment & Integration Architecture
This tool was built to integrate smoothly with live enterprise systems:
1. **SQL Database Connection:** The script bypasses flat files by connecting directly to the ERP's relational database (simulated here via SQLite).
2. **Automated Extraction:** It queries `starting_inventory`, `transactions`, and `physical_counts` tables using standard SQL.
3. **Scalable Processing:** Using Pandas, the engine processes thousands of transactions in milliseconds without burdening the live ERP server.

## Methodology & Logic
1. **Data Aggregation:** Utilizes Pandas `groupby()` to aggregate all warehouse receipts, withdrawals, and inter-warehouse transfers to calculate net inventory movement per item/location.
2. **Balance Reconstruction:** Merges net movements with opening balances to calculate a mathematically verified "Expected Balance."
3. **Variance Detection:** Merges auditor counts and calculates the variance, ignoring acceptable human counting errors (+/- 1 unit) while flagging systemic discrepancies.
4. **Root Cause Isolation:** Filters the transaction log to isolate unauthorized `System_Adjustment` entries, proving mathematically that phantom system transactions—not physical theft—caused the variance.

## Business Impact & Results
* **Reduced Audit Time:** Transformed a manual spreadsheet reconciliation process that took days into an algorithmic script that runs in under one second.
* **Restored Trust:** Replaced operational friction with mathematically proven data, verifying discrepancies were a system/process issue rather than malicious physical activity.
* **Automated Deliverables:** Automatically generates management-ready audit trails (`reconciliation_summary.csv` and `phantom_increase_audit_log.csv`).
