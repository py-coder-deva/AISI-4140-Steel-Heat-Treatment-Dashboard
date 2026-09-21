import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin


class TemperingParameterTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, C=20):
        self.C = C

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()

        # Tempering parameter
        X["tempering_parameter"] = (
            (X["tempering_temp_C"] + 273.15)
            * (
                self.C
                + np.log10(X["tempering_time_hr"])
            )
        )

        return X


class YSTemperingParameterTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, C=20):
        self.C = C

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        X = X.copy()

        # Tempering parameter
        X["tempering_parameter"] = (
            (X["tempering_temp_C"] + 273.15)
            * (
                self.C
                + np.log10(X["tempering_time_hr"])
            )
        )

        # Additional engineered feature for YS
        X["temperature_temp_time"] = (
            X["tempering_temp_C"]
            * X["tempering_time_hr"]
        )

        return X