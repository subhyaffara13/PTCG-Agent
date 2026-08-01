
def violin_plot_stats():
    datetimes = [
        datetime.datetime(2023, 2, 10),
        datetime.datetime(2023, 5, 18),
        datetime.datetime(2023, 6, 6)
    ]
    return [{
        'coords': datetimes,
        'vals': [1.2, 2.8, 1.5],
        'mean': 1.84,
        'median': 1.5,
        'min': 1.2,
        'max': 2.8,
        'quantiles': [1.2, 1.5, 2.8]
    }, {
        'coords': datetimes,
        'vals': [0.8, 1.1, 0.9],
        'mean': 0.94,
        'median': 0.9,
        'min': 0.8,
        'max': 1.1,
        'quantiles': [0.8, 0.9, 1.1]
    }]

