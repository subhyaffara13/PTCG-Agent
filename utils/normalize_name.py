
def normalize_name(
    name: AnyStr | None,
    qualifiers: Union[Union[str, bytes], dict[str, str], None],
    ptype: str | None,
    encode: bool | None = True,
) -> Optional[str]:
    if not name:
        return None

    name_str = name if isinstance(name, str) else name.decode("utf-8")
    quoter = get_quoter(encode)
    name_str = quoter(name_str)
    name_str = name_str.strip().strip("/")
    if ptype and ptype in ("mlflow"):
        return normalize_mlflow_name(name_str, qualifiers)
    if ptype in (
        "bitbucket",
        "github",
        "pypi",
        "gitlab",
        "composer",
        "luarocks",
        "oci",
        "npm",
        "alpm",
        "apk",
        "bitnami",
        "hex",
        "pub",
    ):
        name_str = name_str.lower()
    if ptype == "pypi":
        name_str = name_str.replace("_", "-").lower()
    if ptype == "hackage":
        name_str = name_str.replace("_", "-")
    if ptype == "pub":
        name_str = re.sub(r"[^a-z0-9]", "_", name_str.lower())
    return name_str or None


def normalize_name(name: str, prefix: str = "rename") -> str:
    name = name.replace(".", "_")
    if is_valid_for_codegen(name):
        return name
    return f"{prefix}_{name}"


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


def normalize_name(name: str) -> str:
    """
    Normalizes the given name. This can be applied to either a model *or* enum.
    """
    return re.sub(r'[^a-zA-Z0-9.\-_]', '_', name)


def normalize_name(name):
    """Normalize a python package name a la PEP 503"""
    # https://www.python.org/dev/peps/pep-0503/#normalized-names
    return re.sub('[-_.]+', '-', name).lower()

