import sqlite3
import jinja2

conn = sqlite3.connect('dane/db.sqlite3')
c = conn.cursor()

# funckcja generujaca pliki powiatów dla danego okręgu
def generuj_powiaty(wojewodztwo, okreg):
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "/home/marcin/PycharmProjects/aplikacjewww1/powiaty/powiat.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    # print("jestem w funkcji generuj okregi dla wojewodztwa", okreg)

    lista_powiatow= []
    for row in c.execute("SELECT subareas FROM main_commune WHERE area='" + str(okreg).upper() + "'"):
        lista_powiatow.append(row)

    for powiat in lista_powiatow:
        # print("    jestem w powiecie nr", powiat[0])

        # wyniki kazdego kandydata dla danego powiatu:
        wyniki = [] # wyniki poszczególnych kandydatów w danym okregu, alfabetycznie
        procenty = [] # procent głosów oddanych na kandydata w danym okregu, alfabetycznie
        for row in c.execute("select "
                             "sum(grabowski), "
                             "sum(ikonowicz), "
                             "sum(kalinowski),"
                             "sum(korwin),"
                             "sum(krzaklewski),"
                             "sum(kwasniewski),"
                             "sum(lepper),"
                             "sum(lopuszanski),"
                             "sum(olechowski),"
                             "sum(pawlowski),"
                             "sum(walesa),"
                             "sum(wilecki)"
                             " from main_commune where subareas = " + str(powiat[0]) + " group by subareas"):
            suma = sum(row)
            for result in row:
                wyniki.append(result)
                procenty.append(str(round(result/suma, 4) * 100)[:4]) # magia aby wyświetlało się w stylu 23.45% w html

            # stworz liste gmin nalezacych do danego powiatu
            gminy = []
            for row in c.execute("SELECT DISTINCT name FROM main_commune WHERE subareas='" + str(powiat[0]) + "' AND area='" + str(okreg).upper() + "' AND county='" + str(wojewodztwo).upper() + "'"):
                gminy.append(row[0])
            print("wygenerowalem liste gmin dla powiatu",powiat, ":", gminy)
            templateVars = {"wojewodztwo": wojewodztwo, "okreg": okreg, "powiat" : powiat[0], "wyniki" : wyniki, "procenty" : procenty, "gminy" : gminy }

            with open("powiaty/powiat" + str(powiat[0]) + ".html", "w") as fh:
                outputText = template.render( templateVars )
                fh.write(outputText)

# funkcja generujaca pliki okregow dla danego wojewodztwa
def generuj_okregi(wojewodztwo):
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "/home/marcin/PycharmProjects/aplikacjewww1/okregi/okreg.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    print("jestem w funkcji generuj okregi dla wojewodztwa", wojewodztwo)

    lista_okregow = []
    for row in c.execute("SELECT DISTINCT area FROM main_commune WHERE county='" + str(wojewodztwo).upper() + "'"):
        lista_okregow.append(row)

    for okreg in lista_okregow:
        print("    jestem w okregu nr", okreg[0])

        # wyniki kazdego kandydata dla danego okregu:
        wyniki = [] # wyniki poszczególnych kandydatów w danym okregu, alfabetycznie
        procenty = [] # procent głosów oddanych na kandydata w danym okregu, alfabetycznie
        for row in c.execute("select "
                             "sum(grabowski), "
                             "sum(ikonowicz), "
                             "sum(kalinowski),"
                             "sum(korwin),"
                             "sum(krzaklewski),"
                             "sum(kwasniewski),"
                             "sum(lepper),"
                             "sum(lopuszanski),"
                             "sum(olechowski),"
                             "sum(pawlowski),"
                             "sum(walesa),"
                             "sum(wilecki)"
                             " from main_commune where county='" + str(wojewodztwo).upper() + "'and area = " + str(okreg[0]) + " group by area"):
            suma = sum(row)
            for result in row:
                wyniki.append(result)
                procenty.append(str(round(result/suma, 4) * 100)[:4]) # magia aby wyświetlało się w stylu 23.45% w html

            # stworz liste powiatów nalezacych do danego okregu
            powiaty = []
            for row in c.execute("SELECT DISTINCT subareas FROM main_commune WHERE county='" + str(wojewodztwo).upper() + "' and area='" + str(okreg[0]) + "'"):
                powiaty.append(row[0])
            print("wygenerowalem liste powiatów dla okregu",okreg[0], ":", powiaty)
            templateVars = {"wojewodztwo": wojewodztwo, "okreg": okreg[0], "wyniki" : wyniki, "procenty" : procenty, "powiaty" : powiaty }

            with open("okregi/okreg" + str(okreg[0]) + ".html", "w") as fh:
                outputText = template.render( templateVars )
                fh.write(outputText)

            generuj_powiaty(wojewodztwo, okreg[0])



def generuj_wojewodztwa():
    wojewodztwa = []

    for row in c.execute("SELECT DISTINCT county FROM main_commune"):
        wojewodztwa.append(str(row[0]).lower())

    print(wojewodztwa)

    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "/home/marcin/PycharmProjects/aplikacjewww1/wojewodztwa/wojewodztwo.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    # generujemy pliki z templejta wojewodztwo.html dla poszczegolnych województw
    for wojewodztwo in wojewodztwa:

        # wyniki kazdego kandydata dla danego wojewodztwa:
        wyniki = [] # wyniki poszczególnych kandydatów w danym województwie, alfabetycznie
        procenty = [] # procent głosów oddanych na kandydata w danym województwie, alfabetycznie
        for row in c.execute("select "
                             "sum(grabowski), "
                             "sum(ikonowicz), "
                             "sum(kalinowski),"
                             "sum(korwin),"
                             "sum(krzaklewski),"
                             "sum(kwasniewski),"
                             "sum(lepper),"
                             "sum(lopuszanski),"
                             "sum(olechowski),"
                             "sum(pawlowski),"
                             "sum(walesa),"
                             "sum(wilecki)"
                             " from main_commune where county='" + str(wojewodztwo).upper() + "' group by county"):

            suma = sum(row)
            for result in row:
                wyniki.append(result)
                procenty.append(str(round(result/suma, 4) * 100)[:4]) # magia aby wyświetlało się w stylu 23.45% w html

        # stworz liste okregow nalezacych do danego wojewodztwa
        okregi = []
        for row in c.execute("SELECT DISTINCT area FROM main_commune WHERE county='" + str(wojewodztwo).upper() + "'"):
            okregi.append(row[0])

        templateVars = {"wojewodztwo": wojewodztwo, "wyniki": wyniki, "procenty": procenty, "okregi": okregi}

        with open("wojewodztwa/" + str(wojewodztwo) + ".html", "w") as fh:
            outputText = template.render( templateVars )
            fh.write(outputText)

        generuj_okregi(wojewodztwo)




generuj_wojewodztwa()
