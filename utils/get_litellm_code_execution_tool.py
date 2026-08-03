from typing import Any, Dict

def get_litellm_code_execution_tool() -> Dict[str, Any]:
    """
    Returns the litellm_code_execution tool definition in OpenAI format.

    This tool enables automatic code execution in a sandboxed environment
    when skills include executable Python code.
    """
    return {
        "type": "function",
        "function": {
            "name": LiteLLMInternalTools.CODE_EXECUTION.value,
            "description": "Execute Python code in a sandboxed environment. Use this to run code that generates files, processes data, or performs computations. Generated files will be returned directly.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"}
                },
                "required": ["code"],
            },
        },
    }

