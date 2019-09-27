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
    advises = list["advices"]["recommended"]
    for advice in advises:
        current_lst.add_card(advice)

    board.add_list("Косметика/Гигиена")
    advises = list["hygiene/cosmetics"]
    for advice in advises:
        current_lst.add_card(advice)

    board.add_list("Лекарства")
    advises = list["medicines"]

    board.add_list("Электроника")
    advises = list["electronnics"]
    for advice in advises:
        current_lst.add_card(advice)

    board.add_list("Аксессуары")
    advises = list["hygiene/cosmetics"]
    for advice in advises:
        current_lst.add_card(advice)


    board.add_list("Дополнительная одежда")
    board.add_list("Обувь")
    board.add_list("Повседневная одежда")
    board.add_list("Верхняя одежда")








    return "Ok"