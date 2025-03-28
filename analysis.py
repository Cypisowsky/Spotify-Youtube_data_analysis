import pandas as pd
import numpy as np
import os

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def load_data(filepath):
    """
    Loads a CSV file into a pandas DataFrame.

    :param filepath: Path to the CSV file.
    :return: DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(filepath)
        print("Data loaded successfully.")
        return data
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def filter_data(data):
    """
    Filters out unnecessary columns like descriptions and URLs.

    :param data: Original DataFrame.
    :return: Filtered DataFrame with selected columns.
    """
    columns_to_exclude = [col for col in data.columns if col == 'Unnamed: 0' or col.lower() == 'uri' or 'url_' in col.lower() or 'description' in col.lower() or col == '']
    f_data = data[data.columns.difference(columns_to_exclude)]
    return f_data


def parse_data(data):
    """
    Parse data function.

    :param data: Data to be parsed.
    :return: Parsed data.
    """
    # for numerical data
    numeric_columns = data.select_dtypes(include=['number'])

    # for categorical data
    categorical_columns = data.select_dtypes(include=['object'])

    return numeric_columns, categorical_columns


def basic_desc_data(numeric_columns, categorical_columns):
    """
    Basic description data function.

    :param numeric_columns: numeric data
    :param categorical_columns: categorical data
    :return: Describe return value
    """
    # numerical data
    numeric_stats = numeric_columns.describe(
        percentiles=[0.05, 0.95])  # we use additional parameters to include different percentiles
    numeric_stats.loc['missing_values'] = numeric_columns.isnull().sum()  # we sum nulls as well

    # categorical data
    categorical_stats = pd.DataFrame(
        {  # crating DataFrame containing number of unique classes and number of missing values
            'unique_classes': categorical_columns.nunique(),
            'missing_values': categorical_columns.isnull().sum()
        })
    categorical_stats['proportion'] = None

    # adding proportion to every class
    for col in categorical_columns:
        categorical_stats.at[col, 'proportion'] = categorical_columns[col].value_counts(normalize=True,
                                                                                        dropna=True).to_dict()

    return numeric_stats, categorical_stats

def save_to_csv(**kwargs):
    """
    Save to csv function.

    :param kwargs: Data to be saved.
    :return: Nothing.
    """
    os.makedirs('processed_data', exist_ok=True)
    for var_name, data in kwargs.items():
        if isinstance(data, pd.DataFrame):
            filename = f"processed_data/{var_name}.csv"
            data.to_csv(filename, index=False)
            print(f"Saved: {filename}")
        else:
            print(f"Denied {var_name} — is not DataFrame.")


def scale_data(numeric_data):
    df_clean = numeric_data.dropna() # eliminate every "blank" field
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_clean) # scaling to avoid measuring problems (like different units
    return scaled_data

def PCA_reduce(scaled_data):
    """
        Reduce PCA dimensionality.

        :param scaled_data: Scaled data
        :return: Reduced data
        """
    pca = PCA(n_components=2)  # choosing to transform to 2D
    pca_result = pca.fit_transform(scaled_data)  # transforming

    df_pca = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

    return df_pca
