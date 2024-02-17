from datetime import date, datetime
from collections import UserDict, UserList
from time import sleep

# Создала два класса - Note и Notes (по аналогии с классами Record и AddressBook. Экземпляр класса Note будет добавляться в экземпляр класса Notes, как и Record добавлялся в AddressBook)
# Note - это словарь с 4мя ключами - "title", "tags", "text", "date"
# Notes - список, каждый элемент этого списка - это экземпляр класса Note. Иными словами, Notes - это список, состоящий из словарей.

# class Note. Значения по ключам "title", "tags", "text" по умолчанию принимают значение None. Значение по ключу "date" создается автоматически и равно текущему времени на момент создания

# Главное отличие в поведении экземпляров Note и Notes от Record и AddressBook - при создании экземпляра Note он автоматически добавляется в уже созданный экземпляр Notes,
# это реализовано в строке 34. Сам экземпляр класса Notes создан в строке 68, это переменная my_notes. 
# Внутри этого файла (notatki.py) автоматическое добавление работает, а если экспортировать классы в другой файл и создавать в нем экземпляры классов, то работать не будет. 
# Зато будет работать добавление одной записи (экземпляра Note) в экземпляр класса Notes вручную, то есть с помощью метода add_note класса Notes. 
# Это то самое проблемное место, по поводу которого я хотела задать вопрос Эдуарду. 
# АПДЕЙТ. Убираем пока что эту строку с автоматическим добавлением

# class Note содержит методы для добавления заголовка, тэгов и текста. Метод добавления текста сделан так, что можно добавлять текст к уже существующему тексту, то есть как бы 
# дописывать заметку. Тэги тоже можно добавлять по одному к уже существующим

# В класс Note нужно добавить еще методы для удаления заголовка, текста, тэгов. И ЧТО-ТО ЕЩЕ?
# В класс Notes нужно добавить методы для удаления записи, поиска записи по тэгам и\или заголовку и\или по дате. Добавить метод для сортировке записей по дате и\или алфавиту. 
# Добавить методы для сохранения в файл на жесткий диск и метод для чтения из файла. И ЧТО-ТО ЕЩЕ?

class Note(UserDict):
    def __init__(self, title=None, tags=None, text=None):
        super().__init__()
        self.data["title"] = title
        self.data["tags"] = tags if tags is not None else []
        self.data["text"] = text
        self.data["date"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")    #date.today().strftime("%d.%m.%Y")
        
        # автоматическое добавление экземпляра класса Note в созданный экземпляр класса Notes. АПДЕЙТ. Убираем пока что эту строку с автоматическим добавлением
        # my_notes.add_note(self)

    def add_title(self, title):
        if self.data["title"] is None:
            self.data["title"] = title
    
    def add_tag(self, tag):
        if not isinstance(self.data["tags"], list):
            self.data["tags"] = []
        self.data["tags"].append(tag)
    
    def add_text(self, text):
        if self.data["text"] is None:
            self.data["text"] = text
        else:
            self.data["text"] += text

    def __str__(self):
        return f"{self.data["title"] if self.data["title"] else ""}\ntags: {', '.join(t for t in self.data["tags"]) if self.data["tags"] else ""}\n\
{self.data["text"] if self.data["text"] else ""}\n{self.data["date"]}"



class Notes(UserList):
    def __init__(self):
        super().__init__()

    def add_note(self, note):
        self.append(note)

    # удаление заметки по названию
    def delete_note_by_title(self, title):
        for note in self:
            if note.data["title"] == title:
                self.remove(note)
                return f'Note with title "{title}" has been deleted.'
        return f'Note with title "{title}" not found.'
    
    # удаление заметки по дате
    def delete_note_by_date(self, date):
        for note in self:
            if note.data["date"] == date:
                self.remove(note)
                return f'Note with date "{date}" has been deleted.'
        return f'Note with date "{date}" not found.'

    # сортировка и вывод заметок по дате - от более старых к новым
    def sort_by_date(self):
        sorted_by_date = sorted(self, key=lambda note: datetime.strptime(note.data["date"], "%d.%m.%Y %H:%M:%S"))
        return "\n--------------\n\n".join(str(note) for note in sorted_by_date)
    
    # сортировка и вывод заметок по дате в обратном порядке - от более новых к старым
    def sort_by_date_reverse(self):
        sorted_by_date_reverse = sorted(self, key=lambda note: datetime.strptime(note.data["date"], "%d.%m.%Y %H:%M:%S"), reverse=True)
        return "\n--------------\n\n".join(str(note) for note in sorted_by_date_reverse)

    def __str__(self):
        return "\n--------------\n\n".join(str(note) for note in self)


my_notes = Notes()

# нужно импортировать sleep, чтобы были промежутки во времени между созданием заметок. Это только для проверки, как будет работать сортировка по времени, чтобы была разница
# во времени создания заметок
# from time import sleep

# создаем одну нотатку
recipe_001 = Note("Иишенка", ["завтрак", "холостяк", "яйца"], "разбить и пожарить")
sleep(1)

# дописываем текст к уже существующему тексту созданной нотатки
recipe_001.add_text(", потом съесть")


# создаем вторую нотатку. В таком варианте создания поля "title", "tags", "text" будут пустые, а поле с датой заполнится автоматически
recipe_002 = Note()
sleep(1)

# заполняем поля
recipe_002.add_title("Греча с сосисой")
recipe_002.add_tag("греча")
# добавили второй тэг к уже существующему тэгу
recipe_002.add_tag("сосиса")
recipe_002.add_text("нормально приготовить и съесть")

recipe_003 = Note()
recipe_003.add_title("Крабовый ужин")
recipe_003.add_tag("романтический ужин")
recipe_003.add_tag("крабовые палки")
recipe_003.add_text("крабовые палки будем есть, дальше по ситуации")
sleep(1)

# добавим еще одну пустую нотатку в целях проверить, как именно будет выглядеть одна пустая нотатка в Нотатках
recipe_004 = Note()
sleep(1)

recipe_005 = Note()
recipe_005.add_title("Иишенка")
recipe_005.add_text("это другая иишенка для проверки поведения заметок с одинаковыми заголовком")

# добавляем отдельные заметки в Заметки
my_notes.add_note(recipe_001)
my_notes.add_note(recipe_002)
my_notes.add_note(recipe_003)
my_notes.add_note(recipe_004)
my_notes.add_note(recipe_005)


# принтим все Заметки целиком
print("\nmy_notes: \n")
print(my_notes)


# сортировка и вывод заметок по дате в обратном порядке - от более новых к старым
print("\nmy_notes.sort_by_date_reverse: \n")
print(my_notes.sort_by_date_reverse())


# удаление заметки по заголовку. Пока что работает так - находит первую заметку с указанным заголовком и удаляет ее.
# буду переделывать так, чтобы удалял все заметки с указанным заголовком в случае, если заметок с таким заголовком более одной
# либо нужно лишить юзера возможности создавать заметки с одинаковыми заголовками
print(my_notes.delete_note_by_title("Иишенка"))
print("\nmy_notes после удаления: \n")
print(my_notes)  # проверяем как выглядят все нотатки после удаления заметки


# удаление заметки по заголовку. Проверка случая, когда юзер пытается удалить несуществующую заметку 
print(my_notes.delete_note_by_title("цууке"))
print("\nmy_notes после удаления: \n")
print(my_notes)  # проверяем как выглядят все нотатки после попытки удаления заметки


