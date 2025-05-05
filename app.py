from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_functions import register_user, deposit_cash, withdraw_cash, buy_stock, sell_stock, view_portfolio
from admin_functions import create_new_stock, view_all_stocks
from db_connect import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT symbol, name, price, volume, opening_price FROM Stocks;")
    stocks = cursor.fetchall()
    db.close()
    return render_template('index.html', stocks=stocks)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        message = register_user(full_name, username, email, password, confirm_password)
        flash(message, 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT password FROM Users WHERE username = %s;", (username,))
        result = cursor.fetchone()
        if result and result[0] == password:
            session['username'] = username
            db.close()
            return redirect(url_for('profile'))
        else:
            db.close()
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT full_name, email, cash_balance FROM Users WHERE username = %s;", (username,))
    user_info = cursor.fetchone()
    db.close()
    if user_info:
        full_name, email, balance = user_info
        return render_template('profile.html', username=username, full_name=full_name, email=email, balance=balance)
    else:
        session.pop('username', None)
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))

@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT user_id, cash_balance FROM Users WHERE username = %s;", (username,))
    user_result = cursor.fetchone()
    if not user_result:
        db.close()
        session.pop('username', None)
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    user_id, balance = user_result
    if request.method == 'POST':
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        cursor.execute("SELECT stock_id, price, volume FROM Stocks WHERE symbol = %s;", (symbol,))
        stock_result = cursor.fetchone()
        if not stock_result:
            db.close()
            flash('Stock not found.', 'danger')
            return redirect(url_for('buy'))
        stock_id, price, volume = stock_result
        total_price = price * quantity
        if total_price > balance:
            db.close()
            flash('Insufficient balance to buy stock.', 'danger')
            return redirect(url_for('buy'))
        message = buy_stock(user_id, symbol, quantity)
        db.close()
        return render_template('purchase_success.html')
    cursor.execute("SELECT symbol, name, price FROM Stocks;")
    stocks = cursor.fetchall()
    db.close()
    return render_template('buy.html', stocks=stocks)

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM Users WHERE username = %s;", (username,))
    user_result = cursor.fetchone()
    if not user_result:
        db.close()
        session.pop('username', None)
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    user_id = user_result[0]
    if request.method == 'POST':
        symbol = request.form['symbol']
        quantity = int(request.form['quantity'])
        message = sell_stock(user_id, symbol, quantity)
        db.close()
        return render_template('sale_success.html')
    cursor.execute("""
        SELECT s.symbol, s.name
        FROM Transactions t
        JOIN Stocks s ON t.stock_id = s.stock_id
        WHERE t.user_id = %s
        GROUP BY s.symbol, s.name
        HAVING SUM(t.quantity) > 0;
    """, (user_id,))
    owned_stocks = cursor.fetchall()
    db.close()
    return render_template('sell.html', owned_stocks=owned_stocks)

@app.route('/portfolio')
def portfolio():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM Users WHERE username = %s;", (username,))
    user_result = cursor.fetchone()
    if user_result:
        user_id = user_result[0]
        cursor.execute("""
            SELECT s.symbol, SUM(t.quantity) AS total_quantity, s.price
            FROM Transactions t
            JOIN Stocks s ON t.stock_id = s.stock_id
            WHERE t.user_id = %s
            GROUP BY s.symbol, s.price;
        """, (user_id,))
        rows = cursor.fetchall()
        db.close()
        portfolio = []
        for row in rows:
            symbol = row[0]
            quantity = float(row[1])
            price = float(row[2])
            total_value = round(price * quantity, 2)
            portfolio.append({
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'total_value': total_value
            })
        return render_template('portfolio.html', portfolio=portfolio)
    else:
        db.close()
        session.pop('username', None)
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM Users WHERE username = %s;", (username,))
    user_result = cursor.fetchone()
    if not user_result:
        db.close()
        session.pop('username', None)
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    user_id = user_result[0]
    if request.method == 'POST':
        amount = float(request.form['amount'])
        message = deposit_cash(user_id, amount)
        db.close()
        flash('Deposit successful!', 'success')
        return redirect(url_for('profile'))
    db.close()
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM Users WHERE username = %s;", (username,))
    user_result = cursor.fetchone()
    if not user_result:
        db.close()
        session.pop('username', None)
        flash('User not found. Please login again.', 'danger')
        return redirect(url_for('login'))
    user_id = user_result[0]
    if request.method == 'POST':
        amount = float(request.form['amount'])
        message = withdraw_cash(user_id, amount)
        db.close()
        flash('Withdrawal successful!', 'success')
        return redirect(url_for('profile'))
    db.close()
    return render_template('withdraw.html')

@app.route('/create-stock', methods=['GET', 'POST'])
def create_stock():
    if 'username' not in session:
        flash('You must be logged in.', 'danger')
        return redirect(url_for('login'))

    if session['username'] != 'coreys':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        symbol = request.form['symbol']
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        volume = int(request.form['volume'])

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Stocks (symbol, name, price, opening_price, volume) VALUES (%s, %s, %s, %s, %s);",
            (symbol, name, price, price, volume)
        )
        db.commit()
        db.close()

        flash('New stock created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('create-stock.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
