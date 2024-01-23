import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
import mysql.connector
import random

class RandomNickApp(QWidget):
    def __init__(self):
        super().__init__()

        # Połączenie z bazą danych MySQL
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Puste hasło, jeśli takie jest
            database="nicki"
        )

        # Utworzenie kursora
        self.cursor = self.db_connection.cursor()

        # Utworzenie interfejsu graficznego
        self.init_ui()

    def init_ui(self):
        try:
            # Utworzenie elementów interfejsu
            self.label1 = QLabel('Twój losowo wygenerowany, słodki/bojowy/dziwny nick to:')
            self.label2 = QLabel()
            self.type_combobox = QComboBox()
            self.type_combobox.addItems(['Słodki', 'Bojowy', 'Dziwny'])
            self.generate_button = QPushButton(self)

            # Zmiana wyglądu guzika
            self.update_button_image()

            # Połączenie przycisku z funkcją generowania nicku
            self.generate_button.clicked.connect(self.generate_nick)
            self.type_combobox.currentIndexChanged.connect(self.update_button_image)

            # Zmiana wielkości rozwijanego paska
            self.type_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            # Ustawienia stylizacji i wyglądu
            self.setWindowIcon(QIcon('icon.png'))  # Zmień 'icon.png' na ścieżkę do ikony
            self.setWindowTitle('Generator NICKów')
            self.label1.setFont(QFont('Arial', 15))  # Ustawienie czcionki dla etykiety

            # Dodanie elementów do układu
            vertical_layout = QVBoxLayout()
            vertical_layout.setContentsMargins(20, 20, 20, 20)  # Dodanie marginesów (lewy, górny, prawy, dolny)

            # Dodanie pustego miejsca na górze
            vertical_layout.addStretch()

            # Utworzenie poziomego układu dla przycisku
            horizontal_layout = QHBoxLayout()
            horizontal_layout.addStretch()  # Dodanie pustego miejsca po lewej
            horizontal_layout.addWidget(self.generate_button, 0, alignment=Qt.AlignCenter)  # Wycentrowanie przycisku
            horizontal_layout.addStretch()  # Dodanie pustego miejsca po prawej

            # Dodanie poziomego układu do pionowego
            vertical_layout.addWidget(self.label1)
            vertical_layout.addWidget(self.type_combobox)
            vertical_layout.addWidget(self.label2)
            vertical_layout.addLayout(horizontal_layout)

            # Dodanie pustego miejsca na dole
            vertical_layout.addStretch()

            self.setLayout(vertical_layout)
            self.update_background_color()  # Dodanie zmiany koloru tła na początku
            self.update_font_color()  # Dodanie zmiany koloru czcionki na początku
        except Exception as e:
            print(f"Błąd inicjalizacji interfejsu: {e}")

    def set_button_image(self, button, image_path):
        pixmap = QPixmap(image_path)
        button.setIcon(QIcon(pixmap))
        button.setIconSize(pixmap.rect().size())
        button.setFixedSize(pixmap.rect().size())

    def update_button_image(self):
        selected_type = self.type_combobox.currentText()
        if selected_type == 'Słodki':
            self.set_button_image(self.generate_button, 'button_sweet.png')
        elif selected_type == 'Bojowy':
            self.set_button_image(self.generate_button, 'button_combat.png')
        elif selected_type == 'Dziwny':
            self.set_button_image(self.generate_button, 'button_scary.png')

        self.update_background_color()
        self.update_font_color()

    def update_background_color(self):
        selected_type = self.type_combobox.currentText()
        if selected_type == 'Słodki':
            self.setStyleSheet("background-color: #915546;")  # Kolor brązowy dla słodkich
        elif selected_type == 'Bojowy':
            self.setStyleSheet("background-color: #536FFF;")  # Kolor niebieski dla bojowych
        elif selected_type == 'Dziwny':
            self.setStyleSheet("background-color: #002200;")  # Kolor ciemn-ziel dla dziwnych

    def update_font_color(self):
        selected_type = self.type_combobox.currentText()
        if selected_type == 'Słodki':
            self.label1.setStyleSheet("color: #FAD4E2;")  # Róż dla etykiety słodki
            self.label2.setStyleSheet("color: #FAD4E2;")  # Róż dla etykiety słodki
        elif selected_type == 'Bojowy':
            self.label1.setStyleSheet("color: #ffffff;")  # biały dla etykiety
            self.label2.setStyleSheet("color: #ffffff;")  # biały czerwony dla etykiety
        elif selected_type == 'Dziwny':
            self.label1.setStyleSheet("color: #75FF53;")  # Kolor ziel dla etykiety dziwnych
            self.label2.setStyleSheet("color: #75FF53;")  # Kolor ziel dla etykiety dziwnych

    def generate_nick(self):
        try:
            # Pobranie wybranej wartości z rozwijanej listy
            selected_type = self.type_combobox.currentText()

            # Pobranie losowego nicku z obu tabel, gdzie typ = selected_type
            first_part_nick = self.get_random_nick("pierwsza_czesc", selected_type)
            second_part_nick = self.get_random_nick("druga_czesc", selected_type)

            # Ustawienie tekstu w etykiecie
            if first_part_nick is not None and second_part_nick is not None:
                self.label2.setText(f'{first_part_nick} {second_part_nick}')
            else:
                self.label2.setText('Nie można znaleźć pasującego nicku.')
        except Exception as e:
            print(f"Błąd generowania nicku: {e}")

    def get_random_nick(self, table_name, type_value):
        try:
            # Zapytanie SQL do pobrania losowego nicku z danej tabeli i typem
            query = f"SELECT nick FROM {table_name} WHERE typ = %s ORDER BY RAND() LIMIT 1"

            # Wykonanie zapytania
            self.cursor.execute(query, (type_value,))

            # Pobranie wyników
            result = self.cursor.fetchone()

            # Zwrócenie losowego nicku lub None, jeśli nie ma pasujących wyników
            return result[0] if result and result[0] else None
        except Exception as e:
            print(f"Błąd pobierania losowego nicku: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RandomNickApp()
    window.setFixedSize(900, 500)  # Ustaw stały rozmiar okna
    window.show()
    sys.exit(app.exec_())