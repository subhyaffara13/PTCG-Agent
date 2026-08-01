
def _mk_tmp(request: FixtureRequest, factory: TempPathFactory) -> Path:
    name = request.node.name
    name = re.sub(r"[\W]", "_", name)
    MAXVAL = 30
    name = name[:MAXVAL]
    return factory.mktemp(name, numbered=True)

