
def _check_protected_namespaces(
    protected_namespaces: tuple[str | Pattern[str], ...],
    ann_name: str,
    bases: tuple[type[Any], ...],
    cls_name: str,
) -> None:
    BaseModel = import_cached_base_model()

    for protected_namespace in protected_namespaces:
        ns_violation = False
        if isinstance(protected_namespace, Pattern):
            ns_violation = protected_namespace.match(ann_name) is not None
        elif isinstance(protected_namespace, str):
            ns_violation = ann_name.startswith(protected_namespace)

        if ns_violation:
            for b in bases:
                if hasattr(b, ann_name):
                    if not (issubclass(b, BaseModel) and ann_name in getattr(b, '__pydantic_fields__', {})):
                        raise ValueError(
                            f'Field {ann_name!r} conflicts with member {getattr(b, ann_name)}'
                            f' of protected namespace {protected_namespace!r}.'
                        )
            else:
                valid_namespaces: list[str] = []
                for pn in protected_namespaces:
                    if isinstance(pn, Pattern):
                        if not pn.match(ann_name):
                            valid_namespaces.append(f're.compile({pn.pattern!r})')
                    else:
                        if not ann_name.startswith(pn):
                            valid_namespaces.append(f"'{pn}'")

                valid_namespaces_str = f'({", ".join(valid_namespaces)}{",)" if len(valid_namespaces) == 1 else ")"}'

                warnings.warn(
                    f'Field {ann_name!r} in {cls_name!r} conflicts with protected namespace {protected_namespace!r}.\n\n'
                    f"You may be able to solve this by setting the 'protected_namespaces' configuration to {valid_namespaces_str}.",
                    UserWarning,
                    stacklevel=5,
                )

