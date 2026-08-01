
def dict_to_codeclimate_issues(results, threshold='B'):
    '''Convert a dictionary holding CC analysis results into Code Climate
     issue json.'''
    codeclimate_issues = []
    content = get_content()
    error_content = 'We encountered an error attempting to analyze this line.'

    for path in results:
        info = results[path]
        if type(info) is dict and info.get('error'):
            description = 'Error: {0}'.format(info.get('error', error_content))
            beginline = re.search(r'\d+', description)
            error_category = 'Bug Risk'

            if beginline:
                beginline = int(beginline.group())
            else:
                beginline = 1

            endline = beginline
            remediation_points = 1000000
            fingerprint = get_fingerprint(path, ['error'])
            codeclimate_issues.append(
                format_cc_issue(
                    path,
                    description,
                    error_content,
                    error_category,
                    beginline,
                    endline,
                    remediation_points,
                    fingerprint,
                )
            )
        else:
            for offender in info:
                beginline = offender['lineno']
                endline = offender['endline']
                complexity = offender['complexity']
                category = 'Complexity'
                description = (
                    'Cyclomatic complexity is too high in {0} {1}. '
                    '({2})'.format(
                        offender['type'], offender['name'], complexity
                    )
                )
                remediation_points = get_remediation_points(
                    complexity, threshold
                )
                fingerprint = get_fingerprint(
                    path, [offender['type'], offender['name']]
                )

                if remediation_points > 0:
                    codeclimate_issues.append(
                        format_cc_issue(
                            path,
                            description,
                            content,
                            category,
                            beginline,
                            endline,
                            remediation_points,
                            fingerprint,
                        )
                    )
    return codeclimate_issues

