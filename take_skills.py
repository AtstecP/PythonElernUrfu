import csv
import math
import re


def main():
    # input()
    data = read_file('vacancies_with_skills.csv')
    dataf = clean_data(data)
    skills_data = take_skills(dataf)
    print('data = {')
    for key in skills_data.keys():
        print(f'{key}: {skills_data[key]}', end=',\n')
    print('}')






def take_skills(main_data):
    data = []
    data_dict = {}

    for vacancy in main_data:
        for skill in vacancy['key_skills']:
            if not data_dict.__contains__(vacancy['published_at'][:4]):
                data_dict[vacancy['published_at'][:4]] = {skill: 1}
            else:
                if skill not in data_dict[vacancy['published_at'][:4]]:
                    data_dict[vacancy['published_at'][:4]][skill] = 1
                else:
                    data_dict[vacancy['published_at'][:4]][skill] += 1
    for skill in data_dict:
        data.append([skill, data_dict[skill]])
    for key in data_dict.keys():
        data_dict[key] = dict(sorted(data_dict[key].items(), key=lambda x: x[1], reverse=True)[:10])
    return data_dict





def read_file(name):
    flag = True
    counter = 0
    data = []
    with open(name, encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        heading = next(reader)
        data.append(heading)
        for row in reader:
            for piece in row:
                if len(piece) == 0:
                    flag = False
                counter += 1
            if flag and (len(heading) == counter):
                data.append(row)
            flag = True
            counter = 0
    return data




def clean_data(data):

    heading = data[0]
    chk_pat = '(?:{})'.format(
        '|'.join(['ios']))

    alfa = data
    alfa.pop(0)
    data_new = []

    for row in alfa:
        dict_new = {}
        for i in range(0, len(heading)):
            if heading[i] == 'key_skills':
                dict_new[heading[i]] = row[i].split("\n")
            else:
                row[i] = row[i].replace("\n", ", ")
                row[i] = row[i].strip()
                dict_new[heading[i]] = row[i]
        #print(f'{date} in {row[5][:4]}')

        if re.search(chk_pat, row[1].lower(), flags=re.I):
            data_new.append(dict_new)
    return data_new


if __name__ == "__main__":
    main()
