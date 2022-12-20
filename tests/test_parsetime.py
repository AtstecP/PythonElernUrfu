import datetime
from unittest import TestCase, main
import PrintOrCreate


class Tests(TestCase):

    def test_formate_time(self):
        x = '2022-07-14T11:06:59+0300'
        x_date = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
        for i in range(1_000_00):
            self.assertEqual(PrintOrCreate.DataSet.format_time(x), x_date)

    def test_formate_time1(self):
        x = '2022-07-14T11:06:59+0300'
        x_date = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
        for i in range(1_000_000):
            self.assertEqual(PrintOrCreate.DataSet.format_time1(x), x_date)

    def test_formate_time2(self):
        x = '2022-07-14T11:06:59+0300'
        x_date = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
        for i in range(1_000_000):
            self.assertEqual(PrintOrCreate.DataSet.format_time2(x), x_date)

    def test_formate_time3(self):
        x = '2022-07-14T11:06:59+0300'
        x_date = datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z')
        for i in range(1_000_000):
            self.assertEqual(PrintOrCreate.DataSet.format_time3(x), x_date)


if __name__ == "__main__":
    main()
