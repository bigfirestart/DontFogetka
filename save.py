from trello import TrelloClient
import config

client = TrelloClient(
    api_key=config.TRELLO_API_KEY,
    token=config.TRELLO_API_SECRET
)
def save(list):
    name = "Поездка 13.08 London"
    board = client.add_board(name)
    cols = board.list_lists()
    for col in cols:
        col.close()

    current_lst = board.add_list("Советы")
    params = list["advices"]["recommended"]
    for el in params:
        current_lst.add_card(el)

    current_lst = board.add_list("Косметика/Гигиена")
    params = list["hygiene/cosmetics"]
    for el in params:
        current_lst.add_card(el)

    board.add_list("Лекарства")
    params = list["medicines"]
    for el in params:
        current_lst.add_card(el)

    current_lst = board.add_list("Электроника")
    params = list["electronics"]
    for el in params:
        current_lst.add_card(el)

    current_lst =board.add_list("Аксессуары")
    params = list["accessories"]
    for el in params:
        current_lst.add_card(el)

    current_lst =board.add_list("Дополнительная одежда")
    params = list["clothes"]["additional"]
    for el in params:
        current_lst.add_card(el)

    current_lst =board.add_list("Обувь")
    params = list["clothes"]["shoes"]
    for el in params:
        current_lst.add_card(el)

    current_lst =board.add_list("Повседневная одежда")
    params = list["clothes"]["daily"]
    for el in params:
        current_lst.add_card(el)

    current_lst =board.add_list("Верхняя одежда")
    params = list["clothes"]["outerwear"]
    for el in params:
        current_lst.add_card(el)








    return "Ok"