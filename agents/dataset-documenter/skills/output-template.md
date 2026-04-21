# Skill: Output Template

Purpose: enforce a consistent markdown contract for downstream datamart-generation agents.

## File Naming

- Pattern: `<dataset>_doc.md`
- Examples: `public_doc.md`, `staging_doc.md`, `normalised_doc.md`

## Default Output Path

- `projects/dataset_documentation/`

## Required Sections in Order

1. **Header**
   - dataset, project, generation timestamp, authenticated service account

2. **Executive Summary**

3. **Dataset Inventory Table**
   - object_name, object_type, partitioning, clustering, freshness

4. **Schema Tables** (one per object)
   - column_name, type, nullable, description, semantic_role

5. **Join Rules Matrix**
   - left_object, right_object, join_condition, cardinality_estimate,
     join_type_recommended, confidence, rationale

6. **KPI Catalog**
   - kpi_name, formula, grain, source_objects, validation_notes

7. **Lineage**
   - direct dependencies, transitive dependencies, uncertainty notes

8. **Table Generation Queries (SELECT Logic)**
   - object_name, object_type
   - query_type: `dataform_sqlx` | `dataform_job` | `view_definition_select` | `unavailable`
   - lineage_sources (from Data Lineage API)
   - sql_text (full SQLX content when available, in fenced ```sql block)
   - notes

9. **Cross-Layer Linkage**
   - source_object, source_layer, target_object, target_layer,
     evidence_source (`data_lineage_api`), confidence (`confirmed`)

10. **Dataform Metadata Section**
    - lineage_api_status, project_number
    - dataform_repo, dataform_workspace, dataform_sqlx_path
    - dataform_sqlx_tables_found, sql_text_access

11. **Consumption Notes for Datamart Agent**
    - recommended sources, risks, assumptions

12. **Appendix**
    - limitations, permission-related blind spots
    - read-only compliance statement

## Output Quality Rules

- Use markdown tables with stable column ordering.
- Mark inferred values clearly (e.g. `[inferred]`).
- Keep assumptions explicit and testable.
- Do not expose secrets or key file contents in any section.
- SQL blocks must use fenced ```sql syntax.
