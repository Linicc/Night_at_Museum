from sklearn.ensemble import RandomForestRegressor
import numpy as np

class RiskModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100)
        
    def train(self, features, labels):
        # features: List of environment features (e.g. dist to exit, width)
        # labels: Risk score (e.g. max density observed)
        self.model.fit(features, labels)
        
    def predict(self, features):
        return self.model.predict(features)
