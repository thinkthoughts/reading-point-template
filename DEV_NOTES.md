I used statement_text rather than a second statement key, since YAML would otherwise treat the later key as a replacement for the metadata block. This distinction should carry into the reusable ES schema:

statement:
  id:
  title:
  repository:
  status:

statement_text: >
  The actual engineering statement.
