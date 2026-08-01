
def equalize_decl(doc):
    # etree and lxml differ on quotes and case in xml declaration
    if doc is not None:
        doc = doc.replace(
            '<?xml version="1.0" encoding="utf-8"?',
            "<?xml version='1.0' encoding='utf-8'?",
        )
    return doc

