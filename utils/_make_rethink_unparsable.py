
def _make_rethink_unparsable(schema_keys: tuple[str, str, str]) -> str:
    """Build an unparsable-rethink template carrying this variant's schema."""
    a, b, c = schema_keys
    return f"""

Your previous response ended with:
{{previous_response}}

No valid action JSON could be extracted from that. Conclude your response
with your final action as JSON in a ```json fenced block, exactly as the
original instructions required:

```json
{{{{"action": "offer", "keep": {{{{"{a}": <int>, "{b}": <int>, "{c}": <int>}}}}}}}}
```
or
```json
{{{{"action": "agree"}}}}
```

For example: `{{{{"action": "offer", "keep": {{{{"{a}": 1, "{b}": 0, "{c}": 2}}}}}}}}`

The action you choose must also be legal in the current state.
"""

