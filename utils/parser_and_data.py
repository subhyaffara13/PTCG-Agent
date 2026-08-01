
def parser_and_data(all_parsers, csv1):
    parser = all_parsers

    with open(csv1, "rb") as f:
        data = f.read()
    expected = parser.read_csv(csv1)

    return parser, data, expected

