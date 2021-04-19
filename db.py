def get_meter_data(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM meter_data;''')
    rows = cur.fetchall()
    return rows