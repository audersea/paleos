from loguru import logger
import pandas as pd

def drop_any_duplicated(series: pd.Series) -> pd.Series:
    """Drop any duplicated indices

    Args:
        series (pd.Series): pandas series

    Returns:
        pd.Series: Updated pandas series with any duplicated index removed
    """
    logger.info("Dropping all duplicated indices")
    return series[~series.index.duplicated(keep=False)]


def keep_first_duplicated(series: pd.Series) -> pd.Series:
    """Keep the first encountered duplicated index

    Args:
        series (pd.Series): pandas series

    Returns:
        pd.Series: Updated pandas series keeping the first duplicated index
    """
    logger.info("Keeping first duplicated index")
    return series[~series.index.duplicated(keep="first")]


def average_duplicated(series: pd.Series) -> pd.Series:
    """Average out ages for duplicated indices

    Args:
        series (pd.Series): pandas series

    Returns:
        pd.Series: Updated pandas series with ages averaged out for any duplicated indices
    """
    logger.info("Averaging values for duplicated indices")
    return series.groupby(series.index).mean()