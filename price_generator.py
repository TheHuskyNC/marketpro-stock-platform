import random
from db_connect import get_db_connection

def update_stock_prices():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT stock_id, price FROM Stocks;")
    stocks = cursor.fetchall()
    
    for stock in stocks:
        stock_id = stock[0]
        current_price = float(stock[1])
        change_percent = random.uniform(-0.03, 0.03)
        new_price = round(current_price * (1 + change_percent), 2)
        cursor.execute(
            "UPDATE Stocks SET price = %s WHERE stock_id = %s;",
            (new_price, stock_id)
        )
    
    db.commit()
    db.close()
    print("Stock prices updated!")

if __name__ == "__main__":
    update_stock_prices()
