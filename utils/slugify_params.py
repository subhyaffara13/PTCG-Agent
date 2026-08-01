
def slugify_params(args: argparse.Namespace) -> dict[str, Any]:
    return dict(
        text=args.input_string,
        entities=args.entities,
        decimal=args.decimal,
        hexadecimal=args.hexadecimal,
        max_length=args.max_length,
        word_boundary=args.word_boundary,
        save_order=args.save_order,
        separator=args.separator,
        stopwords=args.stopwords,
        lowercase=args.lowercase,
        replacements=args.replacements,
        allow_unicode=args.allow_unicode
    )

