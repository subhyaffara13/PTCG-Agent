import re

def _parse_nh_struct(text):
    pattern = r'(\w+):\s*([^,}]+)'
    re_spans = re.compile(r'(positive_spans|negative_spans):\[(\d+:\d+(,\d+:\d+)*)\]')
    re_deltas = re.compile(r'(positive_deltas|negative_deltas):\[(-?\d+(?:,-?\d+)*)\]')

    items = dict(re.findall(pattern, text))
    span_matches = re_spans.findall(text)
    deltas = dict(re_deltas.findall(text))

    count_value = int(items['count'])
    sum_value = int(items['sum'])
    schema = int(items['schema'])
    zero_threshold = float(items['zero_threshold'])
    zero_count = int(items['zero_count'])

    pos_spans = _compose_spans(span_matches, 'positive_spans')
    neg_spans = _compose_spans(span_matches, 'negative_spans')
    pos_deltas = _compose_deltas(deltas, 'positive_deltas')
    neg_deltas = _compose_deltas(deltas, 'negative_deltas')
      
    return NativeHistogram(
        count_value=count_value,
        sum_value=sum_value,
        schema=schema,
        zero_threshold=zero_threshold,
        zero_count=zero_count,
        pos_spans=pos_spans,
        neg_spans=neg_spans,
        pos_deltas=pos_deltas,
        neg_deltas=neg_deltas
    )

