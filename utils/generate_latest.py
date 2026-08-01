
def generate_latest(registry: Collector = REGISTRY, escaping: str = openmetrics.UNDERSCORES) -> bytes:
    """
    Generates the exposition format using the basic Prometheus text format.

    Params:
        registry: Collector to export data from.
        escaping: Escaping scheme used for metric and label names.

    Returns: UTF-8 encoded string containing the metrics in text format.
    """

    def sample_line(samples):
        if samples.labels:
            labelstr = '{0}'.format(','.join(
                # Label values always support UTF-8
                ['{}="{}"'.format(
                    openmetrics.escape_label_name(k, escaping), openmetrics._escape(v, openmetrics.ALLOWUTF8, False))
                    for k, v in sorted(samples.labels.items())]))
        else:
            labelstr = ''
        timestamp = ''
        if samples.timestamp is not None:
            # Convert to milliseconds.
            timestamp = f' {int(float(samples.timestamp) * 1000):d}'
        if escaping != openmetrics.ALLOWUTF8 or openmetrics._is_valid_legacy_metric_name(samples.name):
            if labelstr:
                labelstr = '{{{0}}}'.format(labelstr)
            return f'{openmetrics.escape_metric_name(samples.name, escaping)}{labelstr} {floatToGoString(samples.value)}{timestamp}\n'
        maybe_comma = ''
        if labelstr:
            maybe_comma = ','
        return f'{{{openmetrics.escape_metric_name(samples.name, escaping)}{maybe_comma}{labelstr}}} {floatToGoString(samples.value)}{timestamp}\n'

    output = []
    for metric in registry.collect():
        try:
            mname = metric.name
            mtype = metric.type
            # Munging from OpenMetrics into Prometheus format.
            if mtype == 'counter':
                mname = mname + '_total'
            elif mtype == 'info':
                mname = mname + '_info'
                mtype = 'gauge'
            elif mtype == 'stateset':
                mtype = 'gauge'
            elif mtype == 'gaugehistogram':
                # A gauge histogram is really a gauge,
                # but this captures the structure better.
                mtype = 'histogram'
            elif mtype == 'unknown':
                mtype = 'untyped'

            output.append('# HELP {} {}\n'.format(
                openmetrics.escape_metric_name(mname, escaping), metric.documentation.replace('\\', r'\\').replace('\n', r'\n')))
            output.append(f'# TYPE {openmetrics.escape_metric_name(mname, escaping)} {mtype}\n')

            om_samples: Dict[str, List[str]] = {}
            for s in metric.samples:
                for suffix in ['_created', '_gsum', '_gcount']:
                    if s.name == metric.name + suffix:
                        # OpenMetrics specific sample, put in a gauge at the end.
                        om_samples.setdefault(suffix, []).append(sample_line(s))
                        break
                else:
                    output.append(sample_line(s))
        except Exception as exception:
            exception.args = (exception.args or ('',)) + (metric,)
            raise

        for suffix, lines in sorted(om_samples.items()):
            output.append('# HELP {} {}\n'.format(openmetrics.escape_metric_name(metric.name + suffix, escaping),
                                                  metric.documentation.replace('\\', r'\\').replace('\n', r'\n')))
            output.append(f'# TYPE {openmetrics.escape_metric_name(metric.name + suffix, escaping)} gauge\n')
            output.extend(lines)
    return ''.join(output).encode('utf-8')


def generate_latest(registry, escaping=UNDERSCORES, version="1.0.0"):
    '''Returns the metrics from the registry in latest text format as a string.'''
    output = []
    for metric in registry.collect():
        try:
            mname = metric.name
            output.append('# HELP {} {}\n'.format(
                escape_metric_name(mname, escaping), _escape(metric.documentation, ALLOWUTF8, _is_legacy_labelname_rune)))
            output.append(f'# TYPE {escape_metric_name(mname, escaping)} {metric.type}\n')
            if metric.unit:
                output.append(f'# UNIT {escape_metric_name(mname, escaping)} {metric.unit}\n')
            for s in metric.samples:
                if escaping == ALLOWUTF8 and not _is_valid_legacy_metric_name(s.name):
                    labelstr = escape_metric_name(s.name, escaping)
                    if s.labels:
                        labelstr += ','
                else:
                    labelstr = ''

                if s.labels:
                    items = sorted(s.labels.items())
                    # Label values always support UTF-8
                    labelstr += ','.join(
                        ['{}="{}"'.format(
                            escape_label_name(k, escaping), _escape(v, ALLOWUTF8, _is_legacy_labelname_rune))
                            for k, v in items])
                if labelstr:
                    labelstr = "{" + labelstr + "}"
                if s.exemplar:
                    exemplarstr = _compose_exemplar_string(metric, s, s.exemplar)
                else:
                    exemplarstr = ''
                timestamp = ''
                if s.timestamp is not None:
                    timestamp = f' {s.timestamp}'
                
                # Skip native histogram samples entirely if version < 2.0.0
                if s.native_histogram and parse_version(version) < (2, 0, 0):
                    continue
                
                native_histogram = ''
                negative_spans = ''
                negative_deltas = ''
                positive_spans = ''
                positive_deltas = ''
                     
                if s.native_histogram:
                    # Initialize basic nh template
                    nh_sample_template = '{{count:{},sum:{},schema:{},zero_threshold:{},zero_count:{}'

                    args = [
                        s.native_histogram.count_value,
                        s.native_histogram.sum_value,
                        s.native_histogram.schema,
                        s.native_histogram.zero_threshold,
                        s.native_histogram.zero_count,
                    ]
                  
                    # If there are neg spans, append them and the neg deltas to the template and args
                    if s.native_histogram.neg_spans:
                        negative_spans = ','.join([f'{ns[0]}:{ns[1]}' for ns in s.native_histogram.neg_spans])
                        negative_deltas = ','.join(str(nd) for nd in s.native_histogram.neg_deltas)
                        nh_sample_template += ',negative_spans:[{}]'
                        args.append(negative_spans)
                        nh_sample_template += ',negative_deltas:[{}]'
                        args.append(negative_deltas)

                    # If there are pos spans, append them and the pos spans to the template and args
                    if s.native_histogram.pos_spans:
                        positive_spans = ','.join([f'{ps[0]}:{ps[1]}' for ps in s.native_histogram.pos_spans])
                        positive_deltas = ','.join(f'{pd}' for pd in s.native_histogram.pos_deltas)
                        nh_sample_template += ',positive_spans:[{}]'
                        args.append(positive_spans)
                        nh_sample_template += ',positive_deltas:[{}]'
                        args.append(positive_deltas)                       
                                                  
                    # Add closing brace
                    nh_sample_template += '}}'

                    # Format the template with the args
                    native_histogram = nh_sample_template.format(*args)
                    
                    if s.native_histogram.nh_exemplars:
                        for nh_ex in s.native_histogram.nh_exemplars:
                            nh_exemplarstr = _compose_exemplar_string(metric, s, nh_ex)
                            exemplarstr += nh_exemplarstr

                value = ''
                if s.native_histogram:
                    value = native_histogram
                elif s.value is not None:
                    value = floatToGoString(s.value)
                if (escaping != ALLOWUTF8) or _is_valid_legacy_metric_name(s.name):
                    output.append('{}{} {}{}{}\n'.format(
                        _escape(s.name, escaping, _is_legacy_labelname_rune),
                        labelstr,
                        value,
                        timestamp,
                        exemplarstr
                    ))
                else:
                    output.append('{} {}{}{}\n'.format(
                        labelstr,
                        value,
                        timestamp,
                        exemplarstr
                    ))
        except Exception as exception:
            exception.args = (exception.args or ('',)) + (metric,)
            raise

    output.append('# EOF\n')
    return ''.join(output).encode('utf-8')

