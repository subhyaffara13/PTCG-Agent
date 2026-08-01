
def geom_df():
    return DataFrame(
        {
            "shape": ["square", "circle", "triangle"],
            "degrees": [360, 360, 180],
            "sides": [4, np.nan, 3],
        }
    )

