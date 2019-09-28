import json
from pprint import pprint


def is_in_temperature_range(temperature_range: str, temperature: int):
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


def get_count_by_sex(sex, **kwargs):
    count = 0
    if sex == '':
        count = kwargs["males_count"] + kwargs["females_count"]
    elif sex == 'M':
        count = kwargs["males_count"]
    elif sex == 'F':
        count = kwargs["females_count"]
    return count


def add_clothes(tourists, available, **kwargs):
    result = []
    temperature = kwargs["temperature"]
    males_count = kwargs["males_count"]
    females_count = kwargs["females_count"]
    for item in available:
        if is_in_temperature_range(available[item]["temp"], temperature):
            count = get_count_by_sex(available[item]["sex"], **kwargs)
            if count > 0:
                result[available[item]["type"]].append({"name": item, "count": count})
    return result


def add_activities(activity, available, **kwargs):
    males_count = kwargs["males_count"]
    females_count = kwargs["females_count"]
    result = []
    for item in available:
        if available[item] == activity:
            count = get_count_by_sex(available[item]["sex"], **kwargs)
            result.append({"name": item, "count": count})


def build(request):
    # TODO ищет месяц
    city = request["destination_point"]
    # 12.12.2109
    month = get_season_by_month(int(request["arrival_date"].split(".")[1]))
    # TODO смотрит компанию
    males_count = 0
    females_count = 0
    children = 0
    for tourist in request["people"]["tourists"]:
        if not tourist["adult"]:
            children += 1
        if tourist["sex"] == "male":
            males_count += 1
        elif tourist["sex"] == "female":
            females_count += 1

    # TODO смотрит погоду в данном регионе по месяцу
    weather_list = json.load(open("templates/Weather.json"))
    temperature = weather_list[request["destination_point"]][month]

    # TODO подбирает вещи
    clothes_list = json.load(open("templates/Clothes.json"))
    result = json.load(open("templates/EmptyPrediction.json"))

    result["clothes"].update(
        add_clothes(
            request["people"]["tourists"],
            clothes_list,
            temperature=temperature,
            males_count=males_count,
            females_count=females_count
        )
    )

    # TODO добавляем активити
    activity_list = json.loads(open("templates/Activities.json", 'r').read())
    for travel_activity in request["travel_type"]:
        result["activities"] += add_activities(
            travel_activity, activity_list,
            males_count=males_count,
            females_count=females_count
        )

    # TODO добавляем гигиену костылём
    result["hygiene/cosmetics"].append({"name": "Зубная щётка", "count": males_count + females_count})
    result["hygiene/cosmetics"].append({"name": "Зубная паста", "count": 1})
    result["hygiene/cosmetics"].append(
        {"name": "Гель для душа", "count": int(males_count > 0) + int(females_count > 0)})
    result["hygiene/cosmetics"].append({"name": "Шампунь", "count": int(males_count > 0) + int(females_count > 0)})
    result["hygiene/cosmetics"].append({"name": "Мачалка", "count": males_count + females_count})
    result["hygiene/cosmetics"].append({"name": "Косметичка", "count": females_count})

    # TODO добавляем погоду
    result["advices"]["info"] = {"temperature": weather}
    result["source"] = request
    return result


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
