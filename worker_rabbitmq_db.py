import pika
import psycopg2
from datetime import datetime

# --- Configuración de RabbitMQ ---
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'tareas'

# --- Configuración de PostgreSQL ---
DB_HOST = 'localhost'
DB_NAME = 'tasksdb'
DB_USER = 'postgres'
DB_PASS = 'postgres'

def guardar_resultado_en_db(tarea, resultado):
    """Guarda el resultado procesado en PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tareas_resultados (tarea_texto, resultado_texto)
            VALUES (%s, %s)
        """, (tarea, resultado))
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB] Resultado guardado en la base: {tarea} -> {resultado}")
    except Exception as e:
        print("[ERROR DB]", e)

def procesar_tarea(ch, method, properties, body):
    tarea = body.decode()
    print(f"[WORKER] Tarea recibida: {tarea}")
    
    # Simulación de procesamiento
    resultado = f"Resultado de '{tarea}' procesado correctamente."
    
    # Guardar en PostgreSQL
    guardar_resultado_en_db(tarea, resultado)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[WORKER] Tarea completada y guardada en BD.\n")

# --- Conexión a RabbitMQ ---
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

print("[WORKER] Esperando tareas...")
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=procesar_tarea)
channel.start_consuming()
