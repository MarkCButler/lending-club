"""Functions used in generating clean data structures from raw data."""
from calendar import month_name

import pandas as pd

from notebook_tools import DATA_DIR

ACC_LOANS_PATH = DATA_DIR / "accepted_2007_to_2018Q4.csv"
REJ_LOANS_PATH = DATA_DIR / "rejected_2007_to_2018Q4.csv"
ACC_LOANS_METADATA_PATH = DATA_DIR / "accepted_loans_metadata.csv"

# Names of columns to exclude in loading the data
ACC_LOANS_EXCLUDED_COLUMNS = (
    "member_id",
    "url",
    "title",
    "desc",
    "policy_code",
    "hardship_type",
    "hardship_length",
    "deferral_term",
)

# Identifiers for data-conversion steps
ACC_LOANS_CONVERSIONS = ("time_intervals", "dates", "booleans")
REJ_LOANS_CONVERSIONS = ("percentages",)

# Names of columns in the raw data to convert from strings.
ACC_LOANS_DATE_COLUMNS = (
    "issue_d",
    "earliest_cr_line",
    "last_pymnt_d",
    "next_pymnt_d",
    "last_credit_pull_d",
    "sec_app_earliest_cr_line",
    "hardship_start_date",
    "hardship_end_date",
    "payment_plan_start_date",
    "debt_settlement_flag_date",
    "settlement_date",
)
ACC_LOANS_BOOLEAN_COLUMNS = ("pymnt_plan", "hardship_flag", "debt_settlement_flag")

# The data types to use in loading the table of rejected loans.
REJ_LOANS_DTYPES = {
    "Amount Requested": "Float64",
    "Application Date": "string",
    "Loan Title": "string",
    "Risk_Score": "Float64",
    "Debt-To-Income Ratio": "string",
    "Zip Code": "string",
    "State": "string",
    "Employment Length": "string",
    "Policy Code": "string",
}


def load_acc_loan_data(excluded_cols=ACC_LOANS_EXCLUDED_COLUMNS):
    """Load the table of accepted loans from a file of raw data.

    This function also executes data-cleaning steps developed in
    notebooks in the current project.

    Returns:
        Dataframe containing the table of accepted loans
    """
    metadata = load_acc_loan_metadata()
    dtypes = metadata["data type"].to_dict()

    return pd.read_csv(
        ACC_LOANS_PATH,
        dtype=dtypes,
        usecols=lambda col_name: col_name not in excluded_cols,
    )


def load_acc_loan_feat_desc():
    """Load a table of feature descriptions for data on accepted loans.

    Returns:
        Dataframe with index corresponding to feature names for the data on accepted
        loans.  The dataframe contains a single column named 'description'.
    """
    metadata = load_acc_loan_metadata()
    return metadata[["description"]]


def load_acc_loan_metadata():
    """Load a table o metadata on accepted loans.

    Returns:
        Dataframe with index 'column name' and columns 'data type', 'category',
        'known at loan origination', and 'description'.
    """
    metadata = pd.read_csv(ACC_LOANS_METADATA_PATH)
    return metadata.set_index("column name")


def load_rej_loan_data():
    """Load the table of rejected loans from a file of raw data.

    This function also executes data-cleaning steps developed in
    notebooks in the current project.

    Returns:
        Dataframe containing the table of rejected loans
    """
    # The comment to ignore type checking on the next line is needed because the type
    # hint for the dtype argument of read_csv doesn't match the functionality.
    return pd.read_csv(REJ_LOANS_PATH, dtype=REJ_LOANS_DTYPES)  # type: ignore


def filter_acc_loan_data(data):
    """Filter rows from the data on accepted loans.

    The filtering reproduces what is done in the ../notebooks/data-cleaning-02.ipynb.

    Args:
        data:  Dataframe containing table of accepted loans

    Returns:
        Dataframe with unwanted rows filtered out
    """
    bool_index = (
        data["loan_status"].notna()
        & (~data["loan_status"].str.startswith("Does not meet"))
        & (data["issue_d"] >= "2012-01")
    )
    int_rate_is_anomalous = (data["grade"] != "A") & (data["int_rate"] < 7)
    int_rate_is_anomalous = int_rate_is_anomalous | (
        (data["grade"] == "D") & (data["int_rate"] < 9)
    )
    bool_index = bool_index & (~int_rate_is_anomalous)
    return data[bool_index]


def convert_acc_loan_data(data, conversions=ACC_LOANS_CONVERSIONS):
    """Perform data conversion on selected columns in the table of accepted loans.

    Args:
        data:  Dataframe containing table of accepted loans
        conversions:  Tuple of strings specifying data-conversion steps to execute

    Returns:
        Dataframe with converted columns containing the table of accepted loans
    """
    if "time_intervals" in conversions:
        data.loc[:, "term"] = (
            data["term"].str.replace("months", "").str.strip().astype("Int64")
        )
    if "dates" in conversions:
        for col_name in ACC_LOANS_DATE_COLUMNS:
            data.loc[:, col_name] = (
                data[col_name]
                .map(_get_iso_date_string, na_action="ignore")
                .astype("string")
            )
    if "booleans" in conversions:
        mapper = {"N": False, "Y": True}
        for col_name in ACC_LOANS_BOOLEAN_COLUMNS:
            data.loc[:, col_name] = (
                data[col_name]
                .str.upper()
                .map(mapper, na_action="ignore")
                .astype("boolean")
            )
    return data


def convert_rej_loan_data(data, conversions=REJ_LOANS_CONVERSIONS):
    """Perform data conversion on selected columns in the table of rejected loans.

    Args:
        data:  Dataframe containing table of rejected loans
        conversions:  Tuple of strings specifying data-conversion steps to execute

    Returns:
        Dataframe with converted columns containing the table of rejected loans
    """
    if "percentages" in conversions:
        data.loc[:, "Debt-To-Income Ratio"] = (
            data["Debt-To-Income Ratio"].str.replace("%", "").astype("Float64")
        )
    return data


def _get_iso_date_string(element):
    """Convert a date string to ISO format.

    For example, 'Jun-2015' is converted to '2015-06'.

    Args:
        element:  String containing a date in the format used in the raw data, e.g.,
            Jun-2015.
    """
    iso_month_labels = define_month_conversions()
    month, year = element.lower().split("-")
    return year + "-" + iso_month_labels[month]


def define_month_conversions():
    """Return a dictionary used in converting month names to ISO format labels."""
    # The array of capitalized month names in chronological order provided by the
    # calendar module has the empty string as the first element, which is discarded.
    ordered_months = list(month_name)[1:]

    # Dictionary used in converting abbreviated month names to month numbers in ISO
    # format.
    return {
        month.lower()[:3]: format(index + 1, "02")
        for index, month in enumerate(ordered_months)
    }


def get_loan_metadata(loan_data, feature_descriptions=None):
    """Generate a dataframe of metadata describing loan data.

    Args:
        loan_data:  Dataframe containing data on accepted or rejected loans
        feature_descriptions:  Dataframe with a column 'description' that gives a
            description of each feature in loan_data.  The column names in loan_data
            should be in the index of feature_descriptions.

    Returns:
        Dataframe containing columns 'data type' and (if feature_descriptions is not
        None) 'description'.  The index is named 'column name' and contains the column
        names of loan_data.
    """
    metadata = loan_data.dtypes.map(str).to_frame(name="data type")
    if feature_descriptions is not None:
        metadata = metadata.join(feature_descriptions[["description"]])
    metadata.index.rename("column name", inplace=True)
    return metadata
