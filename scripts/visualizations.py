import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import os
import numpy as np

def create_boxplot(numeric_data):
    """
    Creates 3 boxplots in a row for numeric columns and saves the figure.

    :param numeric_data: DataFrame with numeric columns.
    :return: None
    """
    columns = numeric_data.columns
    num_plots = len(columns)

    if num_plots == 0:
        print("No numeric data.")
        return

    cols = 3
    rows = math.ceil(num_plots / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = axes.flatten()

    name = ""
    for i, column in enumerate(columns):
        sns.boxplot(y=numeric_data[column], ax=axes[i])
        axes[i].set_title(f'Boxplot for {column}')
        name = name + str(column)+"-"

    plt.tight_layout()
    os.makedirs('processed_data', exist_ok=True)
    os.makedirs('processed_data/boxplots', exist_ok=True)
    plt.savefig(f'processed_data/boxplots/{name}_boxplot.png')
    plt.close()

def create_violinplot(numeric_data):
    """
    Creates 3 violin plots in a row for numeric columns and saves the figure.

    :param numeric_data: DataFrame with numeric columns.
    :return: None
    """
    columns = numeric_data.columns
    num_plots = len(columns)

    if num_plots == 0:
        print("No numeric data.")
        return

    cols = 3
    rows = math.ceil(num_plots / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
    axes = axes.flatten()

    name = ""
    for i, column in enumerate(columns):
        sns.violinplot(y=numeric_data[column], ax=axes[i])
        axes[i].set_title(f'Violinplot for {column}')
        name = name + str(column) + "-"

    plt.tight_layout()
    os.makedirs('processed_data', exist_ok=True)
    os.makedirs('processed_data/violinplots', exist_ok=True)
    plt.savefig(f'processed_data/violinplots/{name}_violinplot.png')
    plt.close()

def plot_errorbars_from_df(df, columns, error_spec=("sd", 1), jitter=0.1):
    """
    Plots error bars and raw data points for selected columns.

    :param df: DataFrame containing the data.
    :param columns: List of column names to plot.
    :param error_spec: Tuple defining the type and scale of error bar (e.g., ("sd", 1)).
    :param jitter: Amount of jitter to add to the strip plot.
    :return: None
    """
    for column in columns:
        data = df[column].dropna()
        f, axs = plt.subplots(2, figsize=(10, 2), sharex=True, layout="tight", height_ratios=[0.5, 0.8])

        sns.pointplot(
            x=data,
            errorbar=error_spec,
            capsize=0.6,
            color="tab:blue",
            ax=axs[0]
        )

        sns.stripplot(
            x=data,
            jitter=jitter,
            color="tab:blue",
            size=3,
            alpha=0.6,
            ax=axs[1]
        )

        axs[0].set_title(f"{column} – Mean ± {error_spec[1]}×{error_spec[0].upper()}")
        axs[1].set_xlabel(column)
        axs[0].set_ylabel("")
        axs[1].set_ylabel("")

        plt.tight_layout()
        os.makedirs('processed_data', exist_ok=True)
        os.makedirs('processed_data/processed_data_pointplots', exist_ok=True)
        plt.savefig(f'processed_data/processed_data_pointplots/{column}_pointplot_with_error.png')
        plt.close()


def histograms_from_df(df, columns, bins=100):
    """
    Histograms from df function.

    :param df: DataFrame containing the data.
    :param columns: List of column names to plot.
    :param bins: Number of bins.
    :return: Nothing.
    """

    for column in columns:
        sns.displot(data=df, x=column, bins=bins, kde=False, color='skyblue', height=4, aspect=2.5)
        plt.title(f'Histogram: {column}')
        plt.xlabel(column)
        plt.ylabel('Cardinality')

        plt.tight_layout()
        os.makedirs('processed_data', exist_ok=True)
        os.makedirs('processed_data/processed_data_histograms', exist_ok=True)
        plt.savefig(f'processed_data/processed_data_histograms/{column}_histogram.png')  # saving at the end
        plt.close()


def cond_histograms_from_df(df, columns, cond, bins=100):
    """
    Cond histograms from df function.

    :param df: DataFrame containing the data.
    :param columns: List of column names to plot.
    :param cond: Condition column.
    :param bins: Number of bins.
    :return: Nothing.
    """

    for column in columns:
        g = sns.displot(data=df, x=column, bins=bins, palette="tab10", hue=cond, kde=False, color='skyblue', height=4,
                        aspect=2.5)
        plt.title(f'Histogram: {column}')
        g._legend.set_bbox_to_anchor((1.05, 0.5))  # prawa strona, wyśrodkowana w pionie
        plt.xlabel(column)
        plt.ylabel('Cardinality')

        plt.tight_layout()
        os.makedirs('processed_data', exist_ok=True)
        os.makedirs('processed_data/processed_data_cond_histograms', exist_ok=True)
        plt.savefig(f'processed_data/processed_data_cond_histograms/{column}_cond_histogram.png')  # saving at the end
        plt.close()


def heatmap_from_df(df, x, y, value="Cardinality", round_to=1, median=True):
    """
    Heatmap from df function.

    """

    df = df.copy()  # not to change the original

    # roundind of the x and y values

    if np.issubdtype(df[x].dtype, np.number):
        df[x] = df[x].round(round_to)

    if np.issubdtype(df[y].dtype, np.number):
        df[y] = df[y].round(round_to)

    if value == "Cardinality":  # count cardinality by default
        tab = df.pivot_table(index=y, columns=x, aggfunc='size', fill_value=0)
    else:
        tab = df.pivot_table(index=y, columns=x, values=value, aggfunc='median' if median else 'mean')

    plt.figure(figsize=(10, 6))
    sns.heatmap(tab, annot=False, cmap="YlGnBu")

    plt.gca().invert_yaxis()  # turn y axis correct way

    plt.title(f"Heatmap: {value} / {y} and {x}")
    plt.tight_layout()

    os.makedirs('processed_data/processed_data_heatmaps', exist_ok=True)
    plt.savefig(f'processed_data/processed_data_heatmaps/{y}-{x}_heatmap.png')
    plt.close()


def regplot_from_df(df, x, y, order=1, round_to=None):
    """
    Regplot from df function.

    """
    df = df.copy()  # copying in order not to modify the original

    # Rounding of data if given
    if round_to is not None:
        if np.issubdtype(df[x].dtype, np.number):
            df[x] = df[x].round(round_to)
        if np.issubdtype(df[y].dtype, np.number):
            df[y] = df[y].round(round_to)

    plt.figure(figsize=(10, 6))

    sns.regplot(data=df, x=x, y=y, order=order, color='tab:blue', x_jitter=0.1,
                line_kws={
                    "color": "red",  # kolor linii
                    "linewidth": 2.5,  # grubość
                    "linestyle": "--"  # styl przerywany
                },
                scatter_kws={"alpha": 0.5}
                )

    plt.title(f"Regplot: {y} / {x}")
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    plt.tight_layout()

    os.makedirs('processed_data/processed_data_regplots', exist_ok=True)
    plt.savefig(f'processed_data/processed_data_regplots/{x}-{y}_regplot.png')
    plt.close()

