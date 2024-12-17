"""Predifined sklearn pipeline to process and create features with financial data"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs-dev/02_pipelines.ipynb.

# %% auto 0
__all__ = ['MyBaseTransformer', 'ReturnTransformer', 'StdTransformer', 'MATransformer', 'EMATransformer', 'simplify_colnames']

# %% ../nbs-dev/02_pipelines.ipynb 4
import re

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# %% ../nbs-dev/02_pipelines.ipynb 7
class MyBaseTransformer(BaseEstimator, TransformerMixin):
    """Base class for my custom transformers"""
    def __init__(self):
        self.input_features_ = None
        self.output_features_ = None
        self.postfix = "transformed"

    def fit(self, X, y=None):
        if hasattr(X, 'columns'):
            self.input_features_ = X.columns.tolist()
        else:
            self.input_features_ = [f'f_{i}' for i in range(X.shape[1])]
        self.output_features_ = [f"{feat}_{self.postfix}" for feat in self.input_features_]
        return self

    def transform(self, X) -> np.ndarray:
        X = X.copy()
        return X.values

    def get_feature_names_out(self, input_features=None) -> list[str]|None:
        if input_features is not None:
            return [f"{feat}_{self.postfix}" for feat in input_features]
        else:
            return self.output_features_

# %% ../nbs-dev/02_pipelines.ipynb 10
class ReturnTransformer(MyBaseTransformer):
    """Evaluate the percentage return over 1 or more periods"""
    def __init__(self, periods:int=1) -> None:
        super().__init__()
        self.postfix = "ret"
        self.periods = periods

    def transform(self, X) -> np.ndarray:
        """percentage change with previous bar, fist bar is 0"""
        X = X.copy()
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        return X.pct_change(periods=self.periods).fillna(0.0).values

# %% ../nbs-dev/02_pipelines.ipynb 12
class StdTransformer(MyBaseTransformer):
    """Evaluate the standard deviation over a window"""
    def __init__(self, window:int=5) -> None:
        super().__init__()
        self.window = window
        self.postfix = f"std{self.window}"

    def transform(self, X) -> np.ndarray:
        X = X.copy()
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        return X.rolling(window=self.window, min_periods=1).std().values

# %% ../nbs-dev/02_pipelines.ipynb 14
class MATransformer(MyBaseTransformer):
    """Evaluate the moving average over a window"""
    def __init__(self, window:int=5) -> None:
        super().__init__()
        self.window = window
        self.postfix = f"MA{window}"

    def transform(self, X) -> np.ndarray:
        X = X.copy()
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        return X.rolling(window=self.window, min_periods=1).mean().values

# %% ../nbs-dev/02_pipelines.ipynb 15
class EMATransformer(MyBaseTransformer):
    """Evaluate the exponential moving average over a window"""
    def __init__(self, window:int=5) -> None:
        super().__init__()
        self.window = window
        self.postfix = f"EMA{window}"

    def transform(self, X) -> np.ndarray:
        X = X.copy()
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        return X.ewm(span=self.window).mean().values

# %% ../nbs-dev/02_pipelines.ipynb 18
def simplify_colnames(cols)->list[str]:
    """Simplify the columns names by removing the prefix"""
    pat = re.compile(r"[\w\d\-]*_{2}(?P<end>\w*)")
    cols = [pat.match(c).group('end') for c in cols]
    return cols
