
def make_parser(parser_list=[]):
    return expatreader.create_parser()


def make_parser(func_sig, description, epilog, add_nos):
    '''
    Given the signature of a function, create an ArgumentParser
    '''
    parser = ArgumentParser(description=description, epilog=epilog)

    used_char_args = {'h'}

    # Arange the params so that single-character arguments are first. This
    # esnures they don't have to get --long versions. sorted is stable, so the
    # parameters will otherwise still be in relative order.
    params = sorted(
        func_sig.parameters.values(),
        key=lambda param: len(param.name) > 1)

    for param in params:
        _add_arguments(param, parser, used_char_args, add_nos)

    return parser

