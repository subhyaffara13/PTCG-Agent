
def _model_handler(_):
    fig, ax = plt.subplots()
    fig.savefig(BytesIO(), format="pdf")
    plt.close()

