from __future__ import division

from sklearn.linear_model import Ridge
import numpy as np


def train_model(x_observations, y_observations):

    model = Ridge(alpha=10**0)
    model.fit(np.array(x_observations), np.array(y_observations))
    
    return model


def predict(model, xs):
    return model.predict(xs)

