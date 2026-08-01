
def test_longtable_caption_label(styler, caption, cap_exp, label, lab_exp):
    cap_exp1 = f"\\caption{cap_exp[1]}{cap_exp[0]}"
    cap_exp2 = f"\\caption[]{cap_exp[0]}"

    expected = dedent(
        f"""\
        {cap_exp1}{lab_exp} \\\\
         & A & B & C \\\\
        \\endfirsthead
        {cap_exp2} \\\\
        """
    )
    assert expected in styler.to_latex(
        environment="longtable", caption=caption, label=label
    )

