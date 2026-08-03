from typing import Callable

def _translate_comprehension_with_scope(
    builder: IRBuilder,
    node: GeneratorExpr | DictionaryComprehension,
    gen_body: Callable[[], Value],
) -> Value:
    """Wrap a comprehension body with a lightweight scope for closure capture."""
    from mypyc.irbuild.context import FuncInfo
    from mypyc.irbuild.env_class import add_vars_to_env, finalize_env_class, setup_env_class

    comprehension_fdef = builder.comprehension_to_fitem[node]
    fn_info = FuncInfo(
        fitem=comprehension_fdef,
        name=comprehension_fdef.name,
        is_nested=True,
        contains_nested=True,
        is_comprehension_scope=True,
    )

    with builder.enter_scope(fn_info):
        setup_env_class(builder)
        finalize_env_class(builder)
        add_vars_to_env(builder)
        return gen_body()

