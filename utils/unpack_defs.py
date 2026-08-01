
def unpack_defs(
    schema: dict,
    defs: dict,
    max_inlined_bytes: Optional[int] = None,
) -> None:
    """Expand *all* ``$ref`` entries pointing into ``$defs`` / ``definitions``.

    This utility walks the entire schema tree (dicts and lists) so it naturally
    resolves references hidden under any keyword – ``items``, ``allOf``,
    ``anyOf``, ``oneOf``, ``additionalProperties``, etc.

    It mutates *schema* in-place and does **not** return anything.  The helper
    keeps memory overhead low by resolving nodes as it encounters them rather
    than materialising a fully dereferenced copy first.

    ``max_inlined_bytes`` caps the cumulative JSON-byte size of every target
    that has been inlined and is checked *before* each ``copy.deepcopy``, so
    an oversized expansion is rejected without first materialising it. A byte
    bound is the universal measure of expansion -- it simultaneously caps
    ref-count fan-out, node-count amplification, and scalar-byte amplification
    (a target containing a large string, ``const``, or ``enum`` entry).
    Defaults to ``None`` (unbounded) so existing callers are unaffected;
    raises ``ValueError`` on overflow.
    """

    import copy
    from collections import deque

    # Combine the defs handed down by the caller with defs/definitions found on
    # the current node.  Local keys shadow parent keys to match JSON-schema
    # scoping rules.
    root_defs: dict = {
        **defs,
        **schema.get("$defs", {}),
        **schema.get("definitions", {}),
    }

    # Use iterative approach with queue to avoid recursion
    # Each item in queue is (node, parent_container, key/index, active_defs, ref_chain)
    queue: deque[
        tuple[Any, Union[dict, list, None], Union[str, int, None], dict, set]
    ] = deque([(schema, None, None, root_defs, set())])
    inlined_bytes = 0

    while queue:
        node, parent, key, active_defs, ref_chain = queue.popleft()

        # ----------------------------- dict -----------------------------
        if isinstance(node, dict):
            # --- Case 1: this node *is* a reference ---
            if "$ref" in node:
                ref_name = node["$ref"].split("/")[-1]

                # Check for circular reference in the resolution chain
                if ref_name in ref_chain:
                    # Circular reference detected - leave as-is to prevent infinite recursion
                    continue

                target_schema = active_defs.get(ref_name)
                # Unknown reference – leave untouched
                if target_schema is None:
                    continue

                if max_inlined_bytes is not None:
                    inlined_bytes += _estimate_json_bytes(target_schema)
                    if inlined_bytes > max_inlined_bytes:
                        raise ValueError(
                            f"unpack_defs: inlined schema exceeded the "
                            f"{max_inlined_bytes:,}-byte budget. Refusing to "
                            f"deep-copy further to prevent schema-bomb "
                            f"resource exhaustion."
                        )

                # Merge defs from the target to capture nested definitions
                child_defs = {
                    **active_defs,
                    **target_schema.get("$defs", {}),
                    **target_schema.get("definitions", {}),
                }

                # Replace the reference with resolved copy
                resolved = copy.deepcopy(target_schema)
                if parent is not None and key is not None:
                    if isinstance(parent, dict) and isinstance(key, str):
                        parent[key] = resolved
                    elif isinstance(parent, list) and isinstance(key, int):
                        parent[key] = resolved
                else:
                    # This is the root schema itself
                    schema.clear()
                    schema.update(resolved)
                    resolved = schema

                # Add to ref chain to track circular references
                new_ref_chain = ref_chain.copy()
                new_ref_chain.add(ref_name)

                # Add resolved node to queue for further processing
                queue.append((resolved, parent, key, child_defs, new_ref_chain))
                continue

            # --- Case 2: regular dict – process its values ---
            # Update defs with any nested $defs/definitions present *here*.
            current_defs = {
                **active_defs,
                **node.get("$defs", {}),
                **node.get("definitions", {}),
            }

            # Add all dict values to queue
            for k, v in node.items():
                queue.append((v, node, k, current_defs, ref_chain))

        # ---------------------------- list ------------------------------
        elif isinstance(node, list):
            # Add all list items to queue
            for idx, item in enumerate(node):
                queue.append((item, node, idx, active_defs, ref_chain))

