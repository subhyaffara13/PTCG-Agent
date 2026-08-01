
def normalize_report_meta(content: list[str]) -> list[str]:
    # libxml 2.15 and newer emits the "modern" version of this <meta> element.
    # Normalize the old style to look the same.
    html_meta = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
    return ['<meta charset="UTF-8">' if x == html_meta else x for x in content]

