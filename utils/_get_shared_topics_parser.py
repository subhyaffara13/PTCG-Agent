
def _get_shared_topics_parser() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--page-size", dest="page_size", type=int, required=False, help=Help.param_page_size)
    shared.add_argument("--page-token", dest="page_token", required=False, help=Help.param_page_token)
    _add_output_format_args(shared)
    shared.add_argument("-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet)
    return shared

