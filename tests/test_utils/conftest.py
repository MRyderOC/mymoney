import pytest
import numpy as np
import pandas as pd


@pytest.fixture
def dataframe_creator():
    return pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"],
        "col3": [True, True, False],
    })


@pytest.fixture
def superset_column():
    return ["col1", "col2", "col3", "col4", ]


@pytest.fixture
def subset_column():
    return ["col1", "col2", ]


@pytest.fixture
def equal_column():
    return ["col1", "col2", "col3", ]


@pytest.fixture
def series_int():
    return pd.Series(np.arange(3, 13))


@pytest.fixture
def series_string():
    return pd.Series(["a" * i for i in range(10)])


@pytest.fixture
def series_bool():
    return pd.Series([True, True, False, True, False] * 2)


@pytest.fixture
def series_float():
    return pd.Series(np.arange(.1, 1, .1))


@pytest.fixture
def series_complex():
    return pd.Series([complex(1, i) for i in range(10)])


@pytest.fixture
def series_datetime():
    return pd.Series(pd.date_range("2020-01-01", periods=10, freq="M"))


@pytest.fixture
def series_timedelta():
    return pd.Series([pd.Timedelta(days=i, hours=i) for i in range(10)])
