
def _strip_xml_ns(tag):
    # ElementTree API doesn't provide a way to ignore XML namespaces in tags
    # so we here strip them ourselves: cf. https://bugs.python.org/issue18304
    return tag.split("}", 1)[1] if "}" in tag else tag

