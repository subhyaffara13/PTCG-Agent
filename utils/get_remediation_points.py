
def get_remediation_points(complexity, grade_threshold):
    '''Calculate quantity of remediation work needed to reduce complexity to grade
    threshold permitted.'''
    grade_to_max_permitted_cc = {
        'B': 5,
        'C': 10,
        'D': 20,
        'E': 30,
        'F': 40,
    }

    threshold = grade_to_max_permitted_cc.get(grade_threshold, 5)

    if complexity and complexity > threshold:
        return 1000000 + 100000 * (complexity - threshold)
    else:
        return 0

