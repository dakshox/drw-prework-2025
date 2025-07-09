# cmds/plot_utils.py

import matplotlib.pyplot as plt

def scatter_by_type(
    df,
    x: str,
    y: str,
    type_col: str = 'type',
    color_map: dict = None,
    xlabel: str = None,
    ylabel: str = None,
    title: str = None,
    ax: plt.Axes = None,
    **scatter_kwargs
) -> plt.Axes:
    """
    Scatter-plot df[y] vs. df[x], coloring and labeling by unique values in df[type_col].

    Parameters
    ----------
    df : pandas.DataFrame
    x : str
        Column name for the x-axis.
    y : str
        Column name for the y-axis.
    type_col : str
        Column whose unique values define colors/legend labels.
    color_map : dict
        Mapping from each type to a matplotlib‐style color spec.
    xlabel, ylabel, title : str, optional
        Axis labels and plot title.
    ax : matplotlib.axes.Axes, optional
        If provided, use this Axes; otherwise creates a new one.
    scatter_kwargs : dict
        Passed through to ax.scatter (e.g. alpha, s, marker).

    Returns
    -------
    ax : matplotlib.axes.Axes
    """
    if color_map is None:
        color_map = {}

    if ax is None:
        fig, ax = plt.subplots()

    for t, grp in df.groupby(type_col):
        ax.scatter(
            grp[x],
            grp[y],
            label=t,
            color=color_map.get(t, 'gray'),
            **scatter_kwargs
        )

    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    ax.legend(title=type_col.capitalize(), loc='best', frameon=True)
    plt.tight_layout()
    return ax
