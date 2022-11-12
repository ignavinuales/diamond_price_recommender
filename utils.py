import pickle
import numpy as np
import pandas as pd
from scipy.stats import boxcox
from scipy.special import inv_boxcox

class Pipeline():
    def __init__(self, features: dict) -> None:
        self.weight = features['weight']
        self.length = features['length']
        self.width = features['width']
        self.depth = features['depth']
        self.quality = features['quality']
        self.color = features['color']
        self.clarity = features['clarity']

    def data_pipeline(self):
        # Apply boxcox transformation to weight
        lamba_weight_boxcox = -0.0950413870690428  # lambda value from boxcox
        weight = boxcox(self.weight, lamba_weight_boxcox)

        # Apply log transformation to length, width, depth
        length = np.log1p(self.length)
        width = np.log1p(self.width)
        depth = np.log1p(self.depth)

        # Ordinal encoding
        with open('pickle_files/ordinal_encoder.pkl', 'rb') as file:
            ord_encoder = pickle.load(file)  # Load ordinal_encoder
            file.close()
        
        encoded_data = ord_encoder.transform([[self.quality, self.color, self.clarity]]).ravel()
        quality, color, clarity = encoded_data[0], encoded_data[1], encoded_data[2]
        
        # Create dataframe with transformed features
        data = {
            'weight': weight,
            'length': length,
            'width': width,
            'depth': depth,
            'quality': quality,
            'color': color,
            'clarity': clarity
        }
        
        df = pd.DataFrame(data, index=[0])

        return df

    def get_model(self):
        with open('pickle_files/catboost_diamonds_model.pkl', 'rb') as files:
            model = pickle.load(files)

        return model

    def make_prediction(self):
        # Get catboos model
        model = self.get_model()
        # Get input data
        data = self.data_pipeline()
        # Make prediction
        prediction = model.predict(data.iloc[0])
        # Scale back with inverse boxcox
        lambda_price = -0.06711272583112812
        price = inv_boxcox(prediction, lambda_price)
        
        return price
