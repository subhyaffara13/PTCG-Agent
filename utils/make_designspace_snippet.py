
def makeDesignspaceSnippet(axisTag, axisName, axisLimit, mapping):
    """Make a designspace snippet for a single axis."""

    designspaceSnippet = (
        '    <axis tag="%s" name="%s" minimum="%g" default="%g" maximum="%g"'
        % ((axisTag, axisName) + axisLimit)
    )
    if mapping:
        designspaceSnippet += ">\n"
    else:
        designspaceSnippet += "/>"

    for key, value in mapping.items():
        designspaceSnippet += '      <map input="%g" output="%g"/>\n' % (key, value)

    if mapping:
        designspaceSnippet += "    </axis>"

    return designspaceSnippet

