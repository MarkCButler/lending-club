"""Functions used in generating derived features."""
import numpy as np
import pandas as pd


def get_profit(data, total_payment, principal):
    """Generate a series representing profit as a percentage of principal.

    Args:
        data:  Dataframe containing the columns represented by parameters
            'total_payment' and 'principal'
        total_payment:  Name of a column representing the total of all payments made on
            the loan
        principal:  Name of a column representing the loan principal

    Returns:
        Series giving the profit as a percentage of the principal
    """
    return (data[total_payment] - data[principal]) / data[principal]


def get_duration(data, start, end):
    """Generate a series representing duration in months.

    Args:
        data:  Dataframe containing the columns represented by parameters 'start' and
            'end'
        start:  Name of a column containing the start date as a year-month combination
            in ISO format, e.g., 2015-01
        end:  Name of a column containing the end date as a year-month combination in
            ISO format

    Returns:
        Series giving the number of months between the start date and end date as a
        nullable integer (Int64)
    """

    def to_period(ser):
        return pd.to_datetime(ser, format="ISO8601").dt.to_period(freq="M")

    # We are not looking for the exact difference (in days) between dates; instead, we
    # want the number of months between two "dates" that represent month-long time
    # spans, e.g., the number of months between 2015-12 and 2016-06. Convert each date
    # column to a pd.Period object and take the difference to get offsets corresponding
    # to a number of months.
    duration = to_period(data[end]) - to_period(data[start])
    # To extract the integer number of months in the offset, use the 'n' attribute.
    duration = duration.apply(lambda value: np.nan if pd.isna(value) else value.n)
    return duration.astype("Int64")


def get_annualized_return(data, profit, duration):
    """Generate a series representing the creditor's annualized return.

    Args:
        data:  Dataframe containing the columns represented by parameters 'profit' and
            'duration'
        profit:  Name of a column representing the profit as a percentage of principal
        duration:  Name of a column representing the loan duration in months

    Returns:
        Series representing the creditor's annualized return.
    """
    # The dataset includes loans with a duration of zero months that show a profit as
    # large as 4%. In the absence of detailed information about how interest is charged
    # for loans of duration of less than a month, annualized returns are calculated as
    # if these loans had a duration of 1 month.
    number_of_months = data[duration].apply(lambda val: val if val >= 1 else 1)
    return (1 + data[profit]) ** (12 / number_of_months) - 1


def get_year(data, date):
    """Extract the year from a year-month combination in ISO format.

    Args:
        data:  Dataframe containing the column represented by parameter 'date'
        date:  Name of a column of dates expressed as year-month combinations in ISO
            format, e.g., 2015-01
    """
    return data[date].str[:4]
