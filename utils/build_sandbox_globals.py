from typing import Any, Dict

def build_sandbox_globals() -> Dict[str, Any]:
    """Assemble the globals dict for executing guardrail code.

    Includes the LiteLLM-provided primitives (``regex_match``, ``http_get``,
    ``allow``/``block``/``modify``, etc.) plus the RestrictedPython guards
    that the compiled bytecode expects to find by name.
    """
    sandbox: Dict[str, Any] = get_custom_code_primitives().copy()
    sandbox["__builtins__"] = _build_sandbox_builtins()
    sandbox["_getattr_"] = safer_getattr
    sandbox["_getitem_"] = default_guarded_getitem
    sandbox["_getiter_"] = default_guarded_getiter
    sandbox["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
    sandbox["_write_"] = full_write_guard
    sandbox["_inplacevar_"] = _inplacevar_
    return sandbox

