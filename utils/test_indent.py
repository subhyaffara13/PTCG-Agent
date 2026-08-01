
def test_indent():
    codelines = (
        'subroutine test(a)\n'
        'integer :: a, i, j\n'
        '\n'
        'do\n'
        'do \n'
        'do j = 1, 5\n'
        'if (a>b) then\n'
        'if(b>0) then\n'
        'a = 3\n'
        'donot_indent_me = 2\n'
        'do_not_indent_me_either = 2\n'
        'ifIam_indented_something_went_wrong = 2\n'
        'if_I_am_indented_something_went_wrong = 2\n'
        'end should not be unindented here\n'
        'end if\n'
        'endif\n'
        'end do\n'
        'end do\n'
        'enddo\n'
        'end subroutine\n'
        '\n'
        'subroutine test2(a)\n'
        'integer :: a\n'
        'do\n'
        'a = a + 1\n'
        'end do \n'
        'end subroutine\n'
    )
    expected = (
        'subroutine test(a)\n'
        'integer :: a, i, j\n'
        '\n'
        'do\n'
        '   do \n'
        '      do j = 1, 5\n'
        '         if (a>b) then\n'
        '            if(b>0) then\n'
        '               a = 3\n'
        '               donot_indent_me = 2\n'
        '               do_not_indent_me_either = 2\n'
        '               ifIam_indented_something_went_wrong = 2\n'
        '               if_I_am_indented_something_went_wrong = 2\n'
        '               end should not be unindented here\n'
        '            end if\n'
        '         endif\n'
        '      end do\n'
        '   end do\n'
        'enddo\n'
        'end subroutine\n'
        '\n'
        'subroutine test2(a)\n'
        'integer :: a\n'
        'do\n'
        '   a = a + 1\n'
        'end do \n'
        'end subroutine\n'
    )
    p = FCodePrinter({'source_format': 'free'})
    result = p.indent_code(codelines)
    assert result == expected


def test_indent():
  assert ds.outdent(''.join(ds.getsourcelines(tm.quadratic)[0])) == ''.join(ds.getsourcelines(tm.quadratic, lstrip=True)[0])
  assert ds.indent(''.join(ds.getsourcelines(tm.quadratic, lstrip=True)[0]), 2) == ''.join(ds.getsourcelines(tm.quadratic)[0])

