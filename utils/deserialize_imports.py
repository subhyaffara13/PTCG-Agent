
def deserialize_imports(import_bytes: bytes) -> list[ImportBase]:
    """Deserialize import metadata from bytes into mypy AST nodes."""
    if not import_bytes:
        return []

    data = ReadBuffer(import_bytes)

    expect_tag(data, LIST_GEN)
    n_imports = read_int_bare(data)

    imports: list[ImportBase] = []

    for _ in range(n_imports):
        tag = read_tag(data)

        if tag == IMPORT_METADATA:
            name = read_str(data)
            relative = read_int(data)

            has_asname = read_bool(data)
            if has_asname:
                asname = read_str(data)
            else:
                asname = None

            # Note: relative imports are handled via ImportFrom, so relative should be 0 here
            stmt = Import([(name, asname)])
            _read_and_set_import_metadata(data, stmt)
            imports.append(stmt)

        elif tag == IMPORTFROM_METADATA:
            module = read_str(data)
            relative = read_int(data)

            expect_tag(data, LIST_GEN)
            n_names = read_int_bare(data)
            names: list[tuple[str, str | None]] = []

            for _ in range(n_names):
                name = read_str(data)
                has_asname = read_bool(data)
                if has_asname:
                    asname = read_str(data)
                else:
                    asname = None
                names.append((name, asname))

            stmt = ImportFrom(module, relative, names)
            _read_and_set_import_metadata(data, stmt)
            imports.append(stmt)

        elif tag == IMPORTALL_METADATA:
            module = read_str(data)
            relative = read_int(data)

            stmt = ImportAll(module, relative)
            _read_and_set_import_metadata(data, stmt)
            imports.append(stmt)

        else:
            raise ValueError(f"Unexpected tag in import metadata: {tag}")

    return imports

