import json

import pyowm

import config


class Predictor:

    def __init__(self, data):
        self.data = data
        self.predictions = json.load(open("predictions.json"))

    def _get_by_weather(self):
        pass

    def _get_by_climate(self):
        pass

    def _get_by_country(self):
        pass

    def predict(self):
        pass



if __name__ == '__main__':
    predict({})
