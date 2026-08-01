
def check_post_init(api: TypeChecker, defn: FuncItem, info: TypeInfo) -> None:
    if defn.type is None:
        return
    assert isinstance(defn.type, FunctionLike)

    ideal_sig_method = info.get_method(_INTERNAL_POST_INIT_SYM_NAME)
    assert ideal_sig_method is not None and ideal_sig_method.type is not None
    ideal_sig = ideal_sig_method.type
    assert isinstance(ideal_sig, ProperType)  # we set it ourselves
    assert isinstance(ideal_sig, CallableType)
    ideal_sig = ideal_sig.copy_modified(name="__post_init__")

    api.check_override(
        override=defn.type,
        original=ideal_sig,
        name="__post_init__",
        name_in_super="__post_init__",
        supertype="dataclass",
        original_class_or_static=False,
        override_class_or_static=False,
        node=defn,
    )

