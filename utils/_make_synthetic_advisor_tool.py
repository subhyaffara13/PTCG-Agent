from typing import Dict

def _make_synthetic_advisor_tool() -> Dict:
    """Build a regular tool definition the executor provider can understand."""
    return {
        "name": "advisor",
        "description": ADVISOR_TOOL_DESCRIPTION,
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question or challenge you want guidance on.",
                }
            },
            "required": ["question"],
        },
    }

