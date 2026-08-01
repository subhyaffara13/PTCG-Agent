
def remotes_in(
    root: Path,
    name: str,
    uri: str,
) -> Iterable[tuple[str, Schema]]:
    # This messy logic is because the test suite is terrible at indicating
    # what remotes are needed for what drafts, and mixes in schemas which
    # have no $schema and which are invalid under earlier versions, in with
    # other schemas which are needed for tests.

    for each in root.rglob("*.json"):
        schema = json.loads(each.read_text())

        relative = str(each.relative_to(root)).replace("\\", "/")

        if (
            ( # invalid boolean schema
                name in {"draft3", "draft4"}
                and each.stem == "tree"
            ) or
            (  # draft<NotThisDialect>/*.json
                "$schema" not in schema
                and relative.startswith("draft")
                and not relative.startswith(name)
            )
        ):
            continue
        yield f"{MAGIC_REMOTE_URL}/{relative}", schema

