from typing import Any

def build_input_fingerprint(
    tx: "InstructionTranslator",
    fn_args_vt: Any,
    kwargs: dict[str, Any],
) -> InputFingerprint:
    """Build an InputFingerprint by flattening (args, kwargs) via pytree.

    Uses _make_inlined(tx, pytree.tree_flatten) to recursively flatten
    the argument structure into leaf VTs, classifying each leaf as
    tensor/symnode/constant/module. Also records the TreeSpec so that
    cache lookups can verify structural equivalence.

    Fast path: when kwargs is empty and all args are already leaf VTs
    (tensor/symnode/constant/module), skip the expensive pytree flatten.
    """
    # Fast path: flat args, no kwargs — skip pytree machinery.
    if not kwargs:
        all_leaf = True
        for vt in fn_args_vt:
            if classify_vt(vt) is None:
                all_leaf = False
                break
        if all_leaf:
            return build_fingerprint_fast(fn_args_vt)

    return build_fingerprint_with_pytree(tx, fn_args_vt, kwargs)

