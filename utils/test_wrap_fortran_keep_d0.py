
def test_wrap_fortran_keep_d0():
    printer = FCodePrinter()
    lines = [
        '      this_variable_is_very_long_because_we_try_to_test_line_break=1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break =1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break  = 1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break   = 1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break    = 1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break = 10.0d0'
    ]
    expected = [
        '      this_variable_is_very_long_because_we_try_to_test_line_break=1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break =',
        '     @ 1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break  =',
        '     @ 1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break   =',
        '     @ 1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break    =',
        '     @ 1.0d0',
        '      this_variable_is_very_long_because_we_try_to_test_line_break =',
        '     @ 10.0d0'
    ]
    assert printer._wrap_fortran(lines) == expected

