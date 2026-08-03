from typing import Dict

def parse_labels(labels_string: str, openmetrics: bool = False) -> Dict[str, str]:
    labels: Dict[str, str] = {}

    # Copy original labels
    sub_labels = labels_string.strip()
    if openmetrics and sub_labels and sub_labels[0] == ',':
        raise ValueError("leading comma: " + labels_string)
    try:
        # Process one label at a time
        while sub_labels:
            # The label name is before the equal, or if there's no equal, that's the
            # metric name.
            
            name_term, value_term, sub_labels = _next_term(sub_labels, openmetrics)
            if not value_term:
                if openmetrics:
                    raise ValueError("empty term in line: " + labels_string)
                continue
            
            label_name, quoted_name = _unquote_unescape(name_term)
                
            if not quoted_name and not _is_valid_legacy_metric_name(label_name):
                raise ValueError("unquoted UTF-8 metric name")
                
            # Check for missing quotes 
            if not value_term or value_term[0] != '"':
                raise ValueError

            # The first quote is guaranteed to be after the equal.
            # Make sure that the next unescaped quote is the last character.
            i = 1
            while i < len(value_term):
                i = value_term.index('"', i)
                if not _is_character_escaped(value_term[:i], i):
                    break
                i += 1
            # The label value is between the first and last quote
            quote_end = i + 1
            if quote_end != len(value_term):
                raise ValueError("unexpected text after quote: " + labels_string)

            label_value, _ = _unquote_unescape(value_term)
            if label_name == '__name__':
                _validate_metric_name(label_name)
            else:
                _validate_labelname(label_name)
            if label_name in labels:
                raise ValueError("invalid line, duplicate label name: " + labels_string)
            labels[label_name] = label_value
        return labels
    except ValueError:
        raise ValueError("Invalid labels: " + labels_string)

