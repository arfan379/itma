-- Override dbt's default generate_schema_name to use the custom_schema_name
-- directly, without prepending the profile's default schema.
-- This makes dbt output schemas: raw, staging, marts (not itma_raw, etc.)

{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
