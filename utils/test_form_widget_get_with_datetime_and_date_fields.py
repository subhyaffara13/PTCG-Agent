
def test_form_widget_get_with_datetime_and_date_fields():
    from matplotlib.backends.backend_qt import _create_qApp
    _create_qApp()

    form = [
        ("Datetime field", datetime(year=2021, month=3, day=11)),
        ("Date field", date(year=2021, month=3, day=11))
    ]
    widget = _formlayout.FormWidget(form)
    widget.setup()
    values = widget.get()
    assert values == [
        datetime(year=2021, month=3, day=11),
        date(year=2021, month=3, day=11)
    ]

