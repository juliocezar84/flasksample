from flask import Flask, request, jsonify, Response
import psycopg2
from psycopg2.extras import RealDictCursor
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Crie uma métrica de exemplo (contador de requisições)
REQUEST_COUNT = Counter('http_requests_total', 'Total de requisições HTTP', ['method', 'endpoint'])

def get_db_connection():
    conn = psycopg2.connect(
        dbname='test_db_hue7', 
        user='test_db_hue7_user', 
        password='Vodg2GUUce4dBWKmTW9ya8eLkq29nHWR', 
        host='dpg-ct0u3j68ii6s73fa9prg-a.oregon-postgres.render.com'
    )
    return conn

# Middleware para contar requisições
@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

# Rota para o Prometheus coletar as métricas
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route('/', methods=['GET'])
def main_rote():
    
    #conn = get_db_connection()
    #cur = conn.cursor()
    
    #cur.execute('CREATE TABLE public.persons (id INT, first_name TEXT, last_name TEXT, email TEXT, gender TEXT);')

    #conn.commit()
    #cur.close()
    #conn.close()


    return "Atualizando meu servidor Flask!"


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
