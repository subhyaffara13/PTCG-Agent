import json

def format_cc_issue(
    path,
    description,
    content,
    category,
    beginline,
    endline,
    remediation_points,
    fingerprint,
):
    '''Return properly formatted Code Climate issue json.'''
    issue = {
        'type': 'issue',
        'check_name': 'Complexity',
        'description': description,
        'content': {'body': content,},
        'categories': [category],
        'fingerprint': fingerprint,
        'location': {
            'path': path,
            'lines': {'begin': beginline, 'end': endline,},
        },
        'remediation_points': remediation_points,
    }
    return json.dumps(issue)

