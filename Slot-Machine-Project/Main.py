import random
import tkinter as tk
from tkinter import messagebox

MAX_LINES = 3
MAX_BET = 10000
MIN_BET = 100

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def update_slot_machine_display(columns):
    for row in range(len(columns[0])):
        row_display = " | ".join([column[row] for column in columns])
        slot_labels[row].config(text=row_display)


def deposit():
    try:
        amount = int(deposit_entry.get())
        if amount > 0:
            return amount
        else:
            messagebox.showwarning("Invalid Input", "Amount must be greater than 0.")
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a number.")


def get_number_of_lines():
    try:
        lines = int(lines_entry.get())
        if 1 <= lines <= MAX_LINES:
            return lines
        else:
            messagebox.showwarning("Invalid Input", f"Enter a valid number of lines (1-{MAX_LINES}).")
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a number.")


def get_bet():
    try:
        amount = int(bet_entry.get())
        if MIN_BET >= amount <= MAX_BET:
            return amount
        else:
            messagebox.showwarning("Invalid Input", f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a number.")


def spin():
    global balance
    lines = get_number_of_lines()
    if lines is None:
        return

    bet = get_bet()
    if bet is None:
        return

    total_bet = bet * lines

    if total_bet > balance:
        messagebox.showwarning("Insufficient Balance",
                               f"You do not have enough to bet that amount, your current balance is: ${balance}")
        return

    balance -= total_bet

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    update_slot_machine_display(slots)

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    balance += winnings
    balance_label.config(text=f"Current balance: ${balance}")
    result_label.config(text=f"You won ${winnings}. You won on lines: {', '.join(map(str, winning_lines))}")


def start_game():
    global balance
    balance = deposit()
    if balance is not None:
        balance_label.config(text=f"Current balance: ${balance}")
        spin_button.config(state=tk.NORMAL)


# Create the main window
window = tk.Tk()
window.title("Slot Machine Game")

# Balance and Deposit Section
balance_label = tk.Label(window, text="Current balance: $0", font=("Arial", 14))
balance_label.pack()

deposit_label = tk.Label(window, text="Enter deposit amount:", font=("Arial", 12))
deposit_label.pack()

deposit_entry = tk.Entry(window)
deposit_entry.pack()

deposit_button = tk.Button(window, text="Deposit", command=start_game)
deposit_button.pack()

# Number of Lines Section
lines_label = tk.Label(window, text="Enter number of lines to bet on (1-3):", font=("Arial", 12))
lines_label.pack()

lines_entry = tk.Entry(window)
lines_entry.pack()

# Bet Amount Section
bet_label = tk.Label(window, text="Enter bet amount per line:", font=("Arial", 12))
bet_label.pack()

bet_entry = tk.Entry(window)
bet_entry.pack()

# Slot Machine Display
slot_frame = tk.Frame(window)
slot_frame.pack()

slot_labels = [tk.Label(slot_frame, text="", font=("Arial", 18)) for _ in range(ROWS)]
for slot_label in slot_labels:
    slot_label.pack()

# Result Display
result_label = tk.Label(window, text="", font=("Arial", 14))
result_label.pack()

# Spin Button
spin_button = tk.Button(window, text="Spin", state=tk.DISABLED, command=spin)
spin_button.pack()

# Start the GUI main loop
window.mainloop()
