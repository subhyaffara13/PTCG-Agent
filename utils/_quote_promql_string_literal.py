import json

def _quote_promql_string_literal(value: str) -> str:
    """Render ``value`` as a PromQL double-quoted string literal.

    PromQL string literals follow Go's escape rules
    (https://prometheus.io/docs/prometheus/latest/querying/basics/): a
    backslash begins an escape sequence and a bare ``"`` ends the literal.
    Without escaping, callers that accept arbitrary user-supplied values
    (like the ``api_key`` filter on ``/global/spend/logs``) can inject extra
    label matchers or selectors and read cross-tenant metrics.

    JSON's quoting rules are a strict subset of Go's, so ``json.dumps`` of
    a Python string produces a literal Prometheus accepts: ``\\``, ``\\"``,
    and the standard ``\\n`` / ``\\t`` / ``\\uNNNN`` control-character
    escapes. The returned value already includes the surrounding quotes.
    """
    return json.dumps(value, ensure_ascii=False)

