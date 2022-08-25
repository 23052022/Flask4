from flask import Flask
from flask import request
import sqlite3
import datetime


app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d

def get_data(querry: str) -> object:
    conn = sqlite3.connect('db1.db')
    conn.row_factory = dict_factory
    cursor = conn.execute(querry)
    result = cursor.fetchall()
    conn.close()
    return result

def add_data(querry: str):
    conn = sqlite3.connect('db1.db')
    cursor = conn.cursor()
    cursor.execute(querry)
    conn.commit()
    conn.close()



@app.get('/currency/<currency_UPS>')
def currency_list(currency_UPS):
    res = get_data(f"select * from Currency where currency_name='{currency_UPS}'")
    return res

@app.get('/currency/<currency_UPS>/rating')
def currency_rating(currency_UPS):
    res = get_data(f"select avg(rating) from Rating where cur_name='{currency_UPS}'")
    return res

@app.get('/currency')
def all_currency_rating():
    res = get_data(f"SELECT round(avg(rating), 1), cur_name from rating GROUP by cur_name")
    return res


@app.get('/currency/trade/main:<currency_UPS1>/second:<currency_UPS2>')
def course_ups1_to_ups2(currency_UPS1, currency_UPS2):
    res = get_data(f""" SELECT round(
(SELECT The_cost_is_relative_to_USD from Currency WHERE Data = '11-08-22' and currency_name = 'EUR')/
(SELECT The_cost_is_relative_to_USD from Currency WHERE Data = '11-08-22' and currency_name = 'UAH'), 2))""")
    return res



@app.get('/user/<user_id>')
def login_get(user_id):
    res = get_data(f"select * from User WHERE user_id={user_id};")

    return res


@app.post('/currency/trade/<currrency_UPS1>/<currrency_UPS2>')
def exchange(currrency_UPS1, currrency_UPS2, currrency_name_2=None):
    req = request.json
    date_now = datetime.datetime.now().strftime("%m-%d-%Y")
    amount = req['data']['amount']
    comission = 0.2 * amount
    amount1c = amount + comission
    user_id = 1
    user_balance1 = \
        get_data(f"""SELECT balance FROM Account Where user_id = '{user_id}' and currency_name = '{currrency_UPS1}'""")
    user_balance2 = \
        get_data(f"""SELECT * From Currency Where currency_name = '{currrency_UPS1}' ORDER by date DESC limit 1""")

    cur1_USD_relative_value = \
        get_data(f"Select USD_relative_value From Currency Where name='{currrency_name_1}' And date='{date_now}'")[0][0]
    cur2_USD_relative_value = \
        get_data(f"Select USD_relative_value From Currency Where name='{currrency_name_2}' And date='{date_now}'")[0][0]
    print(f"aaa{user_balance1}")
    need_cur2 = amount * cur1_USD_relative_value / cur2_USD_relative_value
    print(f"bbb{need_cur2}")
    existing_amount_currency1 = \
        get_data(f"Select available_quantity From Currency Where name='{currrency_name_1}' And date'{date_now}'")[0][0]
    existing_amount_currency2 = \
        get_data(f"Select available_quantity From Currency Where name='{currrency_name_2}' And date'{date_now}'")[0][0]

   if (user_balance1 >= amount) and existing_amount_currency2 > need_cur2):
       get_data(
           f"UPDATE Currency SET available_quantity={existing_amount_currency2 - need_cur2} WHERE name='{currrency_name_2}'And date'{date_now}'")[0][0]
        get_data(
           f"UPDATE Currency SET available_quantity={existing_amount_currency1 - amount1c} WHERE name='{currrency_name_1}'And date'{date_now}'")[0][0]

        get_data(
            f"UPDATA Account SET balance={user_balance1 - amount} WERE user_id='{user_id}' AND currency_name='{currency_name1}'")
        get_data(
            f"UPDATA Account SET balance={user_balance2 + need_cur2} WERE user_id='{user_id}' AND currency_name='{currency_name2}'")

       get_data(
           f"""INSERT INTO "Transaction"(user_id_initial, operation_type, currency_num_spent, currency_num_obtained, currency_name
"""
       )


        return 'ok'
    else:
        return 'not ok'



@app.post('/currency/<name>/review')
def currency_review_post(name):
    req = request.json
    cur_name = req['data']['currency_name']
    rating = req['data']['rating']
    comment = req['data']['comment']
    add_data(f"""INSERT INTO Rating(currency_name, rating, comment) VALUES('{cur_name}', {rating}, '{comment}');""")
    return 'OK'


@app.put('/currency/<name>/review')
def currency_review_put(name):
    return f'Review currency {name}, PUT method'


@app.delete('/currency/<name>/review')
def currency_review_gelete(name):
    return f'Review currency {name}, DELETE method'

@app.get('/currencies')
def amount_of_currency_available():
    res = get_data("SELECT currency_name, available_quantity FROM Currency WHERE date = '11-08-22'")
    return res

@app.get('/user')
def user_balance():
    res = get_data(f"SELECT balance, currency_name FROM Account WHERE user_id = 2")
    return res

@app.post('/user/transfer')
def transfer():
   pass


@app.get('/user/history')
def user_history():
    res = get_data("""SELECT user_id, type_of_transaction, amount_of_currency, currency_with_which_the_transaction, 
    currency_in_which_the_transaction, data_time,amount_of_currency_received, commission, 
    account_from_which_the_transaction, account_on_which_the_transaction FROM Transaction_history WHERE user_id=1""")
    return res


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
