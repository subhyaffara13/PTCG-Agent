
def _compose_exemplar_string(metric, sample, exemplar):
    """Constructs an exemplar string."""
    if not _is_valid_exemplar_metric(metric, sample):
        raise ValueError(f"Metric {metric.name} has exemplars, but is not a histogram bucket or counter")
    labels = '{{{0}}}'.format(','.join(
        ['{}="{}"'.format(
            k, v.replace('\\', r'\\').replace('\n', r'\n').replace('"', r'\"'))
            for k, v in sorted(exemplar.labels.items())]))
    if exemplar.timestamp is not None:
        exemplarstr = ' # {} {} {}'.format(
            labels,
            floatToGoString(exemplar.value),
            exemplar.timestamp,
        )
    else:
        exemplarstr = ' # {} {}'.format(
            labels,
            floatToGoString(exemplar.value),
        )

    return exemplarstr

