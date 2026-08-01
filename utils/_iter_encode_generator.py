
def _iter_encode_generator(input, encode):
    for chunck in input:
        output = encode(chunck)
        if output:
            yield output
    output = encode('', final=True)
    if output:
        yield output

