
def _escape_grouping_key(k, v):
    if v == "":
        # Per https://github.com/prometheus/pushgateway/pull/346.
        return k + "@base64", "="
    elif '/' in v or ' ' in v:
        # Added in Pushgateway 0.9.0.
        # Use base64 encoding for values containing slashes or spaces
        return k + "@base64", base64.urlsafe_b64encode(v.encode("utf-8")).decode("utf-8")
    else:
        return k, quote_plus(v)

