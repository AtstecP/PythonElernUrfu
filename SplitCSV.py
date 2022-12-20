import csv
import os


class SplitCSV:
    def __init__(self, name):
        self.name = name
        self.split_data = {}

    def filling_dict(self, row, heading):
        x = 5
        year = row[len(row) - 1][:4]
        if not self.split_data.__contains__(year):
            self.split_data[year] = [heading, row]
        else:
            self.split_data[year].append(row)

    def split_by_year(self):
        if os.stat(self.name).st_size == 0:
            return []
        flag = True
        counter = 0
        directory_path = 'F:\Makarov\Spilt_csv'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        with open(self.name, encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            heading = next(reader)
            for row in reader:
                for piece in row:
                    if len(piece) == 0:
                        flag = False
                    counter += 1
                if flag and (len(heading) == counter):
                    self.filling_dict(row, heading)
                flag = True
                counter = 0
        self.creating_files()

    def creating_files(self):
        for key in self.split_data.keys():
            with open(f"F:/Makarov/Spilt_csv/{key}.csv", "w", newline="", encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerows(self.split_data[key])


def main():
    split = SplitCSV('vacancies_by_year.csv')
    split.split_by_year()


if __name__ == "__main__":
    main()
