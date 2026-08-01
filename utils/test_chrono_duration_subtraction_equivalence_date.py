
def test_chrono_duration_subtraction_equivalence_date():
    date1 = datetime.date.today()
    date2 = datetime.date.today()

    diff = date2 - date1
    cpp_diff = m.test_chrono4(date2, date1)

    assert cpp_diff == diff

