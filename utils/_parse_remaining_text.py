
def _parse_remaining_text(text):
    split_text = text.split(" ", 1)
    val = _parse_value(split_text[0])
    if len(split_text) == 1:
        # We don't have timestamp or exemplar
        return val, None, None  

    timestamp = []
    exemplar_value = []
    exemplar_timestamp = []
    exemplar_labels = None

    state = 'timestamp'
    text = split_text[1]

    it = iter(text)
    in_quotes = False
    for char in it:
        if char == '"':
            in_quotes = not in_quotes
        if in_quotes:
            continue
        if state == 'timestamp':
            if char == '#' and not timestamp:
                state = 'exemplarspace'
            elif char == ' ':
                state = 'exemplarhash'
            else:
                timestamp.append(char)
        elif state == 'exemplarhash':
            if char == '#':
                state = 'exemplarspace'
            else:
                raise ValueError("Invalid line: " + text)
        elif state == 'exemplarspace':
            if char == ' ':
                state = 'exemplarstartoflabels'
            else:
                raise ValueError("Invalid line: " + text)
        elif state == 'exemplarstartoflabels':
            if char == '{':
                label_start = _next_unquoted_char(text, '{')
                label_end = _last_unquoted_char(text, '}')
                exemplar_labels = parse_labels(text[label_start + 1:label_end], True)
                state = 'exemplarparsedlabels'
            else:
                raise ValueError("Invalid line: " + text)
        elif state == 'exemplarparsedlabels':
            if char == '}':
                state = 'exemplarvaluespace'
        elif state == 'exemplarvaluespace':
            if char == ' ':
                state = 'exemplarvalue'
            else:
                raise ValueError("Invalid line: " + text)
        elif state == 'exemplarvalue':
            if char == ' ' and not exemplar_value:
                raise ValueError("Invalid line: " + text)
            elif char == ' ':
                state = 'exemplartimestamp'
            else:
                exemplar_value.append(char)
        elif state == 'exemplartimestamp':
            exemplar_timestamp.append(char)

    # Trailing space after value.
    if state == 'timestamp' and not timestamp:
        raise ValueError("Invalid line: " + text)

    # Trailing space after value.
    if state == 'exemplartimestamp' and not exemplar_timestamp:
        raise ValueError("Invalid line: " + text)

    # Incomplete exemplar.
    if state in ['exemplarhash', 'exemplarspace', 'exemplarstartoflabels', 'exemplarparsedlabels']:
        raise ValueError("Invalid line: " + text)

    ts = _parse_timestamp(timestamp)
    exemplar = None
    if exemplar_labels is not None:
        exemplar_length = sum(len(k) + len(v) for k, v in exemplar_labels.items())
        if exemplar_length > 128:
            raise ValueError("Exemplar labels are too long: " + text)
        exemplar = Exemplar(
            exemplar_labels,
            _parse_value(exemplar_value),
            _parse_timestamp(exemplar_timestamp),
        )

    return val, ts, exemplar

