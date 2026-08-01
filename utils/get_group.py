
def get_group(typer_instance: Typer) -> TyperGroup:
    group = get_group_from_info(
        TyperInfo(typer_instance),
        pretty_exceptions_short=typer_instance.pretty_exceptions_short,
        rich_markup_mode=typer_instance.rich_markup_mode,
        suggest_commands=typer_instance.suggest_commands,
    )
    return group

