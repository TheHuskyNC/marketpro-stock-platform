# MarketPro

MarketPro is a Flask-based web application that simulates a stock trading platform. Users can register, buy and sell stocks, deposit and withdraw funds, and view their portfolio. Admins have access to tools for creating and managing available stocks. The project is built using Python, Flask, and MySQL.

## How to Run

1. Download or clone the repository.
2. Open a terminal in the project folder.
3. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Set up your MySQL database and credentials in `config.py`.
6. Run the application:
   ```
   python app.py
   ```
7. Open a web browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## File Overview

- `app.py` – Main Flask application entry point
- `user_functions.py` – Handles user trading logic
- `admin_functions.py` – Functions for admin stock creation and management
- `db_connect.py` – Database connection setup
- `price_generator.py` – Random stock price updater
- `test_connection.py` – MySQL connection test script
- `config.py` – Configuration file for database credentials
- `requirements.txt` – List of Python packages used
- `README.md` – This file
- `schema.sql` – SQL script to recreate database and insert sample data
- `templates/` – HTML pages for login, dashboard, buy/sell, etc.

## Features

- User registration and login
- Buy and sell stocks
- View and manage personal portfolio
- Deposit and withdraw funds
- Admin dashboard to create stocks
- Real-time stock price simulation

## Database Setup

This project uses MySQL. To recreate the database structure and sample data:

1. Open MySQL Workbench or your preferred MySQL client.
2. Connect to your MySQL server.
3. Run the contents of `schema.sql`:
   - In MySQL Workbench: Go to File > Open SQL Script, select `schema.sql`, and click the lightning bolt to run it.
   - Or run it from terminal:
     ```
     mysql -u your_username -p < schema.sql
     ```
4. Update `config.py` with your own MySQL username, password, and host settings.

This will create the `stock_trading` database and all required tables with sample data.

## Future Improvements

- Deploy the app online
- Add stock charts and price history
- Implement user notifications
- Improve UI with Bootstrap or another CSS framework

## Author

Corey Saunders  
Arizona State University – Information Technology

