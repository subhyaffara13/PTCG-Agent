
def _df_bar_xyheight_from_ax_helper(df_bar_data, ax, subplot_division):
    subplot_data_df_list = []

    # get xy and height of squares representing data, separated by subplots
    for i in range(len(subplot_division)):
        subplot_data = np.array(
            [
                (x.get_x(), x.get_y(), x.get_height())
                for x in ax[i].findobj(plt.Rectangle)
                if x.get_height() in df_bar_data
            ]
        )
        subplot_data_df_list.append(
            DataFrame(data=subplot_data, columns=["x_coord", "y_coord", "height"])
        )

    return subplot_data_df_list

