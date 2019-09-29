import json
import datetime
import ad
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
def get_tourists_by_sex(tourists , sex):
    tourists_selection = []
    for tourist in tourists:
        if tourist["sex"] == sex:
            tourists_selection.append(tourist)
    return tourists_selection


def add_clothes(tourists, available, **kwargs):
    result = {}
    temperature = kwargs["temperature"]
    males_count = kwargs["males_count"]
    females_count = kwargs["females_count"]
    travel_duration = kwargs["travel_duration"]

    for item in available:
        if is_in_temperature_range(available[item]["temp"], temperature):
            tourists_count = get_count_by_sex(available[item]["sex"], **kwargs)
            if tourists_count > 0:
                if not result.get(available[item]["type"]):
                    result[available[item]["type"]] = []
                for tourist in tourists:
                    items_count =  int(travel_duration/3) + 1
                    result[available[item]["type"]].append({"name": item + " " + tourist["name"], "count": items_count})
    return result


def add_activities(activity, available, **kwargs):
    males_count = kwargs["males_count"]
    females_count = kwargs["females_count"]
    result = []
    for item in available:
        if available[item]["type"] == activity:
            count = get_count_by_sex(available[item]["sex"], **kwargs)
            result.append({"name": item, "count": count})
    return result
def get_travel_duration(travel_start_date , travel_end_date):
    tsd = travel_start_date.split(".")
    ted = travel_end_date.split(".")
    date1 = datetime.date(int(tsd[2]) ,int(tsd[1]),int(tsd[0]) )
    date2 = datetime.date(int(ted[2]), int(ted[1]), int(ted[0]))
    travel_duration = (date2-date1).days
    return travel_duration


def build(request):
    # TODO ищет месяц
    city = request["destination_point"]

    # TODO смотрим колличество дней
    travel_duration = get_travel_duration(request["arrival_date"] , request["return_date"])

    # 12.12.2109
    month = get_season_by_month(int(request["arrival_date"].split(".")[1]))
    # TODO смотрит компанию
    males_count = 0
    females_count = 0
    children = 0
    for tourist in request["people"]["tourists"]:
        if not tourist["adult"]:
            children += 1
        if tourist["sex"] == "M":
            males_count += 1
        elif tourist["sex"] == "F":
            females_count += 1

    # TODO смотрит погоду в данном регионе по месяцу
    weather_list = json.load(open("templates/Weather.json"))
    temperature = weather_list[city][month]

    # TODO подбирает вещи
    clothes_list = json.load(open("templates/Clothes.json"))
    result = json.load(open("templates/EmptyList.json"))

    result["clothes"].update(
        add_clothes(
            request["people"]["tourists"],
            clothes_list,
            temperature=temperature,
            males_count=males_count,
            females_count=females_count,
            travel_duration=travel_duration
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
    result["hygiene/cosmetics"].append({"name": "Мочалка", "count": males_count + females_count})
    result["hygiene/cosmetics"].append({"name": "Косметичка", "count": females_count})

    # TODO добавляем рекламу
    result["ad"] = ad.build(request["travel_type"])

    # TODO добавляем погоду
    result["advices"]["info"] = {"temperature": temperature}
    result["source"] = request

    # TODO добавляем варнинги
    warnings_list = json.loads(open("templates/Warnings.json", 'r').read())
    sity = request["destination_point"]

    for warning in warnings_list:
        if sity in warnings_list[warning]["cities"]:
            result["advices"]["recommended"].append(warning)


    return result


if __name__ == '__main__':
    req = json.loads(open("samples/Request.json", 'r').read())
    pprint(build(req))
