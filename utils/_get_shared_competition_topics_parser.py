
def _get_shared_competition_topics_parser() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("-p", "--page", dest="page", type=int, default=1, required=False, help=Help.param_page)
    _add_output_format_args(shared)
    shared.add_argument("-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet)
    return shared

