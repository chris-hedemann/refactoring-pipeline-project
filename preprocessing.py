
from sklearn.base import BaseEstimator, TransformerMixin
from geopandas import ... 

class BathBedTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        ratio = X.bedrooms / X.bathrooms
        idx = X.index[(ratio >= 5. ) | (ratio < 0.5 )]
        X.drop(index=idx, inplace=True)
        return X


class BasementAreaTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        X.sqft_basement = X.sqft_living - X.sqft_above
        return X
    
class ModalImputer(BaseEstimator,TransformerMixin):
    def __init__(self,columns=['view','waterfront']):
        self._cols = columns
        self._modes = dict()
    
    def fit(self, X, y=None):
        for col in self._cols:
            self._modes[col] = X[col].mode().values[0]
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        for col in self._cols:
            X[col].fillna(self._modes[col], inplace=True)
        
        return X
    
class LastChangeTransformer(BaseEstimator,TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X = X.copy()
        mask = ( (kc_data_cleaned.yr_renovated.isna()) | 
                (kc_data_cleaned.yr_renovated==0)
        )
        new_col = kc_data_cleaned.yr_renovated.where(
            ~mask, 
            kc_data_cleaned.yr_built
            ).astype(int)
        X['last_known_change'] = new_col
        X.drop(['yr_renovated','yr_built'], axis=1, inplace=True)
        return X