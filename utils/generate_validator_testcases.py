
def generate_validator_testcases(valid):
    validation_tests = (
        {'validator': validate_bool,
         'success': (*((_, True) for _ in
                       ('t', 'y', 'yes', 'on', 'true', '1', 1, True)),
                     *((_, False) for _ in
                       ('f', 'n', 'no', 'off', 'false', '0', 0, False))),
         'fail': ((_, ValueError)
                  for _ in ('aardvark', 2, -1, [], ))
         },
        {'validator': validate_stringlist,
         'success': (('', []),
                     ('a,b', ['a', 'b']),
                     ('aardvark', ['aardvark']),
                     ('aardvark, ', ['aardvark']),
                     ('aardvark, ,', ['aardvark']),
                     (['a', 'b'], ['a', 'b']),
                     (('a', 'b'), ['a', 'b']),
                     (iter(['a', 'b']), ['a', 'b']),
                     (np.array(['a', 'b']), ['a', 'b']),
                     ),
         'fail': ((set(), ValueError),
                  (1, ValueError),
                  )
         },
        {'validator': _listify_validator(validate_int, n=2),
         'success': ((_, [1, 2])
                     for _ in ('1, 2', [1.5, 2.5], [1, 2],
                               (1, 2), np.array((1, 2)))),
         'fail': ((_, ValueError)
                  for _ in ('aardvark', ('a', 1),
                            (1, 2, 3)
                            ))
         },
        {'validator': _listify_validator(validate_float, n=2),
         'success': ((_, [1.5, 2.5])
                     for _ in ('1.5, 2.5', [1.5, 2.5], [1.5, 2.5],
                               (1.5, 2.5), np.array((1.5, 2.5)))),
         'fail': ((_, ValueError)
                  for _ in ('aardvark', ('a', 1), (1, 2, 3), (None, ), None))
         },
        {'validator': validate_cycler,
         'success': (('cycler("color", "rgb")',
                      cycler("color", 'rgb')),
                     ('cycler("color", "Dark2")',
                      cycler("color", mpl.color_sequences["Dark2"])),
                     (cycler('linestyle', ['-', '--']),
                      cycler('linestyle', ['-', '--'])),
                     ("""(cycler("color", ["r", "g", "b"]) +
                          cycler("mew", [2, 3, 5]))""",
                      (cycler("color", 'rgb') +
                       cycler("markeredgewidth", [2, 3, 5]))),
                     ("cycler(c='rgb', lw=[1, 2, 3])",
                      cycler('color', 'rgb') + cycler('linewidth', [1, 2, 3])),
                     ("cycler('c', 'rgb') * cycler('linestyle', ['-', '--'])",
                      (cycler('color', 'rgb') *
                       cycler('linestyle', ['-', '--']))),
                     (cycler('ls', ['-', '--']),
                      cycler('linestyle', ['-', '--'])),
                     (cycler(mew=[2, 5]),
                      cycler('markeredgewidth', [2, 5])),
                     ("2 * cycler('color', 'rgb')", 2 * cycler('color', 'rgb')),
                     ("2 * cycler('color', 'r' + 'gb')", 2 * cycler('color', 'rgb')),
                     ("cycler(c='r' + 'gb', lw=[1, 2, 3])",
                      cycler('color', 'rgb') + cycler('linewidth', [1, 2, 3])),
                     ("cycler('color', 'rgb') * 2", cycler('color', 'rgb') * 2),
                     ("concat(cycler('color', 'rgb'), cycler('color', 'cmk'))",
                      cycler('color', list('rgbcmk'))),
                     ("cycler('color', 'rgbcmk')[:3]", cycler('color', list('rgb'))),
                     ("cycler('color', 'rgb')[::-1]", cycler('color', list('bgr'))),
                     ),
         # validate_cycler() parses an arbitrary string using a safe
         # AST-based parser (no eval). These tests verify that only valid
         # cycler expressions are accepted.
         'fail': ((4, ValueError),  # Gotta be a string or Cycler object
                  ('cycler("bleh, [])', ValueError),  # syntax error
                  ("cycler('color', 'rgb') * * cycler('color', 'rgb')",  # syntax error
                  ValueError),
                  ('Cycler("linewidth", [1, 2, 3])',
                   ValueError),  # only 'cycler()' function is allowed
                  # do not allow dunder in string literals
                  ("cycler('c', [j.__class__(j) for j in ['r', 'b']])",
                   ValueError),
                  ("cycler('c', [j. __class__(j) for j in ['r', 'b']])",
                   ValueError),
                  ("cycler('c', [j.\t__class__(j) for j in ['r', 'b']])",
                   ValueError),
                  ("cycler('c', [j.\u000c__class__(j) for j in ['r', 'b']])",
                   ValueError),
                  ("cycler('c', [j.__class__(j).lower() for j in ['r', 'b']])",
                   ValueError),
                  # list comprehensions are arbitrary code, even if "safe"
                  ("cycler('color', [x for x in ['r', 'g', 'b']])",
                   ValueError),
                  ('1 + 2', ValueError),  # doesn't produce a Cycler object
                  ('os.system("echo Gotcha")', ValueError),  # os not available
                  ('import os', ValueError),  # should not be able to import
                  ('def badjuju(a): return a; badjuju(cycler("color", "rgb"))',
                   ValueError),  # Should not be able to define anything
                  # even if it does return a cycler
                  ('cycler("waka", [1, 2, 3])', ValueError),  # not a property
                  ('cycler(c=[1, 2, 3])', ValueError),  # invalid values
                  ("cycler(lw=['a', 'b', 'c'])", ValueError),  # invalid values
                  (cycler('waka', [1, 3, 5]), ValueError),  # not a property
                  (cycler('color', ['C1', 'r', 'g']), ValueError)  # no CN
                  )
         },
        {'validator': validate_hatch,
         'success': (('--|', '--|'), ('\\oO', '\\oO'),
                     ('/+*/.x', '/+*/.x'), ('', '')),
         'fail': (('--_', ValueError),
                  (8, ValueError),
                  ('X', ValueError)),
         },
        {'validator': validate_colorlist,
         'success': (('r,g,b', ['r', 'g', 'b']),
                     (['r', 'g', 'b'], ['r', 'g', 'b']),
                     ('r, ,', ['r']),
                     (['', 'g', 'blue'], ['g', 'blue']),
                     ([np.array([1, 0, 0]), np.array([0, 1, 0])],
                     np.array([[1, 0, 0], [0, 1, 0]])),
                     (np.array([[1, 0, 0], [0, 1, 0]]),
                     np.array([[1, 0, 0], [0, 1, 0]])),
                     ),
         'fail': (('fish', ValueError),
                  ),
         },
        {'validator': validate_color,
         'success': (('None', 'none'),
                     ('none', 'none'),
                     ('AABBCC', '#AABBCC'),  # RGB hex code
                     ('AABBCC00', '#AABBCC00'),  # RGBA hex code
                     ('tab:blue', 'tab:blue'),  # named color
                     ('C12', 'C12'),  # color from cycle
                     ('(0, 1, 0)', (0.0, 1.0, 0.0)),  # RGB tuple
                     ((0, 1, 0), (0, 1, 0)),  # non-string version
                     ('(0, 1, 0, 1)', (0.0, 1.0, 0.0, 1.0)),  # RGBA tuple
                     ((0, 1, 0, 1), (0, 1, 0, 1)),  # non-string version
                     ),
         'fail': (('tab:veryblue', ValueError),  # invalid name
                  ('(0, 1)', ValueError),  # tuple with length < 3
                  ('(0, 1, 0, 1, 0)', ValueError),  # tuple with length > 4
                  ('(0, 1, none)', ValueError),  # cannot cast none to float
                  ('(0, 1, "0.5")', ValueError),  # last one not a float
                  ),
         },
        {'validator': _validate_color_or_linecolor,
         'success': (('linecolor', 'linecolor'),
                     ('markerfacecolor', 'markerfacecolor'),
                     ('mfc', 'markerfacecolor'),
                     ('markeredgecolor', 'markeredgecolor'),
                     ('mec', 'markeredgecolor')
                     ),
         'fail': (('line', ValueError),
                  ('marker', ValueError)
                  )
         },
        {'validator': validate_hist_bins,
         'success': (('auto', 'auto'),
                     ('fd', 'fd'),
                     ('10', 10),
                     ('1, 2, 3', [1, 2, 3]),
                     ([1, 2, 3], [1, 2, 3]),
                     (np.arange(15), np.arange(15))
                     ),
         'fail': (('aardvark', ValueError),
                  )
         },
        {'validator': validate_markevery,
         'success': ((None, None),
                     (1, 1),
                     (0.1, 0.1),
                     ((1, 1), (1, 1)),
                     ((0.1, 0.1), (0.1, 0.1)),
                     ([1, 2, 3], [1, 2, 3]),
                     (slice(2), slice(None, 2, None)),
                     (slice(1, 2, 3), slice(1, 2, 3))
                     ),
         'fail': (((1, 2, 3), TypeError),
                  ([1, 2, 0.3], TypeError),
                  (['a', 2, 3], TypeError),
                  ([1, 2, 'a'], TypeError),
                  ((0.1, 0.2, 0.3), TypeError),
                  ((0.1, 2, 3), TypeError),
                  ((1, 0.2, 0.3), TypeError),
                  ((1, 0.1), TypeError),
                  ((0.1, 1), TypeError),
                  (('abc'), TypeError),
                  ((1, 'a'), TypeError),
                  ((0.1, 'b'), TypeError),
                  (('a', 1), TypeError),
                  (('a', 0.1), TypeError),
                  ('abc', TypeError),
                  ('a', TypeError),
                  (object(), TypeError)
                  )
         },
        {'validator': _validate_linestyle,
         'success': (('-', '-'), ('solid', 'solid'),
                     ('--', '--'), ('dashed', 'dashed'),
                     ('-.', '-.'), ('dashdot', 'dashdot'),
                     (':', ':'), ('dotted', 'dotted'),
                     ('', ''), (' ', ' '),
                     ('None', 'none'), ('none', 'none'),
                     ('DoTtEd', 'dotted'),  # case-insensitive
                     ('1, 3', (0, (1, 3))),
                     ([1.23, 456], (0, [1.23, 456.0])),
                     ([1, 2, 3, 4], (0, [1.0, 2.0, 3.0, 4.0])),
                     ((0, [1, 2]), (0, [1, 2])),
                     ((-1, [1, 2]), (-1, [1, 2])),
                     ),
         'fail': (('aardvark', ValueError),  # not a valid string
                  (b'dotted', ValueError),
                  ('dotted'.encode('utf-16'), ValueError),
                  ([1, 2, 3], ValueError),  # sequence with odd length
                  (1.23, ValueError),  # not a sequence
                  (("a", [1, 2]), ValueError),  # wrong explicit offset
                  ((None, [1, 2]), ValueError),  # wrong explicit offset
                  ((1, [1, 2, 3]), ValueError),  # odd length sequence
                  (([1, 2], 1), ValueError),  # inverted offset/onoff
                  )
         },
    )

    for validator_dict in validation_tests:
        validator = validator_dict['validator']
        if valid:
            for arg, target in validator_dict['success']:
                yield validator, arg, target
        else:
            for arg, error_type in validator_dict['fail']:
                yield validator, arg, error_type

