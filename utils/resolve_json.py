
def resolve_json(cls):  # type: ignore[no-untyped-def]
    try:
        inner = st.none() if cls.inner_type is None else st.from_type(cls.inner_type)
    except Exception:  # pragma: no cover
        finite = st.floats(allow_infinity=False, allow_nan=False)
        inner = st.recursive(
            base=st.one_of(st.none(), st.booleans(), st.integers(), finite, st.text()),
            extend=lambda x: st.lists(x) | st.dictionaries(st.text(), x),  # type: ignore
        )
    inner_type = getattr(cls, 'inner_type', None)
    return st.builds(
        cls.inner_type.json if lenient_issubclass(inner_type, pydantic.BaseModel) else json.dumps,
        inner,
        ensure_ascii=st.booleans(),
        indent=st.none() | st.integers(0, 16),
        sort_keys=st.booleans(),
    )

