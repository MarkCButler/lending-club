"""Functions that facilitate generation / formatting of plots."""
from textwrap import wrap


def format_counts(tick_value, _tick_position):
    """Format y-axis tick labels that represent counts (e.g. for a histogram).

    Example:  Tick values 750e3, 1e6, 1.25e6 would be formatted as 750k, 1M, 1.25M.

    This function is meant to be used with matplotlib.ticker.FuncFormatter.

    Args:
        tick_value:  Tick value
        _tick_position:  Tick position

    Returns:
        Formatted tick label
    """
    tick_value = int(tick_value)
    if tick_value < 1_000:
        return str(tick_value)
    if tick_value < 1_000_000:
        divisor = 1_000
        unit = "k"
    else:
        divisor = 1_000_000
        unit = "M"
    if tick_value % divisor == 0:
        return format(tick_value // divisor, ",") + unit
    return format(tick_value / divisor, ".2f") + unit


def get_wrapped_caption(feature_name, feature_descriptions, width):
    """Generate a caption with predefined maximum width.

    Args:
        feature_name:  The feature name, corresponding to an index value in the
            dataframe feature_descriptions
        feature_descriptions:  Dataframe with index of feature names and a single column
            named 'description'.  The function load_acc_loan_feat_desc in the module
            notebook_tools.data_cleaning returns a dataframe of this form.
        width:  The maximum width of the caption (in characters).

    Returns:
        Caption containing the feature name and the feature description.  The caption
        text is wrapped so that the number of characters per line is <= width.
    """
    caption = f'{feature_name}: {feature_descriptions.loc[feature_name, "description"]}'
    return "\n".join(wrap(caption, width=width))
