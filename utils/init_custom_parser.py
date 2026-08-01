
def init_custom_parser(modification, transformer=None):
    latex_grammar = Path(grammar_file).read_text(encoding="utf-8")
    latex_grammar += modification

    with tempfile.NamedTemporaryFile() as f:
        f.write(bytes(latex_grammar, encoding="utf8"))
        f.flush()

        parser = LarkLaTeXParser(grammar_file=f.name, transformer=transformer)

    return parser

