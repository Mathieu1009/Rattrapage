import unittest
import json
import re


def get_json():
    with open('parlez_vous_nombre.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def decoupe(nombre):
    words = []
    word = ""
    for i, lettre in enumerate(nombre):
        if lettre == " " or lettre == "-":
            words.append(word)
            word = ""
        else:
            word += lettre
        if i+1 == len(nombre):
            words.append(word)
    return words


def convert_words_nombre(words):
    nombre = []
    a = 0
    for word in words:
        found = False
        d = data['mot-arabe']
        for index in range(len(d)):
            find = re.findall(d[index]['autochtone'], word)
            if find:
                found = True
                nombre.append(d[index]['arabe'])
                if len(str(d[index]['arabe'])) > 6 and a == 0:
                    a = 0
                    nombre.append('+')
                elif len(str(d[index]['arabe'])) > 3 and a != 0:
                    nombre.pop(a-1)
                    a = 0
                    nombre.append('+')
                elif len(str(d[index]['arabe'])) > 2 and a == 0:
                    nombre.append('+')
                    a = len(nombre)
        if found == False:
            return word
    return nombre


def cas_special(f, s):
    '''
    Gère les cas des 80-24-21...
    '''
    if s == 20:
        return f*s
    else:
        return f+s


def separe(nombre):
    tab = []
    result = []
    j = 0
    for i in nombre:
        if i != '+':
            tab.append(i)
        elif i == '+' and j != 0:
            result.append(tab)
            tab = []
            j = 0
        j += 1
    result.append(tab)
    return result


def convert_total(nombres):
    end = 0
    result = 0
    for tab in nombres:
        try:
            while len(tab) > 0:
                first = tab.pop(0)
                sec = tab.pop(0)
                try:
                    n = tab.pop(0)
                    if n == 20:
                        sec *= n
                    else:
                        tab.insert(0, n)
                except:
                    pass
                if len(str(first)) > 2 and len(str(sec)) < 3:
                    result = first + sec
                elif len(str(sec)) > 2:
                    result = first * sec
                else:
                    result = cas_special(first, sec)
                tab.insert(0, result)
        except:
            end += first
    return end


def formate(nombre):
    str_nb = str(nombre)[::-1]
    nb = ""
    for i in range(len(str_nb)):
        nb += str_nb[i]
        if i % 3 == 2:
            nb += " "
    return nb[::-1]


def romain(nombre):
    result = 0
    d = data['romain-arabe']
    for i in range(len(d)):
        result += nombre.count(d[i]['autochtone']) * d[i]['arabe']
    return result


def check_lg(text):
    try:
        if len(re.findall(r'^[MDCLXVI]*$', text)[0]):
            return 0
    except:
        return 1


def main(text):
    if check_lg(text):
        a = decoupe(text)
        b = convert_words_nombre(a)
        if type(b) is str:
            print(
                "Erreur de frappe : '{}' n'est pas compris, veuillez réécrire votre nombre".format(b))
            return 'Error'
        else:
            c = separe(b)
            end = convert_total(c)
    else:
        end = romain(text)
    format_end = formate(end)
    print("{} = {}".format(text, format_end))
    return format_end


class TestNombre(unittest.TestCase):

    def test_1(self):
        self.assertIn(main(
            "huit milliard trois cent million neuf cent quatre vingt douze mille trois cent trois"), ' 8 300 992 303')

    def test_2(self):
        self.assertIn(
            main("quatre Cents Cinquante trois mille neuf cent septante neuf"), " 453 979")

    def test_3(self):
        self.assertIn(main("deux mille sept cent neuf"), " 2 709")

    def test_4(self):
        self.assertIn(main(
            "sept cent sept million sept cent soixante dix sept mille sept"), " 707 777 007")

    def test_5(self):
        self.assertIn(main("Trois mille deux cent un"), " 3 201")

    def test_6(self):
        self.assertIn(main("mil quatre cent"), " 1 400")

    def test_7(self):
        self.assertIn(
            main("quatre-vingt-douze milles huit cent deux"), " 92 802")

    def test_8(self):
        self.assertIn(main(
            "neuf milliards cinq cent soixante et onze millions neuf cent quatre milles vingt trois"), " 9 571 904 023")

    def test_9(self):
        self.assertIn(
            main("Mille deux cent nonante sept"), " 1 297")

    def test_10(self):
        self.assertIn(
            main("MMMMCMLVII"), " 4 957")

    def test_11(self):
        self.assertIn(
            main("sept-cent-mille-trois-cent-vingt-et-un"), " 700 321")

    def test_12(self):
        self.assertIn(
            main("trente-deux millions deux-cent-vingt-trois"), " 32 000 223")

    def test_13(self):
        self.assertIn(
            main("mil neuf cents"), " 1 900")

    def test_14(self):
        self.assertIn(
            main("quatre-vingt-dix-neuf billions neuf cent quatre-vingt-dix-neuf milliards neuf cent quatre-vingt-dix-neuf millions neuf cent quatre-vingt-dix-neuf mille neuf cent quatre-vingt-dix-neuf"), " 99 999 999 999 999")

    def test_15(self):
        self.assertIn(
            main("sept cent soixante-dix-sept billions sept cent soixante-dix-sept milliards sept cent soixante-dix-sept millions sept cent soixante-dix-sept mille sept cent soixante-dix-sept"), " 777 777 777 777 777")

    def test_16(self):
        self.assertIn(
            main("six cent soixante-six billions six cent soixante-six milliards six cent soixante-six millions six cent soixante-six mille six cent soixante-six"), " 666 666 666 666 666")

    def test_17(self):
        self.assertIn(
            main("trois cent trente-trois billions trois cent trente-trois milliards trois cent trente-trois millions trois cent trente-trois mille trois cent trente-trois"), " 333 333 333 333 333")

    def test_18(self):
        self.assertIn(
            main("cent onze billions cent onze milliards cent onze millions cent onze mille cent onze"), " 111 111 111 111 111")

    def test_19(self):
        self.assertIn(
            main("cent vingt-trois millions quatre cent cinquante-six mille sept cent quatre-vingt-neuf"), " 123 456 789")

    def test_20(self):
        self.assertIn(
            main("qutre"), "Error")


if __name__ == '__main__':
    data = get_json()

    text_input = input('Insérez un nombre écrit en toutes lettres :')
    m = main(text_input)
    while m == "Error":
        m = main(input('Insérez un nombre écrit en toutes lettres :'))

    # Test
    # unittest.main()
