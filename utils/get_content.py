
def get_content():
    '''Return explanation string for Code Climate issue document.'''
    content = [
        '##Cyclomatic Complexity',
        'Cyclomatic Complexity corresponds to the number of decisions '
        'a block of code contains plus 1. This number (also called '
        'McCabe number) is equal to the number of linearly independent '
        'paths through the code. This number can be used as a guide '
        'when testing conditional logic in blocks.\n',
        'Radon analyzes the AST tree of a Python program to compute '
        'Cyclomatic Complexity. Statements have the following effects '
        'on Cyclomatic Complexity:\n\n',
        '| Construct | Effect on CC | Reasoning |',
        '| --------- | ------------ | --------- |',
        '| if | +1 | An *if* statement is a single decision. |',
        '| elif| +1| The *elif* statement adds another decision. |',
        '| else| +0| The *else* statement does not cause a new '
        'decision. The decision is at the *if*. |',
        '| for| +1| There is a decision at the start of the loop. |',
        '| while| +1| There is a decision at the *while* statement. |',
        '| except| +1| Each *except* branch adds a new conditional '
        'path of execution. |',
        '| finally| +0| The finally block is unconditionally ' 'executed. |',
        '| with| +1| The *with* statement roughly corresponds to a '
        'try/except block (see PEP 343 for details). |',
        '| assert| +1| The *assert* statement internally roughly '
        'equals a conditional statement. |',
        '| Comprehension| +1| A list/set/dict comprehension of '
        'generator expression is equivalent to a for loop. |',
        '| Boolean Operator| +1| Every boolean operator (and, or) '
        'adds a decision point. |\n',
        'Source: http://radon.readthedocs.org/en/latest/intro.html',
    ]
    return '\n'.join(content)

