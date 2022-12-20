import datetime
from unittest import TestCase, main
import doctest
import PrintOrCreate


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(PrintOrCreate))
    return tests


class Tests(TestCase):

    def test_translate(self):
        self.assertEqual(PrintOrCreate.InputConnect.translate(['name', 'key_skills', 'premium']),
                         ['Название', 'Навыки', 'Премиум-вакансия'])
        self.assertEqual(PrintOrCreate.InputConnect.translate(['BYR', 'EUR', 'GEL']),
                         ['Белорусские рубли', 'Евро', 'Грузинский лари'])
        self.assertEqual(PrintOrCreate.InputConnect.translate(['between1And3', 'between3And6', 'moreThan6']),
                         ['От 1 года до 3 лет', 'От 3 до 6 лет', 'Более 6 лет'])

    def test_coorect_sortparam(self):
        self.assertEqual(PrintOrCreate.InputConnect.check_sortparam(['Оклад', 'Да']), True)
        self.assertEqual(PrintOrCreate.InputConnect.check_sortparam(['Оклад', '']), True)
        self.assertEqual(PrintOrCreate.InputConnect.check_sortparam(['Прогромист', '']), False)

    def test_coorect_filterparam(self):
        self.assertEqual(PrintOrCreate.InputConnect.check_paramtrs('Опыт работы: От 3 до 6 лет '), True)
        self.assertEqual(PrintOrCreate.InputConnect.check_paramtrs('Навыки: CSS'), True)
        self.assertEqual(PrintOrCreate.InputConnect.check_paramtrs('Навыки CSS'), False)


if __name__ == "__main__":
    main()
