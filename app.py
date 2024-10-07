from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname='teste_qthi', 
        user='teste', 
        password='YzxANlVWAXnecF1eARNWVuPd0gwVgOFb', 
        host='dpg-crmpgj5umphs739ipld0-a'
    )
    return conn


@app.route('/', methods=['POST'])
def main_rote():
    return "Meu backend da aula de DevOps!"


@app.route('/persons', methods=['POST'])
def create_person():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO public.persons (id, first_name, last_name, email, gender) VALUES (%s,%s, %s, %s, %s)',
                (data['id'], data['first_name'], data['last_name'], data['email'], data['gender']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(data), 201

@app.route('/persons', methods=['GET'])
def get_persons():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM public.persons')
    persons = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(persons)

@app.route('/persons/<int:id>', methods=['GET'])
def get_person(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM public.persons WHERE id = %s', (id,))
    person = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(person), 200

@app.route('/persons/<int:id>', methods=['PUT'])
def update_person(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE public.persons SET first_name = %s, last_name = %s, email = %s, gender = %s WHERE id = %s',
        (data['first_name'], data['last_name'], data['email'], data['gender'], id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(data), 200

@app.route('/persons/<int:id>', methods=['DELETE'])
def delete_person(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM public.persons WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
