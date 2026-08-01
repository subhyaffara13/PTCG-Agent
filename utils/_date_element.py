
def _date_element(date: datetime, ctx: SimpleNamespace) -> etree.Element:
    el = etree.Element("date")
    el.text = _date_to_string(date)
    return el

