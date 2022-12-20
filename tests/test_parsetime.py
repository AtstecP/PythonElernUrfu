import datetime
from unittest import TestCase, main
import PrintOrCreate


class Tests(TestCase):

    def test_formatetime(self):
        x = {'published_at': '2022-07-14T11:06:59+0300'}
        x_date = datetime.datetime.strptime(x['published_at'], '%Y-%m-%dT%H:%M:%S%z')
        for i in range(1_000_00):
            self.assertEqual(PrintOrCreate.DataSet.format_time(x), x_date)

    def test_formatetime1(self):
        x = {'published_at': '2022-07-14T11:06:59+0300'}
        x_date = datetime.datetime.strptime(x['published_at'], '%Y-%m-%dT%H:%M:%S%z')
        for i in range(1_000_000):
            self.assertEqual(PrintOrCreate.DataSet.format_time1(x), x_date)

    def test_formatetime2(self):
        x = {'published_at': '2022-07-14T11:06:59+0300'}
        x_date = datetime.datetime.strptime(x['published_at'], '%Y-%m-%dT%H:%M:%S%z')
        for i in range(1_000_000):
            self.assertEqual(PrintOrCreate.DataSet.format_time2(x), x_date)

    def test_formatetime3(self):
        x = {'published_at': '2022-07-14T11:06:59+0300'}
        x_date = datetime.datetime.strptime(x['published_at'], '%Y-%m-%dT%H:%M:%S%z')
        for i in range(1_000_000):
            self.assertEqual(PrintOrCreate.DataSet.format_time3(x), x_date)


if __name__ == "__main__":
    main()
