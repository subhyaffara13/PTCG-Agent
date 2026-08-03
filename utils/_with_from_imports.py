import copy

def _with_from_imports(
    parsed: parse.ParsedContent,
    config: Config,
    from_modules: Iterable[str],
    section: str,
    remove_imports: list[str],
    import_type: str,
) -> list[str]:
    output: list[str] = []
    for module in from_modules:
        if module in remove_imports:
            continue

        import_start = f"from {module} {import_type} "
        from_imports = list(parsed.imports[section]["from"][module])
        if (
            not config.no_inline_sort
            or (config.force_single_line and module not in config.single_line_exclusions)
        ) and not config.only_sections:
            from_imports = sorting.sort(
                config,
                from_imports,
                key=lambda key: sorting.module_key(
                    key,
                    config,
                    True,
                    config.force_alphabetical_sort_within_sections,
                    section_name=section,
                ),
                reverse=config.reverse_sort,
            )
        if remove_imports:
            from_imports = [
                line for line in from_imports if f"{module}.{line}" not in remove_imports
            ]

        sub_modules = [f"{module}.{from_import}" for from_import in from_imports]
        as_imports = {
            from_import: [
                f"{from_import} as {as_module}" for as_module in parsed.as_map["from"][sub_module]
            ]
            for from_import, sub_module in zip(from_imports, sub_modules, strict=False)
            if sub_module in parsed.as_map["from"]
        }
        if config.combine_as_imports and not ("*" in from_imports and config.combine_star):
            if not config.no_inline_sort:
                for as_import in as_imports:
                    if not config.only_sections:
                        as_imports[as_import] = sorting.sort(config, as_imports[as_import])
            for from_import in copy.copy(from_imports):
                if from_import in as_imports:
                    idx = from_imports.index(from_import)
                    if parsed.imports[section]["from"][module][from_import]:
                        from_imports[(idx + 1) : (idx + 1)] = as_imports.pop(from_import)
                    else:
                        from_imports[idx : (idx + 1)] = as_imports.pop(from_import)

        only_show_as_imports = False
        comments = parsed.categorized_comments["from"].pop(module, ())
        above_comments = parsed.categorized_comments["above"]["from"].pop(module, None)
        while from_imports:
            if above_comments:
                output.extend(above_comments)
                above_comments = None

            if "*" in from_imports and config.combine_star:
                import_statement = wrap.line(
                    with_comments(
                        _with_star_comments(parsed, module, list(comments or ())),
                        f"{import_start}*",
                        removed=config.ignore_comments,
                        comment_prefix=config.comment_prefix,
                    ),
                    parsed.line_separator,
                    config,
                )
                from_imports = [
                    from_import for from_import in from_imports if from_import in as_imports
                ]
                only_show_as_imports = True
            elif config.force_single_line and module not in config.single_line_exclusions:
                import_statement = ""
                while from_imports:
                    from_import = from_imports.pop(0)
                    single_import_line = with_comments(
                        comments,
                        import_start + from_import,
                        removed=config.ignore_comments,
                        comment_prefix=config.comment_prefix,
                    )
                    comment = (
                        parsed.categorized_comments["nested"].get(module, {}).pop(from_import, None)
                    )
                    if comment:
                        single_import_line += (
                            f"{(comments and ';') or config.comment_prefix} {comment}"
                        )
                    if from_import in as_imports:
                        if (
                            parsed.imports[section]["from"][module][from_import]
                            and not only_show_as_imports
                        ):
                            output.append(
                                wrap.line(single_import_line, parsed.line_separator, config)
                            )
                        from_comments = parsed.categorized_comments["straight"].get(
                            f"{module}.{from_import}"
                        )

                        if not config.only_sections:
                            output.extend(
                                with_comments(
                                    from_comments,
                                    wrap.line(
                                        import_start + as_import, parsed.line_separator, config
                                    ),
                                    removed=config.ignore_comments,
                                    comment_prefix=config.comment_prefix,
                                )
                                for as_import in sorting.sort(config, as_imports[from_import])
                            )

                        else:
                            output.extend(
                                with_comments(
                                    from_comments,
                                    wrap.line(
                                        import_start + as_import, parsed.line_separator, config
                                    ),
                                    removed=config.ignore_comments,
                                    comment_prefix=config.comment_prefix,
                                )
                                for as_import in as_imports[from_import]
                            )
                    else:
                        output.append(wrap.line(single_import_line, parsed.line_separator, config))
                    comments = None
            else:
                while from_imports and from_imports[0] in as_imports:
                    from_import = from_imports.pop(0)

                    if not config.only_sections:
                        as_imports[from_import] = sorting.sort(config, as_imports[from_import])
                    from_comments = (
                        parsed.categorized_comments["straight"].get(f"{module}.{from_import}") or []
                    )
                    if (
                        parsed.imports[section]["from"][module][from_import]
                        and not only_show_as_imports
                    ):
                        specific_comment = (
                            parsed.categorized_comments["nested"]
                            .get(module, {})
                            .pop(from_import, None)
                        )
                        if specific_comment:
                            from_comments.append(specific_comment)
                        output.append(
                            wrap.line(
                                with_comments(
                                    from_comments,
                                    import_start + from_import,
                                    removed=config.ignore_comments,
                                    comment_prefix=config.comment_prefix,
                                ),
                                parsed.line_separator,
                                config,
                            )
                        )
                        from_comments = []

                    for as_import in as_imports[from_import]:
                        specific_comment = (
                            parsed.categorized_comments["nested"]
                            .get(module, {})
                            .pop(as_import, None)
                        )
                        if specific_comment:
                            from_comments.append(specific_comment)

                        output.append(
                            wrap.line(
                                with_comments(
                                    from_comments,
                                    import_start + as_import,
                                    removed=config.ignore_comments,
                                    comment_prefix=config.comment_prefix,
                                ),
                                parsed.line_separator,
                                config,
                            )
                        )

                        from_comments = []

                if "*" in from_imports:
                    output.append(
                        with_comments(
                            _with_star_comments(parsed, module, []),
                            f"{import_start}*",
                            removed=config.ignore_comments,
                            comment_prefix=config.comment_prefix,
                        )
                    )
                    from_imports.remove("*")

                for from_import in copy.copy(from_imports):
                    comment = (
                        parsed.categorized_comments["nested"].get(module, {}).pop(from_import, None)
                    )
                    if comment:
                        # If the comment is a noqa and hanging indent wrapping is used,
                        # keep the name in the main list and hoist the comment to the statement.
                        if (
                            comment.lower().startswith("noqa")
                            and config.multi_line_output == wrap.Modes.HANGING_INDENT  # type: ignore[attr-defined] # noqa: E501
                        ):
                            comments = list(comments) if comments else []
                            comments.append(comment)
                            continue

                        from_imports.remove(from_import)
                        if from_imports:
                            use_comments = []
                        else:
                            use_comments = comments
                            comments = None
                        single_import_line = with_comments(
                            use_comments,
                            import_start + from_import,
                            removed=config.ignore_comments,
                            comment_prefix=config.comment_prefix,
                        )
                        single_import_line += (
                            f"{(use_comments and ';') or config.comment_prefix} {comment}"
                        )
                        output.append(wrap.line(single_import_line, parsed.line_separator, config))

                from_import_section = []
                while from_imports and (
                    from_imports[0] not in as_imports
                    or (
                        config.combine_as_imports
                        and parsed.imports[section]["from"][module][from_import]
                    )
                ):
                    from_import_section.append(from_imports.pop(0))
                if config.combine_as_imports:
                    comments = (comments or []) + list(
                        parsed.categorized_comments["from"].pop(f"{module}.__combined_as__", ())
                    )
                import_statement = with_comments(
                    comments,
                    import_start + (", ").join(from_import_section),
                    removed=config.ignore_comments,
                    comment_prefix=config.comment_prefix,
                )
                if not from_import_section:
                    import_statement = ""

                do_multiline_reformat = False

                force_grid_wrap = config.force_grid_wrap
                if force_grid_wrap and len(from_import_section) >= force_grid_wrap:
                    do_multiline_reformat = True

                if len(import_statement) > config.line_length and len(from_import_section) > 1:
                    do_multiline_reformat = True

                # If line too long AND have imports AND we are
                # NOT using GRID or VERTICAL wrap modes
                if (
                    len(import_statement) > config.line_length
                    and len(from_import_section) > 0
                    and config.multi_line_output not in (wrap.Modes.GRID, wrap.Modes.VERTICAL)  # type: ignore # noqa: E501
                ):
                    do_multiline_reformat = True

                if (
                    import_statement
                    and config.split_on_trailing_comma
                    and module in parsed.trailing_commas
                ):
                    import_statement = wrap.import_statement(
                        import_start=import_start,
                        from_imports=from_import_section,
                        comments=comments,
                        line_separator=parsed.line_separator,
                        config=config,
                        explode=True,
                    )

                elif do_multiline_reformat:
                    import_statement = wrap.import_statement(
                        import_start=import_start,
                        from_imports=from_import_section,
                        comments=comments,
                        line_separator=parsed.line_separator,
                        config=config,
                    )
                    if config.multi_line_output == wrap.Modes.GRID:  # type: ignore
                        other_import_statement = wrap.import_statement(
                            import_start=import_start,
                            from_imports=from_import_section,
                            comments=comments,
                            line_separator=parsed.line_separator,
                            config=config,
                            multi_line_output=wrap.Modes.VERTICAL_GRID,  # type: ignore
                        )
                        if (
                            max(
                                len(import_line)
                                for import_line in import_statement.split(parsed.line_separator)
                            )
                            > config.line_length
                        ):
                            import_statement = other_import_statement
                elif len(import_statement) > config.line_length:
                    import_statement = wrap.line(import_statement, parsed.line_separator, config)

            if import_statement:
                output.append(import_statement)
    return output

