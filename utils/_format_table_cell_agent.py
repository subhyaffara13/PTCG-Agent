from typing import Any

def _format_table_cell_agent(value: Any) -> str:
    """Format a cell value for agent TSV output (ISO timestamps, tabs escaped)."""
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    return _single_line(str(value))

