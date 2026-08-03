import re

def endofcell_marker(source, comment):
    """Issues #31 #38:  does the cell contain a blank line? In that case
    we add an end-of-cell marker"""
    endofcell = "-"
    while True:
        endofcell_re = re.compile(rf"^{re.escape(comment)}( )" + endofcell + r"\s*$")
        if list(filter(endofcell_re.match, source)):
            endofcell = endofcell + "-"
        else:
            return endofcell

