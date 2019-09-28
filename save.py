from trello import *
import config

client = TrelloClient(
    api_key=config.TRELLO_API_KEY,
    token=config.TRELLO_API_SECRET
)


def save(list):
    name = "Поездка " + list["source"]["arrival_date"] + " " + list["source"]["destination_point"]

    # board = client.add_board(name)
    # TODO закоментить перед показом
    all_boards = client.list_boards()
    for brd in all_boards:
        if brd.name == name:
            board = brd

    cols = board.list_lists()
    for col in cols:
        col.close()

    # TODO Информация
    current_lst = board.add_list("Информация")

    for label in board.get_labels():
        if label.color == 'green':
            green_label = label
        if label.color == 'red':
            red_label = label
        if label.color == 'yellow':
            yellow_label = label
    params = list["advices"]["info"]
    for el in params:
        current_lst.add_card("Ожидаемая температура: " + str(params["temperature"]), labels=[yellow_label])
    params = list["advices"]["not_recommended"]
    for el in params:
        current_lst.add_card(el, labels=[red_label])
    params = list["advices"]["recommended"]
    for el in params:
        card = current_lst.add_card(el, labels=[green_label])

    # TODO Другое
    current_lst = board.add_list("Другое")

    current_card = current_lst.add_card("Активности")
    params = list["activities"]
    items = []
    for el in params:
        for iter in range(el["count"]):
            items.append(el["name"] + " " + str(iter + 1))
    current_card.add_checklist("Аксессуары", items)

    current_card = current_lst.add_card("Лекарства")
    params = list["medicines"]
    items = []
    for el in params:
        for iter in range(el["count"]):
            items.append(el["name"] + " " + str(iter + 1))
    current_card.add_checklist("Лекарства", items)

    current_card = current_lst.add_card("Косметика/Гигиена")
    params = list["hygiene/cosmetics"]
    items = []
    for el in params:
        for iter in range(el["count"]):
            items.append(el["name"] + " " + str(iter + 1))
    current_card.add_checklist("Косметика/Гигиена", items)

    # TODO Одежда
    current_lst = board.add_list("Одежда")

    current_card = current_lst.add_card("Верхняя одежда")
    params = list["clothes"]["outerwear"]
    items = []
    for el in params:
        for iter in range(el["count"]):
            items.append(el["name"] + " " + str(iter + 1))
    current_card.add_checklist("Верхняя одежда", items)

    current_card = current_lst.add_card("Повседневная одежда")
    params = list["clothes"]["daily"]
    items = []
    for iter in range(el["count"]):
        items.append(el["name"] + " " + str(iter + 1))
    current_card.add_checklist("Повседневная одежда", items)

    current_card = current_lst.add_card("Обувь")
    params = list["clothes"]["shoes"]
    items = []
    for iter in range(el["count"]):
        items.append(el["name"] + " " + str(iter + 1))
    current_card.add_checklist("Обувь", items)

    current_card = current_lst.add_card("Дополнительная одежда")
    params = list["clothes"]["additional"]
    items = []
    for iter in range(el["count"]):
        items.append(el["name"] + " " + str(iter + 1))
    current_card.add_checklist("Дополнительная одежда", items)
