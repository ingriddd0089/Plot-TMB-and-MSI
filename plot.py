
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statannotations.Annotator import Annotator

def get_TMB(df, capture_size):
    "df is a DataFrame with columns as genes and rows as samples, value is the count of (nonsynonymous) mutations"
    "capture_size is the size of the capture in bases or Mb"
    total_count = df.sum(axis=1)
    capture_size = capture_size/1e6 if capture_size > 1e6 else capture_size
    tmb = total_count / capture_size
    df['TMB']=tmb
    return df

def plot_distribution(
    data,
    column='TMB',
    bins=30,
    color='steelblue',
    alpha=0.6,
    ylabel='Frequency',
    title=None,
    title_size=22,
    xlabel_size=20,
    ylabel_size=20,
    xticks_size=18,
    yticks_size=18,
    grid=True,
    save_path=None
):
    """
    Plots a histogram for a specified column in the DataFrame.

    Parameters:
        data (pd.DataFrame): Input dataframe.
        column (str): Column name to plot (e.g., 'TMB', 'MSI').
        grid (bool): Whether to show gridlines.
        save_path (str): Path to save the plot (without extension).
        output tiff without title, and png with title. 
    """
    if title is None:
        title = f'Distribution of {column} (n={data[column].dropna().shape[0]})'
    plt.figure(figsize=(5, 4))
    plt.rc('font',family='Times New Roman')
    ax = sns.histplot(data[column], bins=bins, color=color, alpha=alpha)
    ax.set_title(title, fontsize=title_size)
    ax.set_xlabel(column, fontsize=xlabel_size)
    ax.set_ylabel(ylabel, fontsize=ylabel_size)
    ax.tick_params(axis='x', labelsize=xticks_size)
    ax.tick_params(axis='y', labelsize=yticks_size)

    if grid:
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    if save_path:
        ax.set_title("")
        plt.savefig(f"{save_path}.tiff", dpi=300, pil_kwargs={"compression": "tiff_lzw"}, bbox_inches='tight')

        ax.set_title(title, fontsize=title_size)
        plt.savefig(f"{save_path}.png", dpi=300, bbox_inches='tight')
    else:
        ax.set_title(title, fontsize=title_size)

    plt.show()

def plot_group_comparison(
    df0,
    column,
    df1=None,
    ylabel="Value",
    title0="Group 1",
    title1="Group 2",
    log_transform=False,
    figsize=(6, 4),
    title_size=22,
    ylabel_size=20,
    xticks_size=18,
    yticks_size=18,
    palette0=None,
    palette1=None,
    group_column="group",
    group_order=None,
    save_path=None
):
    """
    Create boxplots to compare one or two cohorts by a categorical grouping.

    Parameters:
    - df0: First cohort DataFrame (required)
    - df1: Second cohort DataFrame (optional)
    - column: Column name to plot
    - ylabel: Y-axis label
    - title0, title1: Titles for each subplot
    - log_transform: Apply log1p transform to y-values
    - figsize: Figure size
    - title_size, ylabel_size, xticks_size, yticks_size: Font sizes for styling
    - palette0, palette1: Color palette dicts for each plot
    - group_column: Column in DataFrame used for grouping (e.g., 'group' or 'status')
    - group_order: Order of categories for group column (e.g., ["status 1", "status 2"])
    - save_path: File name (without extension) to save plots (.tiff and .png)
    """
    df0 = df0.copy()
    if df1 is not None:
        df1 = df1.copy()

    if log_transform:
        df0[column] = np.log1p(df0[column])
        if df1 is not None:
            df1[column] = np.log1p(df1[column])

    if group_order is None:
        all_labels = df0[group_column].dropna().unique().tolist()
        if df1 is not None:
            all_labels += df1[group_column].dropna().unique().tolist()
        group_order = sorted(set(all_labels))

    if palette0 is None:
        palette0 = {group_order[0]: "lightsteelblue", group_order[1]: "steelblue"} if len(group_order) == 2 else {}
    if palette1 is None:
        palette1 = {group_order[0]: "mistyrose", group_order[1]: "tomato"} if len(group_order) == 2 else {}

    plt.rc('font', family='Times New Roman')

    if df1 is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        sns.boxplot(x=group_column, y=column, data=df0, palette=palette0, hue=group_column,
                    ax=ax, order=group_order, legend=False)
        if len(group_order) == 2:
            annotator = Annotator(ax, [(group_order[0], group_order[1])], data=df0,
                                  x=group_column, y=column, order=group_order)
            annotator.configure(test='Mann-Whitney', text_format='star', loc='inside', fontsize=12)
            annotator.apply_and_annotate()
        ax.set_title(title0, fontsize=title_size)
        ax.set_xlabel("")
        ax.set_ylabel(ylabel, fontsize=ylabel_size)
        ax.tick_params(axis='x', labelsize=xticks_size)
        ax.tick_params(axis='y', labelsize=yticks_size)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()
        if save_path:
            ax.set_title("")
            plt.savefig(f"{save_path}.tiff", dpi=300, pil_kwargs={"compression": "tiff_lzw"}, bbox_inches='tight')
            ax.set_title(title0, fontsize=title_size)
            plt.savefig(f"{save_path}.png", dpi=300, bbox_inches='tight')

    else:
        fig, axes = plt.subplots(1, 2, figsize=figsize, sharey=True)
        for ax, df, palette, title in zip(axes, [df0, df1], [palette0, palette1], [title0, title1]):
            sns.boxplot(x=group_column, y=column, data=df, palette=palette, hue=group_column,
                        ax=ax, order=group_order, legend=False)
            if len(group_order) == 2:
                annotator = Annotator(ax, [(group_order[0], group_order[1])], data=df,
                                      x=group_column, y=column, order=group_order)
                annotator.configure(test='Mann-Whitney', text_format='star', loc='inside', fontsize=12)
                annotator.apply_and_annotate()
            ax.set_title(title, fontsize=title_size)
            ax.set_xlabel("")
            ax.set_ylabel(ylabel, fontsize=ylabel_size)
            ax.tick_params(axis='x', labelsize=xticks_size)
            ax.tick_params(axis='y', labelsize=yticks_size)
            ax.grid(axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()
        if save_path:
            for ax in axes:
                ax.set_title("")
            plt.savefig(f"{save_path}.tiff", dpi=300, pil_kwargs={"compression": "tiff_lzw"}, bbox_inches='tight')
            for ax, title in zip(axes, [title0, title1]):
                ax.set_title(title, fontsize=title_size)
            plt.savefig(f"{save_path}.png", dpi=300, bbox_inches='tight')

    plt.show()
    plt.close()
