
def test_cc_to_codeclimate():
    actual_results = tools.dict_to_codeclimate_issues(
        {'filename': CC_TO_CODECLIMATE_CASE}
    )
    expected_results = [
        json.dumps(
            {
                'description': 'Cyclomatic complexity is too high in function foo. (6)',
                'check_name': 'Complexity',
                'content': {'body': tools.get_content()},
                'location': {
                    'path': 'filename',
                    'lines': {'begin': 12, 'end': 16},
                },
                'type': 'issue',
                'categories': ['Complexity'],
                'remediation_points': 1100000,
                'fingerprint': 'afbe2b8d9a57fde5f3235ec97e7a22e1',
            }
        ),
        json.dumps(
            {
                'description': 'Cyclomatic complexity is too high in class Classname. (8)',
                'check_name': 'Complexity',
                'content': {'body': tools.get_content()},
                'location': {
                    'path': 'filename',
                    'lines': {'begin': 17, 'end': 29},
                },
                'type': 'issue',
                'categories': ['Complexity'],
                'remediation_points': 1300000,
                'fingerprint': '8caecbb525375d825b95c23bc8f881d7',
            }
        ),
    ]

    actual_sorted = []
    for i in actual_results:
        actual_sorted.append(json.loads(i))

    expected_sorted = []
    for i in expected_results:
        expected_sorted.append(json.loads(i))

    assert actual_sorted == expected_sorted

