import logging
import string
from collections.abc import Iterable
from typing import Dict, List, Optional

from pycurl import PASSWORD

"""
№ 1 Реализовать класс MultiTempAttributes, который позволяет временно изменять значения атрибутов объекта.
Этот класс должен поддерживать контекстный менеджер, который изменяет указанные атрибуты объекта на новые значения,
а после завершения работы с объектом автоматически восстанавливает исходные значения атрибутов.

Класс MultiTempAttributes должен реализовывать следующие методы:

__init__(self, obj, attrs_values): Конструктор, принимающий два аргумента:

obj: Объект, атрибуты которого будут временно изменяться.
attrs_values: Словарь, где ключи — это имена атрибутов, которые нужно изменить, а значения — новые значения для этих атрибутов.
__enter__(self): Метод, который сохраняет исходные значения указанных атрибутов и устанавливает новые значения.

__exit__(self, exc_type, exc_value, traceback): Метод, который восстанавливает исходные значения атрибутов после выхода из контекстного менеджера, независимо от того, произошла ли ошибка.
"""


# Контекстный менеджер
class MultiTempAttributes:
    def __init__(self, obj, attrs_values):
        self.__to_save = dict()
        self.__to_load = attrs_values
        self.__target = obj

    def __enter__(self):
        for pair in self.__to_load.items():
            self.__to_save[pair[0]] = getattr(self.__target, pair[0])
            setattr(self.__target, pair[0], pair[1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        for pair in self.__to_save.items():
            setattr(self.__target, pair[0], pair[1])


"""
№ 2 Подсчет уникальных слов

Вам дан текст в виде строки, содержащий слова и пунктуацию.
Напишите функцию, которая определяет количество уникальных слов в этом тексте. Для подсчета уникальных слов следует учитывать следующие условия:

Текст должен быть приведен к нижнему регистру, чтобы слова с разными регистрами считались одинаковыми.
Все знаки пунктуации должны быть удалены из текста.
После удаления пунктуации текст следует разбить на слова, разделенные пробелами.
Слово считается уникальным, если оно встречается в тексте только один раз после удаления пунктуации и приведения текста к нижнему регистру.
"""


def count_unique_words(text: str) -> int:
    text = text.lower()
    for i in range(len(text)-1, -1, -1):
        if text[i] in ",.?!:;&":
            text = text[0:i] + text[i+1:]
    text = text.split()
    if len(text) > 0:
        all_words = [text[0]]
        counts = [0]

        for cur_word in text:
            flag = True
            for i in range(0, len(all_words)):
                if all_words[i] == cur_word:
                    counts[i] = counts[i] + 1
                    flag = False
                    break
            if flag:
                all_words.append(cur_word)
                counts.append(1)
        if type(counts.count(1)) == type(None):
            return 0
        else:
            return len(counts)
    return 0



"""
№ 3 Анализ четных чисел

Аргументы:
numbers: Список целых чисел.


Возвращаемое значение:
Словарь с ключами:
"count": Количество четных чисел.
"sum": Сумма четных чисел (или None, если четных чисел нет).
"average": Среднее значение четных чисел (или None, если четных чисел нет).
"max": Максимальное значение четных чисел (или None, если четных чисел нет).
"min": Минимальное значение четных чисел (или None, если четных чисел нет).
"""


def analyze_even_numbers(numbers: List[int]) -> Dict[str, Optional[float]]:
    count = 0
    sum = 0
    max = 0
    min = 0
    flag = True
    for num in numbers:
        if num % 2 == 0:
            count = count + 1
            sum = sum + num
            if flag:
                max = num
                min = num
                flag = False
            if max < num:
                max = num
            elif min > num:
                min = num

    if count == 0:
        return({"count":count, "sum": None, "average": None, "max": None, "min": None})
    else:
        return ({"count": count, "sum": sum, "average": sum/count, "max": max, "min": min})

"""
№ 4 Проверка уникальности элементов в вложенных структурах данных

Реализовать функцию all_unique_elements, которая проверяет,
содержатся ли в заданной структуре данных только уникальные элементы.

Поддерживаются следующие типы данных:
Строки
Списки
Кортежи
Множества
Вложенные структуры (например, списки внутри списков и т.д.)
Функция должна игнорировать значения типа None.
"""


def all_unique_elements(data) -> bool:
    def flatten(d):
        """Вспомогательная функция для рекурсивного разворачивания вложенных структур.
            Возвратит строку
            При раскрытии коллекции пишет, что это за коллекция в возвращаемую строку.
        """
        result = ""
        for item in d:

            if type(d) == dict:
                result = result + str(type(dict)) + str(item)
                if type(item) == str or type(item) == int:
                    result = result + str(item)
                elif item is not None:
                    result = result + str(type(item)) + flatten(item)

            elif type(item) == str or type(item) == int:
                result = result + str(item)

            elif item is not None:
                result = result + str(type(item)) + flatten(item)
        return(result)

    previous = []

    if type(data) == set:
        return True

    for a in data:
        if type(a) != type(None):
            for b in previous:
                if type(a) == type(b):
                    if type(a) == int or type(a) == float:
                        if int(a) == int(b):
                            return False
                    elif len(a) == len(b):
                        if type(a) == str:
                            if a == b:
                                return False
                        else:
                            if flatten(a) == flatten(b):
                               return False
                elif int(a) == int(b):
                    return False
            previous.append(a)


    return True



"""
№ 5 

Напишите функцию enumerate_list,
которая принимает на вход список data и возвращает новый список,
содержащий элементы из data, но каждый элемент дополнен его индексом.
Индекс каждого элемента рассчитывается начиная с start и увеличивается на step для каждого следующего элемента.

Функция должна поддерживать следующие параметры:

data (list): список, элементы которого нужно перечислить.
start (int, по умолчанию 0): начальный индекс.
step (int, по умолчанию 1): шаг, на который увеличивается индекс.
recursive (bool, по умолчанию False): если True, функция должна рекурсивно обрабатывать вложенные списки.
Функция должна возвращать список, в котором каждый элемент является кортежем из двух элементов: индекса и значения из исходного списка.
"""


def enumerate_list(
        data: list, start: int = 0, step: int = 1, recursive: bool = False
) -> list:
    def recursive_enumerate(lst, idx):
        result = []
        for item in lst:
            if type(item) == str:
                result.append((idx, item))
                idx = idx + 1
            else:
                idx = idx + 1
                result.append((idx - 1, recursive_enumerate(item, idx)))
        return result

    new_data = []
    for item in data:
        # Обрабатываем список рекурсивно
        if recursive and type(item) != str:
            start = start + 1
            new_data.append((start - 1, recursive_enumerate(item, start)))

        # Обрабатываем строку, или НЕ обрабатываем список рекурсивно
        else:
            new_data.append((start, item))
            start = start + step
    return new_data





"""
№ 6 Реализация контекстного менеджера для подключения к базе данных (симуляция)

Вам необходимо реализовать класс DatabaseConnection,
который будет управлять подключением к базе данных и транзакциями(симуляция в виде сообщений),
используя менеджер контекста. Класс должен поддерживать следующие функции:

Инициализация: При создании экземпляра класса, он должен принимать имя базы данных (db_name), к которой будет подключаться.

Менеджер контекста: Класс должен реализовывать методы __enter__ и __exit__, чтобы использовать его в блоке with. 
При входе в блок контекста должно происходить подключение к базе данных, а при выходе из блока — закрытие соединения и обработка возможных ошибок.

Подключение к базе данных: Метод connect должен инициировать подключение к базе данных и сохранять его состояние.

Выполнение запроса: Метод execute_query должен выполнять запрос, если активна транзакция. В противном случае должен выбрасываться исключение.

Управление транзакциями: Методы start_transaction, commit и rollback должны управлять транзакциями. Транзакция должна быть активна для выполнения запросов, и должна быть закрыта после коммита или отката.

Логирование: Класс должен использовать встроенный модуль logging для записи логов подключения, выполнения запросов, начала и завершения транзакций, а также для обработки ошибок.
"""

# Настройка логирования для примера
logging.basicConfig(level=logging.INFO)


class DatabaseConnection:

    def __init__(self, db_name):
        self.connection = None
        self.transaction_active = False
        self.__name = db_name

    def __enter__(self):
        self.connect()
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transaction_active = False
        self.connection = None
        #close + errors
        pass
    def connect(self):
        self.connection = "Connected to " + self.__name + " database"

    def execute_query(self, query):
        if self.transaction_active:
            return "Result of \'" + query + "\'"
        else:
            raise RuntimeError("No active transaction")



    def start_transaction(self):
        self.transaction_active = True
    def commit(self):
        if self.transaction_active:
            self.transaction_active = False
        else:
            raise RuntimeError("No active transaction to commit")
