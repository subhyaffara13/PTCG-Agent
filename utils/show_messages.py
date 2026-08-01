
def show_messages(
    messages: list[str], f: TextIO, formatter: util.FancyFormatter, options: Options
) -> None:
    for msg in messages:
        if options.color_output:
            msg = formatter.colorize(msg)
        f.write(msg + "\n")
    f.flush()

