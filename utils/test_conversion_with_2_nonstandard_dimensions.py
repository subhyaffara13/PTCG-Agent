
def test_conversion_with_2_nonstandard_dimensions():
    good_grade = Quantity("good_grade")
    kilo_good_grade = Quantity("kilo_good_grade")
    centi_good_grade = Quantity("centi_good_grade")

    kilo_good_grade.set_global_relative_scale_factor(1000, good_grade)
    centi_good_grade.set_global_relative_scale_factor(S.One/10**5, kilo_good_grade)

    charity_points = Quantity("charity_points")
    milli_charity_points = Quantity("milli_charity_points")
    missions = Quantity("missions")

    milli_charity_points.set_global_relative_scale_factor(S.One/1000, charity_points)
    missions.set_global_relative_scale_factor(251, charity_points)

    assert convert_to(
        kilo_good_grade*milli_charity_points*millimeter,
        [centi_good_grade, missions, centimeter]
    ) == S.One * 10**5 / (251*1000) / 10 * centi_good_grade*missions*centimeter

