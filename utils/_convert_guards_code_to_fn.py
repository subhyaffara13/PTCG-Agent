
def _convert_guards_code_to_fn(
    guards_code: list[str],
    paths_of_placeholders: list[pytree.KeyPath],
):
    """
    Generates Python code given guards code and paths of placeholders.
    We assume that, based on source information,
    - the tracer generates the guards code
    - the input spec generates the paths of placeholders.

    Example:

    Suppose we are given the guards code "L['z']['k'].size()[1] == 3"
    and we are given that ['z']['k'] is the path of placeholder #2.
    Then we will generate:
    ```
    torch._assert(
        args[2].size()[0] == 3,
        "Guard failed: z['k'].size()[0] == 3",
    )
    ```

    FAQ: Why do we generate code based on (flattened) args instead of
    the original (unflattened) inputs? Because this would require
    inserting an additional pytree.unflatten call in our graph.

    FAQ: Why do we not emit RuntimeError on guard failure as we used to?
    Because it is inconvenient :/, get used to AssertionError instead.
    """

    import ast

    from torch.fx.experimental.symbolic_shapes import SYMPY_INTERP

    actual_guards_code = []
    shadow_guards_code = []
    for c in guards_code:
        a, s = c, c
        for idx, path in enumerate(paths_of_placeholders):
            # e.g., replace L['z']['k'] with args[2] for Python code (actual)
            a = a.replace("L" + pytree.keystr(path), f"args[{idx}]")
            # e.g., replace L['z']['k'] with z['k'] for error message (shadow)
            s = s.replace(
                "L" + pytree.keystr(path),
                path[0].key + pytree.keystr(path[1:]),  # type: ignore[attr-defined]
            )
        actual_guards_code.append(a)
        shadow_guards_code.append(s.replace("\n", ""))

    # generate function code as str
    code_str = "\ndef _(*args):\n"
    for actual, shadow in zip(actual_guards_code, shadow_guards_code):
        # printing guards code may potentially introduce redundant parens;
        # we can normalize them out for readability by parsing/unparsing
        # NOTE: this is not necessary for correctness, just deemed desirable
        _shadow = ast.unparse(ast.parse(shadow, mode="eval"))
        # actual code and shadow error message
        code_str += f'  torch._assert({actual}, "Guard failed: {_shadow}")\n'
    code_str += "  return\n"

    # populate namespace with sympy globals, materialize function (named `_`)
    namespace = {**SYMPY_INTERP}
    exec(code_str, namespace)

    # create and return a module whose forward is the materialized function
    # NOTE: we want Dynamo to trace through this module, to repopulate guards:
    # otherwise we would lose them when retracing
    # NOTE: calling this module will be a side effect (no users): so it must
    # be marked impure to avoid being not cleaned up by DCE
    guards_fn = GuardsFn()
    guards_fn.forward = torch._dynamo.dont_skip_tracing(namespace["_"])  # type: ignore[call-overload, method-assign]
    guards_fn._is_impure = True  # type: ignore[assignment]
    return guards_fn

