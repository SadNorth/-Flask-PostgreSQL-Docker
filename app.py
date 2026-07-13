import os
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='db', # Имя сервиса БД в docker-compose
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f'<h1>Подключение к PostgresSQL успешно!</h1><p>Версия: {version}</p>'
    except Exception as e:
        return f'<h1>Ошибка подключения к PostgresSQL</h1><p>{str(e)}</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)