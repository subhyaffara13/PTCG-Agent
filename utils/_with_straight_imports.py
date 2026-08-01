
def _with_straight_imports(
    parsed: parse.ParsedContent,
    config: Config,
    straight_modules: Iterable[str],
    section: str,
    remove_imports: list[str],
    import_type: str,
) -> list[str]:
    output: list[str] = []

    as_imports = any(module in parsed.as_map["straight"] for module in straight_modules)

    # combine_straight_imports only works for bare imports, 'as' imports not included
    if config.combine_straight_imports and not as_imports:
        if not straight_modules:
            return []

        above_comments: list[str] = []
        inline_comments: list[str] = []

        for module in straight_modules:
            if module in parsed.categorized_comments["above"]["straight"]:
                above_comments.extend(parsed.categorized_comments["above"]["straight"].pop(module))
            if module in parsed.categorized_comments["straight"]:
                inline_comments.extend(parsed.categorized_comments["straight"][module])

        combined_straight_imports = ", ".join(straight_modules)
        if inline_comments:
            combined_inline_comments = " ".join(inline_comments)
        else:
            combined_inline_comments = ""

        output.extend(above_comments)

        if combined_inline_comments:
            output.append(
                f"{import_type} {combined_straight_imports}  # {combined_inline_comments}"
            )
        else:
            output.append(f"{import_type} {combined_straight_imports}")

        return output

    for module in straight_modules:
        if module in remove_imports:
            continue

        import_definition = []
        if module in parsed.as_map["straight"]:
            if parsed.imports[section]["straight"][module]:
                import_definition.append((f"{import_type} {module}", module))
            import_definition.extend(
                (f"{import_type} {module} as {as_import}", f"{module} as {as_import}")
                for as_import in parsed.as_map["straight"][module]
            )
        else:
            import_definition.append((f"{import_type} {module}", module))

        comments_above = parsed.categorized_comments["above"]["straight"].pop(module, None)
        if comments_above:
            output.extend(comments_above)
        output.extend(
            with_comments(
                parsed.categorized_comments["straight"].get(imodule),
                idef,
                removed=config.ignore_comments,
                comment_prefix=config.comment_prefix,
            )
            for idef, imodule in import_definition
        )

    return output

