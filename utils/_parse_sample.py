
def _parse_sample(text):
    separator = " # "
    # Detect the labels in the text
    label_start = _next_unquoted_char(text, '{')
    if label_start == -1 or separator in text[:label_start]:
        # We don't have labels, but there could be an exemplar.
        name_end = _next_unquoted_char(text, ' \t')
        name = text[:name_end].strip()
        if not _is_valid_legacy_metric_name(name):
            raise ValueError("invalid metric name:" + text)
        # Parse the remaining text after the name
        remaining_text = text[name_end + 1:]
        value, timestamp = _parse_value_and_timestamp(remaining_text)
        return Sample(name, {}, value, timestamp)
    name = text[:label_start].strip()
    label_end = _next_unquoted_char(text[label_start:], '}') + label_start
    labels = parse_labels(text[label_start + 1:label_end], False)
    if not name:
        # Name might be in the labels
        if '__name__' not in labels:
            raise ValueError
        name = labels['__name__']
        del labels['__name__']
    elif '__name__' in labels:
        raise ValueError("metric name specified more than once")
    # Parsing labels succeeded, continue parsing the remaining text
    remaining_text = text[label_end + 1:]
    value, timestamp = _parse_value_and_timestamp(remaining_text)
    return Sample(name, labels, value, timestamp)


def _parse_sample(text):
    separator = " # "
    # Detect the labels in the text
    label_start = _next_unquoted_char(text, '{')
    if label_start == -1 or separator in text[:label_start]:
        # We don't have labels, but there could be an exemplar.
        name_end = _next_unquoted_char(text, ' ')
        name = text[:name_end]
        if not _is_valid_legacy_metric_name(name):
            raise ValueError("invalid metric name:" + text)
        # Parse the remaining text after the name
        remaining_text = text[name_end + 1:]
        value, timestamp, exemplar = _parse_remaining_text(remaining_text)
        return Sample(name, {}, value, timestamp, exemplar)
    name = text[:label_start]
    label_end = _next_unquoted_char(text, '}')
    labels = parse_labels(text[label_start + 1:label_end], True)
    if not name:
        # Name might be in the labels
        if '__name__' not in labels:
            raise ValueError
        name = labels['__name__']
        del labels['__name__']
    elif '__name__' in labels:
        raise ValueError("metric name specified more than once")
    # Parsing labels succeeded, continue parsing the remaining text
    remaining_text = text[label_end + 2:]
    value, timestamp, exemplar = _parse_remaining_text(remaining_text)
    return Sample(name, labels, value, timestamp, exemplar)

