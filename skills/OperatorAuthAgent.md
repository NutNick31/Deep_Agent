# Operator Authentication Investigation Guide

This guide is for analyzing operator authentication anomalies using the Operator_Auth dataset schema.

## Mandatory Rules

1. Read operator_id from signal.data.entity_id and use it exactly as-is.
2. Never modify IDs, numeric values, timestamps, or threshold values from the signal.\
3. Use signal.data.feature_value and signal.data.feature_threshold only to decide whether investigation is required.
4. If signal.data.feature_value > signal.data.feature_threshold, explicitly state threshold is breached and proceed with investigation.
5. If signal.data.feature_value <= signal.data.feature_threshold, state threshold is not breached and finish without fraud verdict unless explicit evidence is still provided.
6. Do not claim a check was done unless a tool result is present in evidence.
7. Always consider the result given by tools/DB rows as the primary basis for any conclusion.
8. If pre-fetched DB rows are provided by the manager, treat them as primary evidence.
9. Do not claim containment or remediation actions were executed unless an action tool result is present.
10. Do not search local directories or claim file-based evidence; there are no usable local files in this workflow.
11. Use only tool-delivered evidence and the signal payload to analyze the case.
12. Do not use threshold breach alone to classify suspicious/high risk; classification must come from fetched DB evidence.

## Operator_Auth Schema (CSV)

Use these exact columns while reasoning:

- Event ID
- Auth Code
- Event Timestamp
- Req Date Time
- Opt ID
- Enrolment Reference ID
- Aua
- Sa
- Asa
- Auth Result
- Error Code
- Sub Error Code
- Auth Duration
- Auth Type
- Registered Device Software ID
- Registered Device Software Version
- Device Provider ID
- Model ID
- Device Code
- Cert Expiry Date
- Device Meta Data
- Pid Size
- Face Match Score
- Face Match Type
- Face Sdk Version
- Face Used
- Face Fusion Done
- Fdc
- Finger Match Threshold
- Fmr Sdk Version
- Finger Match Score
- Fmr Count
- Fir Count
- Finger Fusion Performed
- Idc
- Iris Fusion Performed
- Location State Code
- Location District Code
- Resident State Code
- Resident District Code
- Otp Identifier
- Server ID
- Kafka Source Timestamp

## Field Mapping For Analysis

- auth instance -> Auth Code
- operator_id -> Opt ID
- event time -> Event Timestamp, Req Date Time, Kafka Source Timestamp
- pass/fail status -> Auth Result, Error Code, Sub Error Code
- auth mode -> Auth Type
- device identity -> Device Code, Model ID, Device Provider ID, Registered Device Software ID, Registered Device Software Version
- biometric signals -> Face Match Score, Face Used, Face Fusion Done, Finger Match Score, Fmr Count, Fir Count, Finger Fusion Performed, Iris Fusion Performed
- location context -> Location State Code, Location District Code, Resident State Code, Resident District Code
- latency/performance -> Auth Duration, Pid Size
- infrastructure path -> Server ID, Aua, Sa, Asa

## Feature Name Scenarios

The manager will pass one of the following `feature_name` values from the signal.
Treat the selected value as the investigation scenario and focus on the matching rows/fields.
Add your detailed investigation instructions under each heading.

### 1. high_frequency_auth_transactions
<!-- Description: If an operator is trying to authenticate himself/herself rapidly within a 2 minute window, it is considered as suspicious -->
Description: Detects automated or "brute-force" behavior where an operator attempts to authenticate multiple times within a 2-minute window. Rapid-fire attempts often indicate a script or bot is being used to bypass security controls.

### 2. device_sharing
<!-- Description: If an operator has authenticated himself/herself in multiple devices within a gap of 1 day, then the operator is considered suspicious -->
Description: Flags potential credential sharing or account takeover. This occurs when a single operator’s credentials are used across multiple distinct physical devices within a 24-hour period, violating "single-user-single-device" security protocols.

### 3. geo_inconsistency
<!-- Description: If an operator's location is changing rapidly then it is considered suspicious -->
Description: Identifies "impossible travel" scenarios. If an operator’s login location shifts between distant geographic points faster than physically possible by standard travel, it suggests the account has been compromised or accessed via a proxy/VPN to mask the user's true location.

Critical output rule for this scenario:
- If feature_name is geo_inconsistency, your Risk Findings and Final Classification must be primarily based on these fields: Location State Code, Location District Code, Resident State Code, Resident District Code.
- Do not make rapid-repeat timing the primary reason in this scenario unless geo fields are absent; if used, keep it as secondary context.
- Explicitly mention unique resident/location codes and explain why they indicate geo inconsistency or why evidence is insufficient.


### 4. biometric_abuse
<!-- Description: If an operator has used silicone to authenticate himself, then the operator is considered suspicious -->
Description: Detects the use of synthetic artifacts (such as silicone molds, high-resolution photos, or "gummy fingers") during the biometric capture process. This indicates a deliberate attempt to deceive sensors and bypass live-tissue detection.


### 5. time_anomalies
<!-- Description: If an operator has carried out transactions post 10:00 pm and pre 8:00 am, then the operator is considered as suspicious -->
Description: Flags "out-of-hours" activity occurring between 10:00 PM and 8:00 AM. Transactions during these non-standard windows are highly suspicious as they bypass daytime supervision and typical operational monitoring.

Alias handling:
- Treat `time_anomaly` and common misspellings like `time_anaomaly` as `time_anomalies`.

Critical output rule for this scenario:
- If feature_name is time_anomaly/time_anomalies, your first Risk Findings bullet must be time-focused.
- Prioritize evidence from Event Timestamp, Req Date Time, and Kafka Source Timestamp.
- Explicitly report out-of-hours activity and rapid burst intervals before discussing other dimensions.


### 6. failure_success_bursts
<!-- Description: If after multiple failure attempts, an operator is authenticated, and if the duration between all of them is within a few seconds, it is considered as suspicious -->
Description: Identifies "persistence patterns" where a series of rapid authentication failures is immediately followed by a successful login within seconds. This pattern often suggests a user is cycling through credentials or exploiting a system lag to gain unauthorized entry.

## Required Investigation Steps

1. Validate signal context.
  - Capture feature_name, feature_value, feature_threshold, signal_name, entity_id.
  - Compute threshold status correctly using numeric comparison.
  - Use this status only as investigation gating input.

2. Fetch operator evidence.
  - First use pre-fetched DB evidence (if present) from manager context.
  - If missing, choose exactly one scenario tool using feature_name and call it with Opt ID equal to signal.data.entity_id:
    - high_frequency_auth_transactions or high_frequency_auth_transaction -> scan_db_for_operator_auth_high_frequency_auth_transactions
    - device_sharing -> scan_db_for_operator_auth_device_sharing
    - geo_inconsistency -> scan_db_for_operator_auth_geo_inconsistency
    - biometric_abuse -> scan_db_for_operator_auth_biometric_abuse
    - time_anomaly, time_anomalies, time_anaomaly, time_anamoly -> scan_db_for_operator_auth_time_anomalies
    - failure_success_bursts -> scan_db_for_operator_auth_failure_success_bursts
  - Do not call more than one scenario tool for the same request unless the manager explicitly asks for cross-scenario comparison.
  - Record exact returned evidence fields: total_auth_records, time_window, distributions, suspicious_transactions, operator_rows, sample_rows.

3. Analyze authentication volume.
  - Count records for Opt ID.
  - Compare observed count/behavior against feature_name intent such as high_frequency_auth_transaction.

4. Analyze failures and retries.
  - Review Auth Result distribution.
  - Check Error Code and Sub Error Code repetition.
  - Flag repeated fail->retry bursts.

5. Analyze device integrity and sharing indicators.
  - Check Device Code consistency for the operator.
  - Flag frequent switches in Device Code or Model ID.
  - Flag suspicious concentration on a single Server ID with abnormal bursts.

6. Analyze time and geo consistency.
  - Check tight timestamp bursts in Event Timestamp.
  - Compare Location State/District with Resident State/District for abrupt mismatches.

7. Analyze biometric quality indicators when available.
  - Review Face Match Score and Finger Match Score trends.
  - Use Fmr Count/Fir Count spikes as potential misuse indicators.

8. Produce final classification.
  - suspicious/high risk only when fetched DB evidence supports anomaly.
  - not suspicious when fetched DB evidence does not indicate anomaly.
  - never classify solely from feature_value vs feature_threshold.

## Decision Policy

- Highest priority signal: pre-fetched/operator tool evidence (especially operator_rows, total_auth_records, suspicious_transactions).
- Second priority: consistency checks across Auth Result, device, time, and location fields.
- Threshold status from feature_value and feature_threshold is only an investigation trigger, not a verdict source.

If any higher priority rule indicates suspicion, lower priority checks cannot override it.

## Output Template

Return findings in this exact structure:

1. Signal Summary
  - operator_id
  - signal_name
  - feature_name
  - feature_value
  - feature_threshold
  - threshold_status (BREACHED or NOT_BREACHED)

2. Tool Evidence
  - selected scenario tool evidence snapshot
  - total_auth_records
  - suspicious_transactions count
  - supporting observations from relevant schema columns

3. Risk Findings
  - volume findings
  - failure/retry findings
  - device findings
  - time/geo findings
  - biometric findings (if present)

Scenario-priority requirement:
- The first bullet under Risk Findings must address the active feature_name scenario.
- For geo_inconsistency, the first bullet must be geo findings from resident/location code evidence.

4. Final Classification
  - suspicious or not suspicious
  - risk_level: low/medium/high
  - one-line rationale tied to exact evidence fields and values

5. Recommended Action
  - monitor / manual review / immediate containment

6. Suspicious Transactions
  - Return the Auth Code of all the suspicious transactions
  - Add the Sid of the transaction as well

7. Investigation Plan
  - Begin with a short plan describing what you will analyze and in what order for the active feature_name.

## Prohibited Behavior

- Do not invent values that are not in the signal or tool output.
- Do not state feature_value is below threshold when numeric comparison shows otherwise.
- Do not provide a clean verdict without citing tool evidence.
- Do not use filesystem discovery, local directory inspection, or guessed file paths as evidence.
- Do not classify suspicious/not suspicious from threshold breach alone.