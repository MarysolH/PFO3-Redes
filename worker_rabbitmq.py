import pika
import time

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Crear cola si no existe
channel.queue_declare(queue='tareas')

print("[WORKER] Esperando tareas...")

def procesar_tarea(ch, method, properties, body):
    tarea = body.decode()
    print(f"[WORKER] Tarea recibida: {tarea}")
    # Simula trabajo pesado
    time.sleep(2)
    print(f"[WORKER] Tarea completada: {tarea}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Escuchar la cola
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='tareas', on_message_callback=procesar_tarea)

channel.start_consuming()
