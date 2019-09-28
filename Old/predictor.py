import json

import pyowm
import pycountry

import config


class Predictor:

    def __init__(self, data):
        self.data = data
        self.owm = pyowm.OWM(config.OWM_API_KEY)
        self.predictions = json.load(open("predictions.json"))

    @staticmethod
    def _add_item(result, item):
        if item['type'] == 'clothes':
            if item['item'] not in result['clothes'][item['subtype']]:
                result['clothes'][item['subtype']].append(item['item'])

        elif item['item'] not in result[item['type']]:
            result[item['type']].append(item['item'])

    def _get_by_weather(self):
        result = []
        place = self.data['destination_point']
        weather = self.owm.weather_at_place(place)

    def _get_by_reason(self):
        pass

    def _get_by_country(self):
        pass

    def predict(self):
        pass


if __name__ == '__main__':
    Predictor({}).predict()
