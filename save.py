from trello import *
import config

client = TrelloClient(
    api_key=config.TRELLO_API_KEY,
    token=config.TRELLO_API_SECRET
)


def trello_save_list(card, save_list):
    items_list = []
    for item in save_list:
        for item_iter in range(item["count"]):
            if item["count"] == 1:
                items_list.append(item["name"])
            else:
                items_list.append(item["name"] + " " + str(item_iter + 1))
    card.add_checklist(card.name, items_list)


def trello_add_other(request, other_list):
    activity_card = other_list.add_card("Активности")
    activities_list = []
    for i in range(len(request["activities"])):
        request["activities"][i]["name"] =request["activities"][i]["name"]  +" x"+ str(request["activities"][i]["count"])
        request["activities"][i]["count"] = 1
    trello_save_list(activity_card, request["activities"])

    med_card = other_list.add_card("Лекарства")
    trello_save_list(med_card, request["medicines"])

    cosm_card = other_list.add_card("Косметика/Гигиена")
    trello_save_list(cosm_card, request["hygiene/cosmetics"])


def trello_add_clothes(request, clothes_list):
    under_card = clothes_list.add_card("Верхняя одежда")
    trello_save_list(under_card, request["clothes"]["outerwear"])

    daily_card = clothes_list.add_card("Повседневная одежда")
    trello_save_list(daily_card, request["clothes"]["daily"])

    shoes_card = clothes_list.add_card("Обувь")
    trello_save_list(shoes_card, request["clothes"]["shoes"])

    additional_card = clothes_list.add_card("Дополнительная одежда")
    trello_save_list(additional_card, request["clothes"]["additional"])


def save(request):
    name = "Поездка " + request["source"]["arrival_date"] + " " + request["source"]["destination_point"]

    all_boards = client.list_boards()
    for brd in all_boards:
        if brd.name == name:
            board = brd
            print("Board with name: " + name + " found")
            break
    else:
        print("Creating board with name: " + name)
        board = client.add_board(name)

    cols = board.list_lists()
    for col in cols:
        col.close()

    ad_list = board.add_list("Акции и предложения")
    req_ad = request["ad"]
    for ad in req_ad:
        ad_list.add_card(ad)

    special_list = board.add_list("Информация")
    for label in board.get_labels():
        if label.color == 'green':
            green_label = label
        if label.color == 'red':
            red_label = label
        if label.color == 'yellow':
            yellow_label = label
    req_info = request["advices"]["info"]

    for inf in req_info:
        special_list.add_card("Ожидаемая температура: " + str(req_info["temperature"]), labels=[yellow_label])
    req_not_rec = request["advices"]["not_recommended"]
    for not_rec in req_not_rec:
        special_list.add_card(not_rec, labels=[red_label])
    req_rec = request["advices"]["recommended"]
    for rec in req_rec:
        special_list.add_card(rec, labels=[green_label])

    other_list = board.add_list("Другое")
    trello_add_other(request, other_list)

    clothes_list = board.add_list("Одежда")
    trello_add_clothes(request, clothes_list)
