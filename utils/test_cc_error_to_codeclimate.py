import json

def test_cc_error_to_codeclimate():
    error_result = {'error': 'Error: invalid syntax (<unknown>, line 100)'}

    expected_results = [
        json.dumps(
            {
                'description': 'Error: Error: invalid syntax (<unknown>, line 100)',
                'check_name': 'Complexity',
                'content': {
                    'body': 'We encountered an error attempting to analyze this line.'
                },
                'location': {
                    'path': 'filename',
                    'lines': {'begin': 100, 'end': 100},
                },
                'type': 'issue',
                'categories': ['Bug Risk'],
                'remediation_points': 1000000,
                'fingerprint': '10ac332cd7f638664e8865b098a1707c',
            }
        ),
    ]

    actual_results = tools.dict_to_codeclimate_issues(
        {'filename': error_result}
    )

    actual_sorted = []
    for i in actual_results:
        actual_sorted.append(json.loads(i))

    expected_sorted = []
    for i in expected_results:
        expected_sorted.append(json.loads(i))

    assert actual_sorted == expected_sorted

