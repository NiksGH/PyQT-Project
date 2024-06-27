import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

LOGIN_SCREEN_INDEX = 0
SHELF_SCREEN_INDEX = 1
AUTHORS_SCREEN_INDEX = 2


class App(QWidget):
    def __init__(self):
        super().__init__()
        # Установить начальное положение и размер окна
        self.setGeometry(0, 0, 500, 350)
        self.setWindowTitle('Always-read')

        # Создаем экраны приложения
        self.loginScreen = QWidget()
        self.shelfScreen = QWidget()
        self.shelfAuthor = QWidget()

        self.loginScreenUI()
        self.shelfScreenUI()
        self.shelfAuthorUI()

        # Кладем все наши экраны в стек
        self.stack = QStackedWidget(self)

        self.stack.addWidget(self.loginScreen)
        self.stack.addWidget(self.shelfScreen)
        self.stack.addWidget(self.shelfAuthor)

        # Отображаем стек пользователю
        HBox = QHBoxLayout()
        HBox.addWidget(self.stack)
        self.setLayout(HBox)

    # LOGIN SCREEN

    def loginScreenUI(self):
        layout = QVBoxLayout()

        lbl1 = QLabel('Вход')
        lbl1.setFont(QFont('Arial', 20))
        lbl1.setAlignment(Qt.AlignCenter)
        lbl1.setStyleSheet('color: white')
        layout.addWidget(lbl1)

        self.loginScreen_login = QLineEdit()
        self.loginScreen_login.setPlaceholderText('Логин')
        self.loginScreen_login.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.loginScreen_login)

        self.loginScreen_password = QLineEdit()
        self.loginScreen_password.setPlaceholderText('Пароль')
        self.loginScreen_password.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.loginScreen_password)

        btn = QPushButton('Войти')
        btn.clicked.connect(self.auth)
        btn.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(btn)

        self.loginScreen_error = QLabel('')
        self.loginScreen_error.setStyleSheet('color: red')
        layout.addWidget(self.loginScreen_error)

        self.setStyleSheet("background-color: rgb(43, 56, 67);")

        self.loginScreen.setLayout(layout)

    def auth(self):
        l = self.loginScreen_login.text()
        p = self.loginScreen_password.text()
        if len(l) > 0 and len(p) > 0:
            result = cur.execute("""SELECT password, role FROM users
                WHERE login = ?""", (l,)).fetchall()
            if len(result) == 0:
                self.loginScreen_error.setText('Неверный логин')
            elif result[0][0] != p:
                self.loginScreen_error.setText('Неверный пароль')
            else:
                self.current_user_role = result[0][1]
                if self.current_user_role != 'admin':
                    self.redact.hide()
                    self.redact_a.hide()
                self.stack.setCurrentIndex(SHELF_SCREEN_INDEX)
        else:
            self.loginScreen_error.setText('Заполните поля')

    # SHELF SCREEN

    def shelfScreenUI(self):
        # Горизонтальный макет
        layout = QHBoxLayout()
        self.shelfScreen_leftColumn = QWidget()
        self.shelfLeftColumnUI()

        self.shelfScreen_rightColumn = QWidget()
        self.shelfRightUI()

        layout.addWidget(self.shelfScreen_leftColumn)
        layout.addWidget(self.shelfScreen_rightColumn)

        self.shelfScreen.setLayout(layout)

    def shelfLeftColumnUI(self):
        layout = QVBoxLayout()

        label = QLabel()
        pixmap = QPixmap('logo-always-read-wight.png')
        label.setPixmap(pixmap)
        label.setFixedSize(70, 69)
        layout.addWidget(label)

        btn1 = QPushButton('Книги')
        btn1.setFixedSize(70, 20)
        btn1.clicked.connect(self.openBooks)
        btn1.setStyleSheet('QPushButton {background-color: rgb(43, 56, 67); color: white;}')
        layout.addWidget(btn1)

        btn2 = QPushButton('Авторы')
        btn2.setFixedSize(70, 20)
        btn2.clicked.connect(self.openAuthors)
        btn2.setStyleSheet('QPushButton {background-color: rgb(43, 56, 67); color: white;}')
        layout.addWidget(btn2)


        #leftlist = QListWidget()
        #leftlist.insertItem(0, 'Книги')
        #leftlist.insertItem(1, 'Авторы')
        #layout.addWidget(leftlist)

        self.shelfScreen_leftColumn.setStyleSheet("background-color: rgb(69, 92, 114);")

        self.shelfScreen_leftColumn.setLayout(layout)

    def shelfRightUI(self):
        layout = QVBoxLayout()

        search = QWidget()

        search_layout = QHBoxLayout()

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText('Поиск')
        self.search_line.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        search_layout.addWidget(self.search_line)

        self.search_button = QPushButton('Искать')
        self.search_button.clicked.connect(self.search)
        self.search_button.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        search_layout.addWidget(self.search_button)

        search.setLayout(search_layout)
        layout.addWidget(search)


        self.bookList = QTableWidget()
        self.bookList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.getBooks()
        self.bookList.setColumnCount(4)
        self.bookList.setRowCount(len(self.books))
        self.bookList.setHorizontalHeaderLabels(["Название", "Жанр", "Автор", "Текущий читатель"])

        for i in range(len(self.books)):
            self.bookList.setItem(i, 0, QTableWidgetItem(self.books[i][1]))
            self.bookList.setItem(i, 1, QTableWidgetItem(self.books[i][3]))
            self.bookList.setItem(i, 2, QTableWidgetItem(self.books[i][4]))
            self.bookList.setItem(i, 3, QTableWidgetItem(self.books[i][5]))

        self.bookList.resizeColumnsToContents()
        self.bookList.clicked.connect(self.openBookInfo)
        self.bookList.setStyleSheet('QTableWidget {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.bookList)

        self.redact = QWidget()

        redact_layout = QHBoxLayout()

        self.add_button = QPushButton('Добавить книгу')
        self.add_button.clicked.connect(self.addBook)
        self.add_button.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        redact_layout.addWidget(self.add_button)

        self.update_btn = QPushButton('Показать все книги')
        self.update_btn.clicked.connect(self.update)
        self.update_btn.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        redact_layout.addWidget(self.update_btn)

        self.redact.setLayout(redact_layout)
        layout.addWidget(self.redact)

        self.shelfScreen_rightColumn.setLayout(layout)

    def shelfAuthorRightUI(self):
        layout = QVBoxLayout()

        search = QWidget()

        search_layout = QHBoxLayout()

        self.search_author = QLineEdit()
        self.search_author.setPlaceholderText('Поиск')
        self.search_author.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        search_layout.addWidget(self.search_author)

        self.button_author = QPushButton('Искать')
        self.button_author.clicked.connect(self.searchAuthor)
        self.button_author.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        search_layout.addWidget(self.button_author)

        search.setLayout(search_layout)
        layout.addWidget(search)

        self.authorList = QTableWidget()
        self.authorList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.getAuthors()
        self.authorList.setColumnCount(2)
        self.authorList.setRowCount(len(self.searched_authors))
        self.authorList.setHorizontalHeaderLabels(["Автор", "Дата рождения"])

        for i in range(len(self.searched_authors)):
            self.authorList.setItem(i, 0, QTableWidgetItem(self.searched_authors[i][1]))
            self.authorList.setItem(i, 1, QTableWidgetItem(self.searched_authors[i][2]))

        self.authorList.resizeColumnsToContents()
        self.authorList.clicked.connect(self.openAuthorInfo)
        self.authorList.setStyleSheet('QTableWidget {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.authorList)

        self.redact_a = QWidget()

        redact_layout = QHBoxLayout()

        self.add_author = QPushButton('Добавить автора')
        self.add_author.clicked.connect(self.addAuthor)
        self.add_author.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        redact_layout.addWidget(self.add_author)

        self.update_author = QPushButton('Показать всех авторов')
        self.update_author.clicked.connect(self.updateAuthor)
        self.update_author.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        redact_layout.addWidget(self.update_author)

        self.redact_a.setLayout(redact_layout)
        layout.addWidget(self.redact_a)

        self.column_author.setLayout(layout)

    def shelfAuthorUI(self):
        # Горизонтальный макет
        layout = QHBoxLayout()
        self.shelfScreen_leftColumn = QWidget()
        self.shelfLeftColumnUI()

        self.column_author = QWidget()
        self.shelfAuthorRightUI()

        layout.addWidget(self.shelfScreen_leftColumn)
        layout.addWidget(self.column_author)

        self.shelfAuthor.setLayout(layout)

    def searchAuthor(self):
        self.searched_authors = list(filter(lambda x: self.search_author.text() in x[1], self.authors))
        self.authorList.setRowCount(len(self.searched_authors))
        for i in range(len(self.searched_authors)):
            self.authorList.setItem(i, 0, QTableWidgetItem(self.searched_authors[i][1]))
            self.authorList.setItem(i, 1, QTableWidgetItem(self.searched_authors[i][2]))

    def updateAuthor(self):
        self.getAuthors()
        self.authorList.setRowCount(len(self.searched_authors))
        for i in range(len(self.searched_authors)):
            self.authorList.setItem(i, 0, QTableWidgetItem(self.searched_authors[i][1]))
            self.authorList.setItem(i, 1, QTableWidgetItem(self.searched_authors[i][2]))

    def addAuthor(self):
        self.w1 = AddAuthor()
        self.w1.show()

    def getAuthors(self):
        self.authors = cur.execute("""SELECT * FROM authors""").fetchall()
        self.searched_authors = self.authors

    def openBooks(self):
        self.stack.setCurrentIndex(SHELF_SCREEN_INDEX)

    def openAuthors(self):
        self.stack.setCurrentIndex(AUTHORS_SCREEN_INDEX)

    def search(self):
        self.searched_books = list(filter(lambda x: self.search_line.text() in x[1], self.books))
        self.bookList.setRowCount(len(self.searched_books))
        for i in range(len(self.searched_books)):
                self.bookList.setItem(i, 0, QTableWidgetItem(self.searched_books[i][1]))
                self.bookList.setItem(i, 1, QTableWidgetItem(self.searched_books[i][3]))
                self.bookList.setItem(i, 2, QTableWidgetItem(self.searched_books[i][4]))
                self.bookList.setItem(i, 3, QTableWidgetItem(self.searched_books[i][5]))

    def addBook(self):
        self.w2 = AddBook()
        self.w2.show()

    def update(self):
        self.getBooks()
        self.bookList.setRowCount(len(self.searched_books))
        for i in range(len(self.books)):
            self.bookList.setItem(i, 0, QTableWidgetItem(self.searched_books[i][1]))
            self.bookList.setItem(i, 1, QTableWidgetItem(self.searched_books[i][3]))
            self.bookList.setItem(i, 2, QTableWidgetItem(self.searched_books[i][4]))
            self.bookList.setItem(i, 3, QTableWidgetItem(self.searched_books[i][5]))

    def getBooks(self):
        result = cur.execute("""SELECT * FROM books""").fetchall()
        for i in range(len(result)):
            id_author = result[i][4]
            id_renter = result[i][5]
            author = cur.execute("""SELECT name FROM authors
                WHERE id = ?""", (id_author,)).fetchall()[0][0]
            if id_renter != None:
                renter = cur.execute("""SELECT login FROM users
                                WHERE id = ?""", (id_renter,)).fetchall()[0][0]
            else:
                renter = '-'
            result[i] = (result[i][0], result[i][1], result[i][2], result[i][3], author, renter)
        self.books = result
        self.searched_books = result

    def openBookInfo(self, clicked_index):
        row = clicked_index.row()
        self.current_book = self.searched_books[row]
        self.w2 = BookInfo(self.current_book, self.current_user_role)
        self.w2.show()

    def openAuthorInfo(self, clicked_index):
        row = clicked_index.row()
        self.current_author = self.searched_authors[row]
        self.w1 = AuthorInfo(self.current_author, self.current_user_role)
        self.w1.show()

BOOK_INFO_SCREEN_INDEX = 0
BOOK_EDIT_INFO_SCREEN_INDEX = 1

class BookInfo(QWidget):
    def __init__(self, book, role):
        self.book = book
        self.role = role
        self.getAuthors()
        self.getReader()

        super().__init__()

        self.setGeometry(530, 30, 500, 350)
        self.setWindowTitle('Always-read')

        self.setStyleSheet("background-color: rgb(43, 56, 67);")

        self.bookInfoScreen = QWidget()
        self.bookEditInfoScreen = QWidget()

        self.bookInfoScreenUI()
        self.bookEditInfoScreenUI()

        # Кладем все наши экраны в стек
        self.stack = QStackedWidget(self)

        self.stack.addWidget(self.bookInfoScreen)
        self.stack.addWidget(self.bookEditInfoScreen)

        # Отображаем стек пользователю
        HBox = QHBoxLayout()
        HBox.addWidget(self.stack)
        self.setLayout(HBox)

    def bookInfoScreenUI(self):
        layout = QVBoxLayout()

        name = QWidget()

        name_layout = QHBoxLayout()

        label = QLabel()
        pixmap = QPixmap('logo-always-read-wight.png')
        label.setPixmap(pixmap)
        name_layout.addWidget(label)

        self.name_book = QLabel(self.book[1])
        self.name_book.setStyleSheet('color: white;')
        name_layout.addWidget(self.name_book)

        name.setLayout(name_layout)
        layout.addWidget(name)

        self.info = QLabel(self.book[2])
        self.info.setStyleSheet('color: white;')
        self.info.setWordWrap(True)
        layout.addWidget(self.info)

        self.btn1 = QPushButton('Редактировать')
        self.btn1.clicked.connect(self.redect)
        self.btn1.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.btn1)

        if self.role != 'admin':
            self.btn1.hide()

        self.bookInfoScreen.setLayout(layout)

    def redect(self):
        self.stack.setCurrentIndex(BOOK_EDIT_INFO_SCREEN_INDEX)

    def getAuthors(self):
        self.authors = cur.execute("""SELECT * FROM authors""").fetchall()

    def getReader(self):
        self.users = cur.execute("""SELECT * FROM users""").fetchall()

    def bookEditInfoScreenUI(self):
        layout = QVBoxLayout()

        self.name_b = QLineEdit()
        self.name_b.setText(self.book[1])
        self.name_b.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.name_b)

        self.author = QComboBox(self)
        for i in range(len(self.authors)):
            self.author.addItem(self.authors[i][1])
        self.author.setCurrentText(self.book[4])
        self.author.setStyleSheet('QComboBox {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.author)

        self.janre = QLineEdit()
        self.janre.setText(self.book[3])
        self.janre.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.janre)

        self.reader = QComboBox(self)
        for i in range(len(self.users)):
            self.reader.addItem(self.users[i][1])
        self.reader.addItem('-')
        self.reader.setCurrentText(self.book[5])
        self.reader.setStyleSheet('QComboBox {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.reader)

        self.description = QLineEdit()
        self.description.setText(self.book[2])
        self.description.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.description)

        self.save_btn = QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save)
        self.save_btn.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton('Отменить')
        self.cancel_btn.clicked.connect(self.cancel)
        self.cancel_btn.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.cancel_btn)

        self.bookEditInfoScreen.setLayout(layout)

    def cancel(self):
        self.stack.setCurrentIndex(BOOK_INFO_SCREEN_INDEX)

    def save(self):
        cur.execute("""UPDATE books
                        SET name = ?
                        WHERE id = ?""", (self.name_b.text(), self.book[0]))
        self.name_book.setText(self.name_b.text())

        cur.execute("""UPDATE books
                                SET genres = ?
                                WHERE id = ?""", (self.janre.text(), self.book[0]))

        cur.execute("""UPDATE books
                                SET description = ?
                                WHERE id = ?""", (self.description.text(), self.book[0]))
        self.info.setText(self.description.text())

        for i in range(len(self.authors)):
            if self.author.currentText() == self.authors[i][1]:
                a = self.authors[i][0]

        cur.execute("""UPDATE books
                                SET author = ?
                                WHERE id = ?""", (a, self.book[0]))

        if self.reader.currentText() != '-':
            for i in range(len(self.users)):
                if self.reader.currentText() == self.users[i][1]:
                    a = self.users[i][0]

        else:
            a = None

        cur.execute("""UPDATE books
                                SET renter = ?
                                WHERE id = ?""", (a, self.book[0]))

        con.commit()
        self.stack.setCurrentIndex(BOOK_INFO_SCREEN_INDEX)


class AddBook(QWidget):
    def __init__(self):
        super().__init__()

        self.authors = cur.execute("""SELECT * FROM authors""").fetchall()
        self.users = cur.execute("""SELECT * FROM users""").fetchall()

        self.setGeometry(530, 30, 500, 350)
        self.setWindowTitle('Always-read')

        self.addBookUI()

    def addBookUI(self):
        layout = QVBoxLayout()

        self.setStyleSheet("background-color: rgb(43, 56, 67);")

        self.name_b = QLineEdit()
        self.name_b.setPlaceholderText('Название книги')
        self.name_b.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.name_b)

        self.author = QComboBox(self)
        for i in range(len(self.authors)):
            self.author.addItem(self.authors[i][1])
        self.author.setStyleSheet('QComboBox {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.author)

        self.janre = QLineEdit()
        self.janre.setPlaceholderText('Жанр книги')
        self.janre.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.janre)

        self.reader = QComboBox(self)
        for i in range(len(self.users)):
            self.reader.addItem(self.users[i][1])
        self.reader.addItem('-')
        self.reader.setStyleSheet('QComboBox {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.reader)

        self.description = QLineEdit()
        self.description.setPlaceholderText('Описание книги')
        self.description.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.description)

        self.save_btn = QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save)
        self.save_btn.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.save_btn)

        self.success = QLabel('')
        layout.addWidget(self.success)

        self.setLayout(layout)

    def save(self):
        for i in range(len(self.authors)):
            if self.author.currentText() == self.authors[i][1]:
                a = self.authors[i][0]

        if self.reader.currentText() != '-':
            for i in range(len(self.users)):
                if self.reader.currentText() == self.users[i][1]:
                    b = self.users[i][0]

        else:
            b = None

        cur.execute("""INSERT INTO books(name, description, genres, author, renter) VALUES(?, ?, ?, ?, ?);""", (self.name_b.text(), self.description.text(), self.janre.text(), a, b))

        con.commit()
        self.success.setText(f'Книга добавлена: {self.name_b.text()}')


class AddAuthor(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(530, 30, 500, 350)
        self.setWindowTitle('Always-read')

        self.addAuthorUI()

    def addAuthorUI(self):
        layout = QVBoxLayout()

        self.setStyleSheet("background-color: rgb(43, 56, 67);")

        self.author = QLineEdit()
        self.author.setPlaceholderText('Автор')
        self.author.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.author)

        self.data = QLineEdit()
        self.data.setPlaceholderText('Дата рождения')
        self.data.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.data)

        self.save_btn = QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save)
        self.save_btn.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.save_btn)

        self.success = QLabel('')
        self.success.setStyleSheet('color: white;}')
        layout.addWidget(self.success)

        self.setLayout(layout)

    def save(self):
        cur.execute("""INSERT INTO authors(name, date_of_birth) VALUES(?, ?);""", (self.author.text(), self.data.text()))

        con.commit()
        self.success.setText(f'Автор добавлен: {self.author.text()}')

AUTHORS_EDIT_SCREEN_INDEX = 1

class AuthorInfo(QWidget):
    def __init__(self, author, role):
        self.author = author
        self.role = role
        self.getBooks()

        super().__init__()

        self.setGeometry(530, 30, 500, 350)
        self.setWindowTitle('Always-read')

        self.authorInfoScreen = QWidget()
        self.authorEditInfoScreen = QWidget()

        self.authorInfoScreenUI()
        self.authorEditInfoScreenUI()

        # Кладем все наши экраны в стек
        self.stack = QStackedWidget(self)

        self.stack.addWidget(self.authorInfoScreen)
        self.stack.addWidget(self.authorEditInfoScreen)

        # Отображаем стек пользователю
        HBox = QHBoxLayout()
        HBox.addWidget(self.stack)
        self.setLayout(HBox)

    def authorInfoScreenUI(self):
        layout = QVBoxLayout()

        name = QWidget()

        name_layout = QHBoxLayout()

        self.setStyleSheet("background-color: rgb(43, 56, 67);")

        label = QLabel()
        pixmap = QPixmap('logo-always-read-wight.png')
        label.setPixmap(pixmap)
        name_layout.addWidget(label)

        self.author_name = QLabel(self.author[1])
        self.author_name.setStyleSheet('color: white;}')
        name_layout.addWidget(self.author_name)

        name.setLayout(name_layout)
        layout.addWidget(name)

        self.info = QLabel(self.books)
        self.info.setWordWrap(True)
        self.info.setStyleSheet('color: white;}')
        layout.addWidget(self.info)

        self.btn1 = QPushButton('Редактировать')
        self.btn1.clicked.connect(self.redect)
        self.btn1.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.btn1)

        if self.role != 'admin':
            self.btn1.hide()

        self.authorInfoScreen.setLayout(layout)

    def redect(self):
        self.stack.setCurrentIndex(AUTHORS_EDIT_SCREEN_INDEX)

    def getAuthors(self):
        self.authors = cur.execute("""SELECT * FROM authors""").fetchall()

    def getReader(self):
        self.users = cur.execute("""SELECT * FROM users""").fetchall()

    def authorEditInfoScreenUI(self):
        layout = QVBoxLayout()

        self.name_a = QLineEdit()
        self.name_a.setText(self.author[1])
        self.name_a.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.name_a)

        self.data = QLineEdit()
        self.data.setText(self.author[2])
        self.data.setStyleSheet('QLineEdit {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.data)

        self.save_btn = QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save_a)
        self.save_btn.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton('Отменить')
        self.cancel_btn.clicked.connect(self.cancel_a)
        self.cancel_btn.setStyleSheet('QPushButton {background-color: rgb(69, 92, 114); color: white;}')
        layout.addWidget(self.cancel_btn)

        self.authorEditInfoScreen.setLayout(layout)

    def cancel_a(self):
        self.stack.setCurrentIndex(AUTHORS_SCREEN_INDEX)

    def save_a(self):
        cur.execute("""UPDATE authors
                        SET name = ?
                        WHERE id = ?""", (self.name_a.text(), self.author[0]))
        self.author_name.setText(self.name_a.text())

        cur.execute("""UPDATE authors
                                SET date_of_birth = ?
                                WHERE id = ?""", (self.data.text(), self.author[0]))

        con.commit()
        self.stack.setCurrentIndex(AUTHORS_SCREEN_INDEX)

    def getBooks(self):
        result = cur.execute("""SELECT * FROM books
            WHERE author = ?""", (self.author[0],)).fetchall()
        self.books = '\n'.join(map(lambda x: x[1], result))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = App()
    demo.show()
    sys.exit(app.exec_())