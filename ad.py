import json
def get_simular_by_two_lists(list1 , list2):
    simular = []
    for el1 in list1:
        for el2 in list2:
            if el1==el2:
                simular.append(el1)
    return simular

def build(categories):
    ads = json.loads(open("templates/Ad.json", 'r').read())
    ads_list = []
    for ad in ads:
        if len(get_simular_by_two_lists(ads[ad]["category"], categories))>0:
            ads_list.append(ad)
    return ads_list


if __name__ == '__main__':
    req = json.loads(open("samples/Request.json", 'r').read())
    print(build(req["travel_type"]))