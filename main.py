import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import random
import pyqtgraph as pg

def initUI(window, balance, graph_count):
    window.setWindowTitle('Balance Graph')
    window.setGeometry(100, 100, 800, 600)

    # Set dark theme
    window.setStyleSheet("""
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QPushButton {
            background-color: #3c3f41;
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #4c4f51;
        }
        QLabel {
            font-size: 16px;
        }
    """)

    layout = QVBoxLayout()

    balance_label = QLabel(f'Balance: {balance}')
    layout.addWidget(balance_label)

    # Add input boxes for balance change with labels
    input_layout = QHBoxLayout()
    increase_input_label = QLabel('Increase Amount (%):')
    increase_input = QLineEdit()
    increase_input.setPlaceholderText('Enter percentage')
    decrease_input_label = QLabel('Decrease Amount (%):')
    decrease_input = QLineEdit()
    decrease_input.setPlaceholderText('Enter percentage')
    input_layout.addWidget(increase_input_label)
    input_layout.addWidget(increase_input)
    input_layout.addWidget(decrease_input_label)
    input_layout.addWidget(decrease_input)
    layout.addLayout(input_layout)

    graph_layout = QVBoxLayout()
    layout.addLayout(graph_layout)

    button_layout = QHBoxLayout()
    increase_button = QPushButton('Increase Balance')
    decrease_button = QPushButton('Decrease Balance')
    button_layout.addWidget(increase_button)
    button_layout.addWidget(decrease_button)

    layout.addLayout(button_layout)
    window.setLayout(layout)

    # Add pyqtgraph plot
    plot_widget = pg.PlotWidget()
    layout.addWidget(plot_widget)

    return balance_label, graph_layout, increase_button, decrease_button, plot_widget, increase_input, decrease_input

def increase_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, increase_input):
    try:
        percent = float(increase_input.text())
        amount = balance * (percent / 100)
    except ValueError:
        amount = random.randint(50, 150)
    balance += amount
    update_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history)
    return balance

def decrease_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, decrease_input):
    try:
        percent = float(decrease_input.text())
        amount = balance * (percent / 100)
    except ValueError:
        amount = random.randint(50, 150)
    balance -= amount
    update_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history)
    return balance

def update_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history):
    balance_label.setText(f'Balance: {balance}')
    add_graph(balance, plot_widget, balance_history)

def add_graph(balance, plot_widget, balance_history):
    balance_history.append(balance)
    plot_widget.plot(balance_history, pen=pg.mkPen('y', width=2))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    balance = 1000
    graph_count = 0
    balance_history = [balance]

    balance_label, graph_layout, increase_button, decrease_button, plot_widget, increase_input, decrease_input = initUI(window, balance, graph_count)

    def handle_increase():
        global balance
        balance = increase_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, increase_input)

    def handle_decrease():
        global balance
        balance = decrease_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, decrease_input)

    increase_button.clicked.connect(handle_increase)
    decrease_button.clicked.connect(handle_decrease)

    window.show()
    sys.exit(app.exec_())