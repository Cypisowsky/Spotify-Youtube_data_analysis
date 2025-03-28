from analysis import *
from visualizations import *

def main():
    # Load the data
    data = load_data("Spotify_Youtube.csv")

    if data is None:
        return

    # Filter the data
    filtered_data = filter_data(data)

    # Parse into numeric and categorical
    numeric_columns, categorical_columns = parse_data(filtered_data)

    # Basic descriptive stats
    numeric_stats, categorical_stats = basic_desc_data(numeric_columns, categorical_columns)

    # Save results
    save_to_csv(numeric_stats=numeric_stats, categorical_stats=categorical_stats)

    # Create visualizations
    create_boxplot(numeric_columns)
    create_violinplot(numeric_columns)
    plot_errorbars_from_df(numeric_columns, numeric_columns.columns)
    histograms_from_df(data, numeric_columns.columns)

    # Correlations finding
    cond_histograms_from_df(data, ["Views", "Stream"], "official_video")
    heatmap_from_df(data, "Valence", "Key")
    heatmap_from_df(data, "Danceability", "Speechiness")
    heatmap_from_df(data, "Danceability", "Speechiness", "Stream")
    heatmap_from_df(data, "Licensed", "Album_type", "Stream")
    heatmap_from_df(data, "Licensed", "Album_type", "Views")
    regplot_from_df(data, "Views", "Likes")
    regplot_from_df(data, "Likes", "Comments", 2, 0)

    # PSA dimensionality reduction
    reduced_data = PCA_reduce(scale_data(numeric_columns))
    save_to_csv(reduced_data=reduced_data)


if __name__ == "__main__":
    main()