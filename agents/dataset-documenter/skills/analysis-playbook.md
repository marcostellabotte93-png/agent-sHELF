# Skill: Analysis Playbook

Purpose: maximize coverage and quality of dataset documentation with fast metadata-first analysis.

## Non-Negotiable Constraint

Analysis must remain read-only at all times.

Never execute operations that create, modify, or delete cloud objects/data.
Forbidden keywords: CREATE, UPDATE, DELETE, INSERT, MERGE, ALTER, DROP, TRUNCATE.
If a step would require one of these operations, stop and report `READ_ONLY_POLICY_VIOLATION`.

## Input Parameters

- project_id
- dataset_id
- location
- optional Dataform context

## Analysis Order

1. Inventory
- List tables, views, materialized views.
- Capture partitioning and clustering metadata.

2. Schemas
- Extract column name, type, nullability, description.
- Infer semantic role: key, measure, dimension, timestamp, technical.

3. Join Rules
- Derive explicit joins from known keys and constraints.
- Infer implicit joins by naming and lineage.
- Add confidence and rationale for each rule.

4. KPI Discovery
- Parse view logic and metadata notes for formulas.
- Normalize KPI definitions and grain.
- Add validation notes and caveats.

5. SQL and DDL Recovery
- Extract `ddl` from region-level `INFORMATION_SCHEMA.TABLES` when available.
- Extract `view_definition` from `INFORMATION_SCHEMA.VIEWS` for views.
- Read SQLX files directly from Dataform workspace (primary source).
- Preserve SQL text as read-only evidence of how objects are generated.
- If SQL is unavailable for an object, mark as `not_available` with reason.

6. BigQuery Lineage
- Use Cloud Data Lineage API (`datalineage.googleapis.com/v1`) with `searchLinks` endpoint.
- Requires project number (not ID) in the URL path.
- Fallback to parsing view SQL dependencies.
- Build direct and transitive dependency maps.

7. Cross-Layer Linkage (staging/public)
- Use Lineage API to detect references across datasets in the same project.
- Build object-to-object links with confidence and evidence.
- Highlight links required for downstream datamart generation.

8. Dataform Enrichment
- Fetch SQLX files from Dataform workspace via `queryDirectoryContents` + `readFile` API.
- Path pattern: `definitions/<prefix>/<dataset>/<table>.sqlx`
- Reconcile with BigQuery lineage and report mismatches.

## Quality Gates

- Documentation contains inventory, schema tables, join matrix, KPI catalog, lineage section.
- Documentation contains SQL/DDL recovery section and cross-layer linkage section.
- If dataset has multiple objects, join matrix cannot be empty.
- If lineage is partial, flag uncertainty explicitly.

## Performance Notes

- Prefer metadata endpoints over data scans.
- Batch metadata requests when possible.
- Use deterministic sorting for stable outputs.
- Validate every command against read-only policy before execution.
