
def dict_to_xml(results):
    '''Convert a dictionary holding CC analysis result into a string containing
    xml.'''
    ccm = et.Element('ccm')
    for filename, blocks in results.items():
        for block in blocks:
            metric = et.SubElement(ccm, 'metric')
            et.SubElement(metric, 'complexity').text = str(block['complexity'])

            unit = et.SubElement(metric, 'unit')
            name = block['name']
            if 'classname' in block:
                name = '{0}.{1}'.format(block['classname'], block['name'])
            unit.text = name

            et.SubElement(metric, 'classification').text = block['rank']
            et.SubElement(metric, 'file').text = filename
            et.SubElement(metric, 'startLineNumber').text = str(
                block['lineno']
            )
            et.SubElement(metric, 'endLineNumber').text = str(block['endline'])
    return et.tostring(ccm).decode('utf-8')

