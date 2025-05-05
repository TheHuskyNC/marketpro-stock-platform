from db_connect import get_db_connection

def create_new_stock(symbol, name, price, volume):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO Stocks (symbol, name, price, volume, opening_price) VALUES (%s, %s, %s, %s, %s);",
        (symbol, name, price, volume, price)
    )
    db.commit()
    db.close()

def view_all_stocks():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT stock_id, symbol, name, price, volume FROM Stocks;")
    stocks = cursor.fetchall()
    db.close()
    return stocks


