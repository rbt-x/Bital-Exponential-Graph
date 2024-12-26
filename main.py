import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit, QShortcut
from PyQt5.QtGui import QPalette, QColor, QKeySequence, QIcon  # Add this import
from PyQt5.QtCore import Qt, QTimer
import random
import pyqtgraph as pg

def initUI(window, balance, graph_count):
    window.setWindowTitle('Bital Exponential Graph')
    window.setGeometry(100, 100, 800, 600)
    window.setWindowFlags(Qt.FramelessWindowHint)  # Hide the window bar

    # Center the window on the screen
    screen = QApplication.primaryScreen().availableGeometry()
    window.setGeometry(
        (screen.width() - window.width()) // 2,
        (screen.height() - window.height()) // 2,
        window.width(),
        window.height()
    )

    # Set glass theme
    window.setAttribute(Qt.WA_TranslucentBackground)
    window.setStyleSheet("""
        QWidget {
            background: rgba(30, 30, 30, 0.95);
            color: #ffffff;
        }
        QPushButton {
            background-color: rgba(60, 63, 65, 0.95);
            border: 1px solid #555555;
            padding: 10px;
            border-radius: 10px;
            font-family: 'Digital-7', monospace;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: rgba(76, 79, 81, 0.95);
        }
        QLineEdit {
            background-color: rgba(43, 43, 43, 0.95);
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 10px;
            font-family: 'Digital-7', monospace;
            font-size: 14px;
            color: #ffffff;
        }
        QLabel {
            background-color: rgba(30, 30, 30, 0.8);
            padding: 5px;
            border-radius: 5px;
            font-size: 16px;
            font-family: 'Digital-7', monospace;
        }
        QLabel#help-text {
            color: #00ff00;  # Ensure this line sets the help text color to green
            font-family: 'Digital-7', monospace;
            font-size: 12px;
            text-align: center;
        }
    """)

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)  # Center the content

    # Custom title bar
    title_bar = QHBoxLayout()
    title_label = QLabel('Bital Exponential Graph')
    title_label.setStyleSheet("font-size: 18px; font-family: 'Digital-7', monospace;")
    title_label.setAlignment(Qt.AlignCenter)
    close_button = QPushButton('X')
    close_button.setFixedSize(30, 30)
    close_button.clicked.connect(window.close)
    title_bar.addWidget(title_label)
    title_bar.addStretch()
    title_bar.addWidget(close_button)
    layout.addLayout(title_bar)

    # Add input field for start balance
    start_balance_label = QLabel('Start Balance:')
    start_balance_input = QLineEdit()
    start_balance_input.setPlaceholderText('Enter start balance')
    layout.addWidget(start_balance_label)
    layout.addWidget(start_balance_input)

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

    # Add labels for statistics in one line
    statistics_layout = QHBoxLayout()
    max_drawdown_label = QLabel('Max Drawdown: 0')
    total_trades_label = QLabel('Total Trades: 0')
    total_wins_label = QLabel('Total Wins: 0')
    total_losses_label = QLabel('Total Losses: 0')
    statistics_layout.addWidget(max_drawdown_label, alignment=Qt.AlignCenter)
    statistics_layout.addWidget(total_trades_label, alignment=Qt.AlignCenter)
    statistics_layout.addWidget(total_wins_label, alignment=Qt.AlignCenter)
    statistics_layout.addWidget(total_losses_label, alignment=Qt.AlignCenter)
    layout.addLayout(statistics_layout)

    graph_layout = QVBoxLayout()
    layout.addLayout(graph_layout)

    button_layout = QHBoxLayout()
    increase_button = QPushButton('Increase Balance')
    decrease_button = QPushButton('Decrease Balance')
    back_button = QPushButton('Back')
    button_layout.addWidget(increase_button)
    button_layout.addWidget(decrease_button)
    button_layout.addWidget(back_button)

    layout.addLayout(button_layout)
    window.setLayout(layout)

    # Add pyqtgraph plot
    plot_widget = pg.PlotWidget()
    layout.addWidget(plot_widget)

    # Add shortcut for restarting the application
    restart_shortcut = QShortcut(QKeySequence("Ctrl+R"), window)
    restart_shortcut.activated.connect(lambda: restart_app(window))

    # Add shortcut keys for buttons
    QShortcut(QKeySequence("Space"), window).activated.connect(lambda: decrease_button.click())
    QShortcut(QKeySequence("Return"), window).activated.connect(lambda: increase_button.click())
    QShortcut(QKeySequence("Escape"), window).activated.connect(lambda: window.close())
    QShortcut(QKeySequence("Backspace"), window).activated.connect(lambda: back_button.click())

    # Add moving description line for help
    help_text = QLabel("Press[ 'space' to Decrease   /  'Enter' to Increase   /   'Backspace' to back    /   'Esc' to Close ] " )
    help_text.setObjectName("help-text")
    help_text.setAlignment(Qt.AlignCenter)
    layout.addWidget(help_text)

    def move_help_text():
        current_text = help_text.text()
        help_text.setText(current_text[1:] + current_text[0])

    timer = QTimer()
    timer.timeout.connect(move_help_text)
    timer.start(200)

    # Enable window dragging
    def mousePressEvent(event):
        if event.button() == Qt.LeftButton:
            window.dragPos = event.globalPos()

    def mouseMoveEvent(event):
        if event.buttons() == Qt.LeftButton:
            window.move(window.pos() + event.globalPos() - window.dragPos)
            window.dragPos = event.globalPos()
            event.accept()

    window.mousePressEvent = mousePressEvent
    window.mouseMoveEvent = mouseMoveEvent

    return balance_label, graph_layout, increase_button, decrease_button, back_button, plot_widget, increase_input, decrease_input, start_balance_input, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label

def increase_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, increase_input):
    try:
        percent = float(increase_input.text())
        amount = balance * (percent / 100)
    except ValueError:
        amount = random.randint(50, 150)
    balance += amount
    balance_history.append(balance)
    return balance

def decrease_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, decrease_input):
    try:
        percent = float(decrease_input.text())
        amount = balance * (percent / 100)
    except ValueError:
        amount = random.randint(50, 150)
    balance -= amount
    balance_history.append(balance)
    return balance

def back_balance(balance_history):
    if len(balance_history) > 1:
        balance_history.pop()
    return balance_history[-1]

def update_statistics(balance_history, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label):
    max_drawdown = 0
    peak = balance_history[0]
    for balance in balance_history:
        if balance > peak:
            peak = balance
        drawdown = peak - balance
        if drawdown > max_drawdown:
            max_drawdown = drawdown

    total_trades = len(balance_history) - 1
    total_wins = sum(1 for i in range(1, len(balance_history)) if balance_history[i] > balance_history[i-1])
    total_losses = total_trades - total_wins

    max_drawdown_label.setText(f'Max Drawdown: {max_drawdown:.2f}')
    total_trades_label.setText(f'Total Trades: {total_trades}')
    total_wins_label.setText(f'Total Wins: {total_wins}')
    total_losses_label.setText(f'Total Losses: {total_losses}')

def update_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label):
    balance_label.setText(f'Balance: {balance:.2f}')
    add_graph(balance, plot_widget, balance_history)
    update_statistics(balance_history, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label)

def add_graph(balance, plot_widget, balance_history):
    plot_widget.clear()  # Clear the previous plot
    plot_widget.plot(balance_history, pen=pg.mkPen('y', width=2))

def restart_app(window):
    window.close()
    QApplication.quit()
    status = QApplication.exec_()
    sys.exit(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    balance = 1000
    graph_count = 0
    balance_history = [balance]

    balance_label, graph_layout, increase_button, decrease_button, back_button, plot_widget, increase_input, decrease_input, start_balance_input, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label = initUI(window, balance, graph_count)

    def handle_increase():
        global balance
        balance = increase_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, increase_input)
        update_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label)

    def handle_decrease():
        global balance
        balance = decrease_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, decrease_input)
        update_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label)

    def handle_back():
        global balance
        balance = back_balance(balance_history)
        update_balance(balance, balance_label, graph_layout, graph_count, plot_widget, balance_history, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label)

    def set_start_balance():
        global balance
        try:
            balance = float(start_balance_input.text())
        except ValueError:
            balance = 1000
        balance_label.setText(f'Balance: {balance}')
        balance_history.clear()
        balance_history.append(balance)
        plot_widget.clear()
        add_graph(balance, plot_widget, balance_history)
        update_statistics(balance_history, max_drawdown_label, total_trades_label, total_wins_label, total_losses_label)

    start_balance_input.editingFinished.connect(set_start_balance)
    increase_button.clicked.connect(handle_increase)
    decrease_button.clicked.connect(handle_decrease)
    back_button.clicked.connect(handle_back)

    window.show()
    sys.exit(app.exec_())