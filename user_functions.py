from db_connect import get_db_connection

def register_user(full_name, username, email, password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match. Please try again."

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = %s OR email = %s;", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        db.close()
        return "Username or Email already exists. Please try again with different credentials."

    cursor.execute(
        "INSERT INTO Users (username, password, full_name, email, cash_balance) VALUES (%s, %s, %s, %s, %s);",
        (username, password, full_name, email, 10000.00)
    )
    db.commit()
    db.close()
    return "Registration successful! Please log in."

def deposit_cash(user_id, amount):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE Users SET cash_balance = cash_balance + %s WHERE user_id = %s;", (amount, user_id))
    db.commit()
    db.close()

def withdraw_cash(user_id, amount):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT cash_balance FROM Users WHERE user_id = %s;", (user_id,))
    balance = cursor.fetchone()[0]
    if amount > balance:
        db.close()
        return False
    else:
        cursor.execute("UPDATE Users SET cash_balance = cash_balance - %s WHERE user_id = %s;", (amount, user_id))
        db.commit()
        db.close()
        return True

def buy_stock(user_id, symbol, quantity):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT stock_id, price, volume FROM Stocks WHERE symbol = %s;", (symbol,))
    stock = cursor.fetchone()
    if not stock:
        db.close()
        return "Stock not found"
    stock_id, price, available_volume = stock
    total_cost = price * quantity
    if quantity > available_volume:
        db.close()
        return "Not enough volume available"
    cursor.execute("SELECT cash_balance FROM Users WHERE user_id = %s;", (user_id,))
    balance = cursor.fetchone()[0]
    if total_cost > balance:
        db.close()
        return "Not enough cash balance"
    new_volume = available_volume - quantity
    new_cash = balance - total_cost
    cursor.execute("UPDATE Stocks SET volume = %s WHERE stock_id = %s;", (new_volume, stock_id))
    cursor.execute("UPDATE Users SET cash_balance = %s WHERE user_id = %s;", (new_cash, user_id))
    cursor.execute(
        "INSERT INTO Transactions (user_id, stock_id, quantity, price_at_time) VALUES (%s, %s, %s, %s);",
        (user_id, stock_id, quantity, price)
    )
    db.commit()
    db.close()
    return "Purchase successful"

def sell_stock(user_id, symbol, quantity):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT stock_id, price, volume FROM Stocks WHERE symbol = %s;", (symbol,))
    stock = cursor.fetchone()
    if not stock:
        db.close()
        return "Stock not found"
    stock_id, price, volume = stock
    cursor.execute("SELECT SUM(quantity) FROM Transactions WHERE user_id = %s AND stock_id = %s;", (user_id, stock_id))
    owned = cursor.fetchone()[0]
    if not owned or quantity > owned:
        db.close()
        return "You don't own enough shares"
    cursor.execute("UPDATE Stocks SET volume = volume + %s WHERE stock_id = %s;", (quantity, stock_id))
    total_sale = price * quantity
    cursor.execute("UPDATE Users SET cash_balance = cash_balance + %s WHERE user_id = %s;", (total_sale, user_id))
    cursor.execute(
        "INSERT INTO Transactions (user_id, stock_id, quantity, price_at_time) VALUES (%s, %s, %s, %s);",
        (user_id, stock_id, -quantity, price)
    )
    db.commit()
    db.close()
    return "Sale successful"

def view_portfolio(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT cash_balance FROM Users WHERE user_id = %s;", (user_id,))
    balance = cursor.fetchone()[0]
    cursor.execute("""
        SELECT s.symbol, s.name, SUM(t.quantity) AS total_shares
        FROM Transactions t
        JOIN Stocks s ON t.stock_id = s.stock_id
        WHERE t.user_id = %s
        GROUP BY s.symbol, s.name;
    """, (user_id,))
    stocks = cursor.fetchall()
    db.close()
    return balance, stocks

def view_transaction_history(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT s.symbol, t.quantity, t.price_at_time, t.timestamp
        FROM Transactions t
        JOIN Stocks s ON t.stock_id = s.stock_id
        WHERE t.user_id = %s
        ORDER BY t.timestamp DESC;
    """, (user_id,))
    transactions = cursor.fetchall()
    db.close()
    return transactions
