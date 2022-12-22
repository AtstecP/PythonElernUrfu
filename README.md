# Основной файл это PrintOrCreate.py
 
## Тесты

![image](https://user-images.githubusercontent.com/109477937/208450012-f6eaf8c5-08ee-4062-931e-2e6287b78523.png)
## Оптимизация
![img_1.png](screenshots/img_1.png)

#### Проверял скорость методов через тесты
![img.png](screenshots/test_parser_time.png)
#### Но они оказальст мало эфективными
#### Gровел тесты через основной код
#### strip = 63.91 сек
#### простое заполнение = 49.32 сек
#### isoparse = 64.43 сек
#### ciso8601 = 39.46 сек
#### Буду использовать библиотеку ciso8601
### Заметил, что regex работают медлено
![img.png](screenshots/sub_stat.png)
#### заменил на собсвенный метод
### Итоговое время 19.24 сек

## Спилит CSV по годам 
#### SplitCSV.py
![img.png](screenshots/split_csv.png)

## Multiprocessing 
### Сделал 10 испытаний с замерами и построил график
#### Без многопроцессорной обработки - 10.26 сек
#### Multiprocessing - 7.82 сек
![img_1.png](screenshots/multi_plot.png) ![img.png](screenshots/multi_stat.png)