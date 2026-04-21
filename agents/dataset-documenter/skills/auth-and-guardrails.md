# Skill: Authentication and Guardrails

Purpose: enforce secure, deterministic authentication with minimum privileges before any metadata analysis.

## Required Identity

- A dedicated service account with read-only permissions on the target GCP project.
- Minimum required roles:
  - `roles/bigquery.metadataViewer`
  - `roles/datalineage.viewer`
  - `roles/dataform.viewer`

## Input Parameters

- `service_account_key_file` — path to the JSON key file (never commit to repo)
- `project_id` — GCP project ID

## Execution Checklist

1. Validate key file exists at the specified path.
2. Activate service account: `gcloud auth activate-service-account --key-file <key_file>`
3. Set active project: `gcloud config set project <project_id>`
4. Read active account: `gcloud config get-value account`
5. Verify active account matches the expected service account exactly.
6. Abort with `AUTH_ACCOUNT_MISMATCH` if mismatch detected.

## Guardrails

- Never print `private_key` content from the JSON key.
- Never copy the key JSON into repository files or logs.
- Never proceed if the active account does not match.
- Keep all log events non-sensitive and concise.

## Read-Only Command Policy (Categorical)

Allowed command families:
- `gcloud auth`, `gcloud config`, `gcloud projects describe`
- `bq ls`, `bq show`
- `bq query` only when the query is a strictly read-only SELECT

Forbidden command patterns — block execution immediately:
- CREATE, UPDATE, DELETE, INSERT, MERGE, ALTER, DROP, TRUNCATE
- `bq mk`, `bq rm`

Preflight check before every query or command:
1. Convert command text to uppercase.
2. If it contains any forbidden pattern, abort with `READ_ONLY_POLICY_VIOLATION`.
3. Log only command class, never secrets.

## Expected Log Events

- `AUTH_START`
- `AUTH_ACCOUNT_VERIFIED`
- `AUTH_PROJECT_SET`
- `AUTH_OK`

## Failure Events

- `AUTH_KEYFILE_MISSING`
- `AUTH_ACCOUNT_MISMATCH`
- `AUTH_FAILED`
- `READ_ONLY_POLICY_VIOLATION`
