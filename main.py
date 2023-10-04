import sys
import sqlite3
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextBrowser, QInputDialog, QHBoxLayout

# Создаем базу данных
conn = sqlite3.connect('passwords.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY,
              login TEXT,
              password TEXT)''')
conn.commit()

class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.login_label = QLabel('Логин:')
        self.login_input = QLineEdit()

        self.password_label = QLabel('Пароль:')
        self.password_input = QLineEdit()

        self.save_button = QPushButton('Сохранить')
        self.search_button = QPushButton('Поиск')
        self.delete_button = QPushButton('Удалить')
        self.view_all_button = QPushButton('Просмотреть все')
        self.author_button = QPushButton('Автор')
        self.telegram_button = QPushButton('Телеграмм')

        self.result_display = QTextBrowser()

        vbox = QVBoxLayout()
        vbox.addWidget(self.login_label)
        vbox.addWidget(self.login_input)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_input)
        vbox.addWidget(self.save_button)
        vbox.addWidget(self.search_button)
        vbox.addWidget(self.delete_button)
        vbox.addWidget(self.view_all_button)
        vbox.addWidget(self.author_button)
        vbox.addWidget(self.telegram_button)
        vbox.addWidget(self.result_display)

        self.setLayout(vbox)

        self.save_button.setMaximumWidth(160)
        self.search_button.setMaximumWidth(160)
        self.delete_button.setMaximumWidth(160)
        self.view_all_button.setMaximumWidth(160)
        self.author_button.setMaximumWidth(160)
        self.telegram_button.setMaximumWidth(160)

        self.save_button.setFixedHeight(30)
        self.search_button.setFixedHeight(30)
        self.delete_button.setFixedHeight(30)
        self.view_all_button.setFixedHeight(30)
        self.author_button.setFixedHeight(30)
        self.telegram_button.setFixedHeight(30)

        self.save_button.clicked.connect(self.save_password)
        self.search_button.clicked.connect(self.search_password)
        self.delete_button.clicked.connect(self.delete_password)
        self.view_all_button.clicked.connect(self.view_all_passwords)
        self.author_button.clicked.connect(self.open_author_page)
        self.telegram_button.clicked.connect(self.open_telegram_page)

        hbox1 = QVBoxLayout()
        hbox1.addWidget(self.save_button)
        hbox1.addWidget(self.delete_button)

        hbox2 = QVBoxLayout()
        hbox2.addWidget(self.search_button)
        hbox2.addWidget(self.view_all_button)

        hbox3 = QVBoxLayout()
        hbox3.addWidget(self.author_button)
        hbox3.addWidget(self.telegram_button)

        hbox = QHBoxLayout()
        hbox.addLayout(hbox1)
        hbox.addLayout(hbox2)
        hbox.addLayout(hbox3)

        vbox.addLayout(hbox)

        self.setWindowTitle('QiyanaPassManager')
        self.setFixedSize(350, 400)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowIcon(QtGui.QIcon('ico.ico'))

        with open('dracula.css', 'r') as styleFile:
            self.setStyleSheet(styleFile.read())

    def save_password(self):
        login = self.login_input.text()
        password = self.password_input.text()

        if login and password:
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute('INSERT INTO passwords (login, password) VALUES (?, ?)', (login, password))
            conn.commit()
            conn.close()

            self.login_input.clear()
            self.password_input.clear()

    def search_password(self):
        fragment, ok = QInputDialog.getText(self, 'Поиск', 'Что вы хотите найти?')
        if ok and fragment:
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute('SELECT * FROM passwords WHERE login LIKE ? OR password LIKE ?', ('%'+fragment+'%', '%'+fragment+'%'))
            data = c.fetchall()
            conn.close()

            if data:
                self.result_display.clear()
                self.result_display.append("Результаты поиска:")
                for entry in data:
                    self.result_display.append(f"ID: {entry[0]}, Логин: {entry[1]}, Пароль: {entry[2]}")

    def delete_password(self):
        id_to_delete, ok = QInputDialog.getText(self, 'Удаление', 'Введите ID для удаления:')
        if ok and id_to_delete:
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute('DELETE FROM passwords WHERE id=?', (id_to_delete,))
            conn.commit()
            conn.close()

    def view_all_passwords(self):
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('SELECT * FROM passwords')
        data = c.fetchall()
        conn.close()

        if data:
            self.result_display.clear()
            self.result_display.append("Все пароли:")
            for entry in data:
                self.result_display.append(f"ID: {entry[0]}, Логин: {entry[1]}, Пароль: {entry[2]}")

    def open_author_page(self):
        import webbrowser
        webbrowser.open('https://zelenka.guru/sataraitsme/')
        
    def open_telegram_page(self):
        import webbrowser
        webbrowser.open('https://t.me/sataraitsme')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordManager()
    ex.show()
    sys.exit(app.exec_())