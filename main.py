import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)


class MainWindow(QWidget):
    # Создание конструктора объекта класса
    def __init__(self):
        super(MainWindow, self).__init__()

        # Создаем подключение к базе
        self._connect_to_db()

        # Титульное название таблицы
        self.setWindowTitle("Shedule")

        self.vbox = QVBoxLayout(self)

        # Создаем структуру которую можно заполнять вкладками
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        # Создаем вкладки
        self._create_shedule_tab()
        self._create_teacher_tab()
        self._create_subjects_tab()

    # Подключение к базе данных
    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="rasp",
                                     user="postgres",
                                     password="2258",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()


    def _create_shedule_tab(self):
        # Создание содержимого этих вкладок
        self.shedule_tab = QWidget()
        # Добавление окон с вкладками, передаем ему то окно которое должно вызываться по переходе на эту вкладку
        self.tabs.addTab(self.shedule_tab, "Shedule")
        self.svbox = QVBoxLayout()
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        for i in range(len(days)):
            # Текст который будет изображаться на рамочке и объединять такие же элементы
            # f'{}' - форматированный строковый литерал
            setattr(self, f'{days[i]}_gbox', QGroupBox(days[i]))
            # setattr функция устанавливающая значение атрибута указанного объекта по его имени
            # self - объект, значение атрибута которого требуется установить
            # f'shbox{i} - имя атрибута
            # QHBoxLayout - произвольное значение атрибута
            setattr(self, f'shbox{i}', QHBoxLayout())
            # getattribute - вызывается всегда для реализации доступа к атрибутам для экземпляров класса
            # getattr - позволяет получить значение атрибута объекта по его имени
            self.svbox.__getattribute__('addLayout')(getattr(self, f'shbox{i}'))
            getattr(self, f'shbox{i}').__getattribute__('addWidget')(getattr(self, f'{days[i]}_gbox'))
            self.__getattribute__('_create_day_table')(f'{days[i]}')

        # Создание элементов для выравнивания
        self.shbox5 = QHBoxLayout()
        # Выравнивание элементов по вертикали игоризонтали
        self.svbox.addLayout(self.shbox5)
        # Создание кнопки обновления
        self.update_shedule_button = QPushButton("Update")
        # Выравнивание этой кнопки
        self.shbox5.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

    def _create_teacher_tab(self):
        # Создание содержимого этих вкладок
        self.teacher_tab = QWidget()
        # Добавление окон с вкладками, передаем ему то окно которое должно вызываться по переходе на эту вкладку
        self.tabs.addTab(self.teacher_tab, "Teachers")

        # Текст который будет отображаться на рамочке
        self.teacher_gbox = QGroupBox("Teachers")

        # Создание элементов для выравнивания
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.teacher_gbox)

        # Создание таблицы такой же как в базе
        self._create_teacher_table()

        # Создание и выравнивание кнопки обновления
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.teacher_tab.setLayout(self.svbox)

    def _create_subjects_tab(self):
        # Создание содержимого этих вкладок
        self.subjects_tab = QWidget()
        # Добавление окон с вкладками, передаем ему то окно которое должно вызываться по переходе на эту вкладку
        self.tabs.addTab(self.subjects_tab, "Subjects")

        # Текст который будет отображаться на рамочке
        self.subjects_gbox = QGroupBox("Subjects")

        # Создание элементов для выравнивания
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.subjects_gbox)

        # Создание таблицы такой же как в базе
        self._create_subjects_table()

        # Создание и выравнивание кнопки обновления
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.subjects_tab.setLayout(self.svbox)


    def _create_day_table(self, day):
        # Создание пустой пользовательской таблицы
        # setattr функция устанавливающая значение атрибута указанного объекта по его имени
        # self - объект, значение атрибута которого требуется установить
        # f'day_table_{day} - имя атрибута
        # QTableWidget - произвольное значение атрибута
        setattr(self, f'day_table_{day}', QTableWidget())
        # Подстравиваем ширину под данный контекст
        # getattr - позволяет получить значение атрибута объекта по его имени
        getattr(self, f'day_table_{day}').setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Определение сколько столбцов будет в нашей таблице и их названия
        getattr(self, f'day_table_{day}').setColumnCount(7)
        getattr(self, f'day_table_{day}').setHorizontalHeaderLabels(["id", "day", "Subject", "Room", "Time", "", ""])

        # Обновление базы day
        self._update_day_table(day)

        # Создание вертикального box
        self.mvbox = QVBoxLayout()
        # Добавляеи box к таблице
        self.mvbox.addWidget(getattr(self, f'day_table_{day}'))
        # Передача таблицы
        getattr(self, f'{day}_gbox').setLayout(self.mvbox)

    def _create_teacher_table(self):
        # Создание пустой пользовательской таблицы
        self.teacher_table = QTableWidget()
        # Подстравиваем ширину под данный контекст
        self.teacher_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Определение сколько столбцов будет в нашей таблице и их названия
        self.teacher_table.setColumnCount(5)
        self.teacher_table.setHorizontalHeaderLabels(["id", "full_name", "Subject", "", ""])

        # Обновление базы teacher
        self._update_teacher_table()

        # Создание вертикального box
        self.mvbox = QVBoxLayout()
        # Добавляеи box к таблице
        self.mvbox.addWidget(self.teacher_table)
        # Передача таблицы
        self.teacher_gbox.setLayout(self.mvbox)

    def _create_subjects_table(self):
        # Создание пустой пользовательской таблицы
        self.subjects_table = QTableWidget()
        # Подстравиваем ширину под данный контекст
        self.subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Определение сколько столбцов будет в нашей таблице и их названия
        self.subjects_table.setColumnCount(3)
        self.subjects_table.setHorizontalHeaderLabels(["name", "", ""])

        # Обновление базы subjects
        self._update_subjects_table()

        # Создание вертикального box
        self.mvbox = QVBoxLayout()
        # Добавляеи box к таблице
        self.mvbox.addWidget(self.subjects_table)
        # Передача таблицы
        self.subjects_gbox.setLayout(self.mvbox)


    def _update_day_table(self, day):
        getattr(self, f'day_table_{str(day)}').setRowCount(0)
        # print(f"SELECT * FROM timetable WHERE day='{str(day)}'")
        # Обращение к курсору
        self.cursor.execute(f"SELECT * FROM timetable WHERE day='{str(day)}'")
        # Происходит возвращение запроса списком
        records = list(self.cursor.fetchall())

        # Обращение к таблице, передача длины списка в котором содержится информация из бд
        getattr(self, f'day_table_{day}').setRowCount(len(records) + 1)

        # Получение содержания индекса
        for i, r in enumerate(records):
            r = list(r)
            # Создание кнопок
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            insertButton = QPushButton("Insert")
            # Создание строк
            getattr(self, f'day_table_{day}').setItem(i, 0, QTableWidgetItem(str(r[0])))
            getattr(self, f'day_table_{day}').setItem(i, 1, QTableWidgetItem(str(r[1])))
            getattr(self, f'day_table_{day}').setItem(i, 2, QTableWidgetItem(str(r[2])))
            getattr(self, f'day_table_{day}').setItem(i, 3, QTableWidgetItem(str(r[3])))
            getattr(self, f'day_table_{day}').setItem(i, 4, QTableWidgetItem(str(r[4])))
            # Создание кнопки в конкретной строке
            getattr(self, f'day_table_{day}').setCellWidget(i, 5, joinButton)
            getattr(self, f'day_table_{day}').setCellWidget(i, 6, deleteButton)
            getattr(self, f'day_table_{day}').setCellWidget(len(records), 5, insertButton)

            # Функция обработчика для запоминани кнопки joinButton
            joinButton.clicked.connect(lambda ch, num=i, day=day: self._change_day_from_table(num, day))
            deleteButton.clicked.connect(
                lambda ch, id_to_delete=r[0], num=i: self._delete_day_from_table(id_to_delete, num, day))
            insertButton.clicked.connect(lambda ch, num=i + 1: self._insert_day_from_table(num, day))

            # Адаптирование размеров ячеек под размеры данных таблицы
            getattr(self, f'day_table_{day}').resizeRowsToContents()

        if len(records) == 0:
            insertButton = QPushButton("Insert 1st record")
            getattr(self, f'day_table_{day}').setCellWidget(len(records), 5, insertButton)
            insertButton.clicked.connect(lambda ch, num=0: self._insert_day_from_table(num, day))

            getattr(self, f'day_table_{day}').resizeRowsToContents()

    def _update_teacher_table(self):
        self.teacher_table.removeRow(0)
        # Обращение к курсору
        self.cursor.execute("SELECT * FROM teacher")
        # Происходит возвращение запроса списком
        records = list(self.cursor.fetchall())
        # Обращение к таблице, передача длины списка в котором содержится информация из бд
        self.teacher_table.setRowCount(len(records) + 1)

        # Получение содержания индекса
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            insertButton = QPushButton("Insert")
            self.teacher_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.teacher_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            self.teacher_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            self.teacher_table.setCellWidget(i, 3, joinButton)
            self.teacher_table.setCellWidget(i, 4, deleteButton)
            self.teacher_table.setCellWidget(len(records), 3, insertButton)
            # Функция обработчика для запоминани кнопки joinButton
            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher_from_table(num))
            deleteButton.clicked.connect(
                lambda ch, id_to_delete=r[0], num=i: self._delete_teacher_from_table(id_to_delete, num))
            insertButton.clicked.connect(lambda ch, num=i + 1: self._insert_teacher_from_table(num))

            # Адаптирование размеров ячеек под размеры данных таблицы
            self.teacher_table.resizeRowsToContents()

        if len(records) == 0:
            insertButton = QPushButton("Insert 1st record")
            self.teacher_table.setCellWidget(len(records), 3, insertButton)
            insertButton.clicked.connect(lambda ch, num=0: self._insert_teacher_from_table(num))

            self.teacher_table.resizeRowsToContents()

    def _update_subjects_table(self):
        self.subjects_table.removeRow(0)
        # Обращение к курсору
        self.cursor.execute("SELECT * FROM subject")
        records = list(self.cursor.fetchall())
        self.subjects_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            deleteButton = QPushButton("Delete")
            insertButton = QPushButton("Insert")
            self.subjects_table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            self.subjects_table.setCellWidget(i, 1, joinButton)
            self.subjects_table.setCellWidget(i, 2, deleteButton)
            self.subjects_table.setCellWidget(len(records), 1, insertButton)
            joinButton.clicked.connect(lambda ch, num=i: self._change_subjects_from_table(num))
            deleteButton.clicked.connect(
                lambda ch, id_to_delete=r[0], num=i: self._delete_subjects_from_table(id_to_delete, num))
            insertButton.clicked.connect(lambda ch, num=i + 1: self._insert_subjects_from_table(num))

            self.subjects_table.resizeRowsToContents()

        if len(records) == 0:
            insertButton = QPushButton("Insert 1st record")
            self.subjects_table.setCellWidget(len(records), 2, insertButton)
            insertButton.clicked.connect(lambda ch, num=0: self._insert_subjects_from_table(num))

            self.subjects_table.resizeRowsToContents()


    def _change_day_from_table(self, rowNum, day):
        # Создание списка строк
        row = list()
        # Находим конкретную строку и записываем значения в колонки
        for i in range(getattr(self, f'day_table_{day}').columnCount()):
            try:
                row.append(getattr(self, f'day_table_{day}').item(rowNum, i).text())
            except:
                row.append(None)


        # Запрос на обновления данных
        try:
            self.cursor.execute(
                f"UPDATE timetable SET (day, subject, room_numb, start_time) = ('{row[1]}','{row[2]}','{row[3]}','{row[4]}') WHERE id={row[0]};")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")


    def _change_teacher_from_table(self, rowNum):
        # Создание списка строк
        row = list()
        # Находим конкретную строку и записываем значения в колонки
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)

        # Запрос на обновления данных
        try:
            self.cursor.execute(
                "UPDATE teacher SET subject='" + str(row[2]) + "', full_name='" + row[1] + "' where id='" + str(
                    row[0]) + "'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")

    def _change_subjects_from_table(self, rowNum):
        row = list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(rowNum, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute("UPDATE subject SET subject='" + row[1] + "' where id='" + str(row[0]) + "'")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")


    def _delete_day_from_table(self, delete, rowNum, day):
        try:
            self.cursor.execute("delete from timetable where id=" + str(delete) + ";")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Field doesn't exist")
        getattr(self, f'day_table_{day}').removeRow(rowNum)
        self._update_day_table(day)

    def _delete_subjects_from_table(self, delete, rowNum):
        try:
            self.cursor.execute("delete from subject where name='" + str(delete) + "';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Field doesn't exist")
        self.subjects_table.removeRow(rowNum)
        self._update_subjects_table()

    def _delete_teacher_from_table(self, delete, rowNum):
        try:
            self.cursor.execute("delete from teacher where id='" + str(delete) + "';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Field doesn't exist")
        self.teacher_table.removeRow(rowNum)
        self._update_teacher_table()

    def _insert_day_from_table(self, rowNum, day):
        row = list()
        for i in range(getattr(self, f'day_table_{day}').columnCount()):
            try:
                row.append(getattr(self, f'day_table_{day}').item(rowNum, i).text())
            except:
                row.append(None)


        try:
            self.cursor.execute(
                f"insert into timetable values ({str(row[0])},'{str(row[1])}','{str(row[2])}','{str(row[3])}','{str(row[4])}');")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")


    def _insert_teacher_from_table(self, rowNum):
        row = list()
        for i in range(self.teacher_table.columnCount()):
            try:
                row.append(self.teacher_table.item(rowNum, i).text())
            except:
                row.append(None)


        try:
            self.cursor.execute(
                "insert into teacher values ('" + str(row[0]) + "', '" + row[1] + "', '" + str(row[2]) + "');")
            self.conn.commit()

        except:
            QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")


    def _insert_subjects_from_table(self, rowNum):
        # Создание списка строк
        row = list()
        # Находим конкретную строку и записываем значения в колонки
        for i in range(self.subjects_table.columnCount()):
            try:
                # Возвращение текста записанного в определенной ячейке
                row.append(self.subjects_table.item(rowNum, i).text())
            except:
                row.append(None)

        # Запрос на обновления данных
        try:
            self.cursor.execute("insert into subject values ('" + str(row[0]) + "');")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Fill in all the fields in the row correctly!")


    # Создаем метод обновляющий все таблицы на вкладке
    def _update_shedule(self):
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
        for day in days:
            self._update_day_table(day)
        self._update_teacher_table()
        self._update_subjects_table()

# Запуск приложения
app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())





