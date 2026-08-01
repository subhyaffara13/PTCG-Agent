
def _add_arguments(param, parser, used_char_args, add_nos):
    '''
    Add the argument(s) to an ArgumentParser (using add_argument) for a given
    parameter. used_char_args is the set of -short options currently already in
    use, and is updated (if necessary) by this function. If add_nos is True,
    this will also add an inverse switch for all boolean options. For
    instance, for the boolean parameter "verbose", this will create --verbose
    and --no-verbose.
    '''

    # Impl note: This function is kept separate from make_parser because it's
    # already very long and I wanted to separate out as much as possible into
    # its own call scope, to prevent even the possibility of suble mutation
    # bugs.
    if param.kind is param.POSITIONAL_ONLY:
        raise PositionalArgError(param)
    elif param.kind is param.VAR_KEYWORD:
        raise KWArgError(param)

    # These are the kwargs for the add_argument function.
    arg_spec = {}
    is_option = False

    # Get the type and default from the annotation.
    arg_type, description = _get_type_description(param.annotation)

    # Get the default value
    default = param.default

    # If there is no explicit type, and the default is present and not None,
    # infer the type from the default.
    if arg_type is None and default not in {_empty, None}:
        arg_type = type(default)

    # Add default. The presence of a default means this is an option, not an
    # argument.
    if default is not _empty:
        arg_spec['default'] = default
        is_option = True

    # Add the type
    if arg_type is not None:
        # Special case for bool: make it just a --switch
        if arg_type is bool:
            if not default or default is _empty:
                arg_spec['action'] = 'store_true'
            else:
                arg_spec['action'] = 'store_false'

            # Switches are always options
            is_option = True

        # Special case for file types: make it a string type, for filename
        elif isinstance(default, IOBase):
            arg_spec['type'] = str

        # TODO: special case for list type.
        #   - How to specificy type of list members?
        #       - param: [int]
        #       - param: int =[]
        #   - action='append' vs nargs='*'

        else:
            arg_spec['type'] = arg_type

    # nargs: if the signature includes *args, collect them as trailing CLI
    # arguments in a list. *args can't have a default value, so it can never be
    # an option.
    if param.kind is param.VAR_POSITIONAL:
        # TODO: consider depluralizing metavar/name here.
        arg_spec['nargs'] = '*'

    # Add description.
    if description is not None:
        arg_spec['help'] = description

    # Get the --flags
    flags = []
    name = param.name

    if is_option:
        # Add the first letter as a -short option.
        for letter in name[0], name[0].swapcase():
            if letter not in used_char_args:
                used_char_args.add(letter)
                flags.append('-{}'.format(letter))
                break

        # If the parameter is a --long option, or is a -short option that
        # somehow failed to get a flag, add it.
        if len(name) > 1 or not flags:
            flags.append('--{}'.format(name))

        arg_spec['dest'] = name
    else:
        flags.append(name)

    parser.add_argument(*flags, **arg_spec)

    # Create the --no- version for boolean switches
    if add_nos and arg_type is bool:
        parser.add_argument(
            '--no-{}'.format(name),
            action='store_const',
            dest=name,
            const=default if default is not _empty else False)

