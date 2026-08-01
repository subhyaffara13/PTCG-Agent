
def _escape_comment(s):
    s = _escape_cdata(s)
    return _escape_xml_comment.sub('- ', s)

