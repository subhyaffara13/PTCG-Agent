
def get_parser(prog='pycodestyle', version=__version__):
    """Create the parser for the program."""
    parser = OptionParser(prog=prog, version=version,
                          usage="%prog [options] input ...")
    parser.config_options = [
        'exclude', 'filename', 'select', 'ignore', 'max-line-length',
        'max-doc-length', 'indent-size', 'hang-closing', 'count', 'format',
        'quiet', 'show-pep8', 'show-source', 'statistics', 'verbose']
    parser.add_option('-v', '--verbose', default=0, action='count',
                      help="print status messages, or debug with -vv")
    parser.add_option('-q', '--quiet', default=0, action='count',
                      help="report only file names, or nothing with -qq")
    parser.add_option('-r', '--repeat', default=True, action='store_true',
                      help="(obsolete) show all occurrences of the same error")
    parser.add_option('--first', action='store_false', dest='repeat',
                      help="show first occurrence of each error")
    parser.add_option('--exclude', metavar='patterns', default=DEFAULT_EXCLUDE,
                      help="exclude files or directories which match these "
                           "comma separated patterns (default: %default)")
    parser.add_option('--filename', metavar='patterns', default='*.py',
                      help="when parsing directories, only check filenames "
                           "matching these comma separated patterns "
                           "(default: %default)")
    parser.add_option('--select', metavar='errors', default='',
                      help="select errors and warnings (e.g. E,W6)")
    parser.add_option('--ignore', metavar='errors', default='',
                      help="skip errors and warnings (e.g. E4,W) "
                           "(default: %s)" % DEFAULT_IGNORE)
    parser.add_option('--show-source', action='store_true',
                      help="show source code for each error")
    parser.add_option('--show-pep8', action='store_true',
                      help="show text of PEP 8 for each error "
                           "(implies --first)")
    parser.add_option('--statistics', action='store_true',
                      help="count errors and warnings")
    parser.add_option('--count', action='store_true',
                      help="print total number of errors and warnings "
                           "to standard error and set exit code to 1 if "
                           "total is not null")
    parser.add_option('--max-line-length', type='int', metavar='n',
                      default=MAX_LINE_LENGTH,
                      help="set maximum allowed line length "
                           "(default: %default)")
    parser.add_option('--max-doc-length', type='int', metavar='n',
                      default=None,
                      help="set maximum allowed doc line length and perform "
                           "these checks (unchecked if not set)")
    parser.add_option('--indent-size', type='int', metavar='n',
                      default=INDENT_SIZE,
                      help="set how many spaces make up an indent "
                           "(default: %default)")
    parser.add_option('--hang-closing', action='store_true',
                      help="hang closing bracket instead of matching "
                           "indentation of opening bracket's line")
    parser.add_option('--format', metavar='format', default='default',
                      help="set the error format [default|pylint|<custom>]")
    parser.add_option('--diff', action='store_true',
                      help="report changes only within line number ranges in "
                           "the unified diff received on STDIN")
    group = parser.add_option_group("Testing Options")
    group.add_option('--benchmark', action='store_true',
                     help="measure processing speed")
    return parser


def get_parser():
    """Return the markdown-it parser to use."""
    parser = (
        MarkdownIt("commonmark")
        .enable("table")
        .use(front_matter_plugin)
        .use(myst_block_plugin)
        .use(myst_role_plugin)
        # we only need to parse block level components (for efficiency)
        .disable("inline", True)
    )
    return parser

