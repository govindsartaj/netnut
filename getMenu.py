import requests
from datetime import date
from bs4 import BeautifulSoup

start_date = date(2020, 6, 2)
LUNCH = 319155
DINNER = 319183


class Menu:

    menu_items = []

    def __delta_date(self, query_date):
        delta = query_date - start_date
        return delta.days

    def __get_lunch_oid(self, query_date):
        return str(LUNCH + self.__delta_date(query_date))

    def __get_dinner_oid(self, query_date):
        return str(DINNER + self.__delta_date(query_date))

    def __build_url(self, query_date, course):
        if course == "L":
            return "https://nutrition.grinnell.edu/NetNutrition/1/Menu/SelectMenu?menuOid=" + self.__get_lunch_oid(
                query_date)
        elif course == "D":
            return "https://nutrition.grinnell.edu/NetNutrition/1/Menu/SelectMenu?menuOid=" + self.__get_dinner_oid(
                query_date)

    def __process_item_name(self, item):
        item_text = str(item.text)
        return item_text.split('(')[0].strip()

    def __populate_menu(self, response):
        response = response.json()
        page = BeautifulSoup(response['panels'][0]['html'], features="html.parser")
        stuff = page.select('table')[1].select('tr')
        for item in stuff:
            self.menu_items.append(self.__process_item_name(item))
        self.menu_items = self.menu_items[1:-1]

    def get_menu(self, query_date, course):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Basic Og==',
            'Cookie': 'CBORD.netnutrition2=NNexternalID=1; ASP.NET_SessionId=aow5eurmpcdkrgblv0gos5wr'
        }

        response = requests.request("POST", self.__build_url(query_date, course), headers=headers)
        self.__populate_menu(response)



def main():
    menu = Menu()
    menu.get_menu(date(2020, 6, 4), "L")
    print(menu.menu_items)


if __name__ == '__main__':
    main()