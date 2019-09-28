import json
from pprint import pprint


def is_in_range(temperature_range: str, temperature: int):
    max_temp = int(temperature_range.split()[0])
    min_temp = int(temperature_range.split()[1])
    if min_temp <= temperature <= max_temp:
        return True
    else:
        return False


def get_season_by_month(month: int):
    if month == 12 or month <= 2:
        return "winter"
    elif 3 <= month <= 5:
        return "spring"
    elif 6 <= month <= 8:
        return "summer"
    elif 9 <= month <= 11:
        return "fall"
    else:
        raise ValueError


def build(request):
    # TODO ищет месяц
    city = request["destination_point"]
    month = int(int(request["arrival_date"].split(".")[1]) / 3)
    month = get_season_by_month(month)
    # TODO смотрит компанию
    males_count = 0
    females_count = 0
    adults = 0
    for tourist in request["people"]["tourists"]:
        if not tourist["adult"]:
            adults = adults + 1
        if tourist["sex"] == "male":
            males_count = males_count + 1
        if tourist["sex"] == "female":
            females_count = females_count + 1

    # TODO смотрит погоду в данном регионе по месяцу
    weather_list = json.load(open("templates/Weather.json"))
    for tourist in weather_list:
        if tourist == city:
            weather = int(weather_list[tourist][month])

    # TODO подбирает вещи
    clothes_list = json.loads(open("templates/Clothes.json", 'r').read())
    final_list = json.loads(open("templates/EmptyPrediction.json", 'r').read())
    for tourist in clothes_list:
        if is_in_range(clothes_list[tourist]["temp"], weather):
            if clothes_list[tourist]["sex"] == '':
                name = tourist
                count = males_count + females_count
            if clothes_list[tourist]["sex"] == 'M' and males_count > 0:
                name = tourist
                count = males_count
            if clothes_list[tourist]["sex"] == 'F' and females_count > 0:
                name = tourist
                count = females_count
            final_list["clothes"][clothes_list[tourist]["type"]].append({"name": name, "count": count})
    # TODO добавляем активити
    activity_list = json.loads(open("templates/Activities.json", 'r').read())
    name = ""
    for actv_name in request["travel_type"]:
        for actv in activity_list:
            if activity_list[actv]["type"] == actv_name:
                if activity_list[actv]["sex"] == '':
                    name = actv
                    count = males_count + females_count
                if activity_list[actv]["sex"] == 'M' and males_count > 0:
                    name = actv
                    count = males_count
                if activity_list[actv]["sex"] == 'F' and females_count > 0:
                    name = actv
                    count = females_count
                final_list["activities"].append({"name": name, "count": count})
    # TODO добавляем гигиену костылём
    final_list["hygiene/cosmetics"].append({"name": "Зубная щётка", "count": males_count + females_count})
    final_list["hygiene/cosmetics"].append({"name": "Зубная паста", "count": 1})
    final_list["hygiene/cosmetics"].append(
        {"name": "Гель для душа", "count": int(males_count > 0) + int(females_count > 0)})
    final_list["hygiene/cosmetics"].append({"name": "Шампунь", "count": int(males_count > 0) + int(females_count > 0)})
    final_list["hygiene/cosmetics"].append({"name": "Мачалка", "count": males_count + females_count})
    final_list["hygiene/cosmetics"].append({"name": "Косметичка", "count": females_count})

    # TODO добавляем погоду
    final_list["advices"]["info"] = {"temperature": weather}
    final_list["source"] = request
    return final_list


if __name__ == '__main__':
    req = {
        "departure_point": "Moscow",
        "destination_point": "Zurich",
        "arrival_date": "23.12.2019",
        "return_date": "01.10.2019",
        "travel_type": ["sking", "work"],
        "people": {
            "count": 3,
            "tourists": [
                {
                    "sex": "male",
                    "adult": True
                },
                {
                    "sex": "female",
                    "adult": True
                },
                {
                    "sex": "male",
                    "adult": False
                }
            ]
        }
    }
    pprint(build(req))
