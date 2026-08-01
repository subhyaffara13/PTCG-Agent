
def _print_help(what, name):
    try:
        if what == 'lexer':
            cls = get_lexer_by_name(name)
            print(f"Help on the {cls.name} lexer:")
            print(dedent(cls.__doc__))
        elif what == 'formatter':
            cls = find_formatter_class(name)
            print(f"Help on the {cls.name} formatter:")
            print(dedent(cls.__doc__))
        elif what == 'filter':
            cls = find_filter_class(name)
            print(f"Help on the {name} filter:")
            print(dedent(cls.__doc__))
        return 0
    except (AttributeError, ValueError):
        print(f"{what} not found!", file=sys.stderr)
        return 1

