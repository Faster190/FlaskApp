Анализатор прайс-листов.
========================


### Логика программы:
В папке находятся несколько файлов, содержащих прайс-листы от разных поставщиков.
Количество и название файлов заранее неизвестно, однако точно известно, что в названии файлов прайс-листов есть слово "price".
Файлы, не содержащие слово "price" игнорируются.
Формат файлов: данные, разделенные запятой.
Порядок колонок в файле заранее неизвестен, но известно, что столбец с названием товара называется одним из вариантов: "название", "продукт", "товар", "наименование".
Столбец с ценой может называться "цена" или "розница".
Столбец с весом имеет название "фасовка", "масса" или "вес" и всегда указывается в килограммах.
Остальные столбцы игнорируются.

### Описание работы программы и взаимодействие с пользователем:
Программа загружает данные из всех прайс-листов и предоставляет интерфейс для поиска товара по фрагменту названия с сорторовкой по цене за килогорамм.
Интерфейс для поиска реализован через консоль, циклически получая информацию от пользователя.
Если введено слово "exit", то цикл обмена с пользователем завершается, программа выводит сообщение о том, что работа закончена и завершает свою работу. В противном случае введенный текст считается текстом для поиска. Программа выводит список найденных позиций в виде таблицы:

№   Наименование               цена вес   файл   цена за кг.<br>
1   филе гигантского кальмара         617  1 price_0.csv 617.0<br>
2   филе гигантского кальмара         639  1 price_4.csv 639.0<br>
3   филе гигантского кальмара         639  1 price_6.csv 639.0<br>
4   филе гигантского кальмара         683  1 price_1.csv 683.0<br>
5   филе гигантского кальмара         1381  2 price_5.csv 690.5<br>
6   кальмар тушка                   3420  3 price_3.csv 1140.0<br>
7   кальмар тушка                   4756  4 price_0.csv 1189.0<br>

Список будет отсортирован по возрастанию стоимости за килограмм.

Предусмотрен вывод массива данных в текстовый файл в формате html.

_________________________

* ### Как запустить?
Запускаем файл "project.py". По умолчанию ищет файлы в месте расположения самого проекта. 

* ### Как поменять директорию поиска файлов?
Можно поменять директорию поиска, указав путь в качестве параметра при вызове функции load_prices() объекта pm.

* ### Как производить сортировку по другому столбцу?
В теле метода класса load_prices, а точнее в его конце, при вызове метода "self._search_product_price_weight()" в качестве параметра передать строку-название необходимого столбца.

_________________________________
### Скриншоты работы программы: