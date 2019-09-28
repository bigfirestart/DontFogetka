import json


def isInRange(range: str, temp: int):
    max = int(range.split()[0])
    min = int(range.split()[1])
    if temp >= min and temp <= max:
        return 1
    else:
        return 0


Seasons = {0: "winter", 1: "spring", 2: "summer", 3: "fall", 4: "winter"}


def build(list):
    # TODO ищет месяц
    city = list["destination_point"]
    month = int(int(list["arrival_date"].split(".")[1]) / 3)
    month = Seasons[month]
    # TODO смотрит компанию
    males_count = 0
    females_count = 0
    adults = 0
    for el in list["people"]["tourists"]:
        if not el["adult"]:
            adults = adults + 1
        if el["sex"] == "male":
            males_count = males_count + 1
        if el["sex"] == "female":
            females_count = females_count + 1

    # TODO смотрит погоду в данном регионе по месяцу
    weather_list = json.loads(open("templates/Weather.json", 'r').read())
    for el in weather_list:
        if el == city:
            weather = int(weather_list[el][month])
    # TODO подбирает вещи
    clothes_list = json.loads(open("templates/Clothes.json", 'r').read())
    final_list = json.loads(open("templates/EmptyPrediction.json", 'r').read())
    for el in clothes_list:
        if isInRange(clothes_list[el]["temp"], weather):
            if clothes_list[el]["sex"] == '':
                name = el
                count = males_count + females_count
            if clothes_list[el]["sex"] == 'M' and males_count > 0:
                name = el
                count = males_count
            if clothes_list[el]["sex"] == 'F' and females_count > 0:
                name = el
                count = females_count
            final_list["clothes"][clothes_list[el]["type"]].append({"name": name, "count": count})
    # TODO добавляем активити
    activity_list = json.loads(open("templates/Activities.json", 'r').read())
    name = ""
    for actv_name in list["travel_type"]:
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
    final_list["source"] = list
    return final_list
