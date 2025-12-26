import psycopg2

DB_CONFIG = {
    "dbname": "logistock_db",
    "user": "postgres",
    "password": "Ivcamir04",
    "host": "localhost",
    "port": "5432"
}

def probar_conexion():
    conexion = None 
    try:
        print("Conenctando a PostgreSQL...")
        conexion = psycopg2.connect(**DB_CONFIG)#desempaqueto para usar los argumentos de manerea individual

        cursor = conexion.cursor()#el que ma va a buscar los datos

        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        
        print("Conectado existosamente")
        print(f"Estas conectado a: {version[0]}")
    
    except Exception as e:
        print("Error de conexion:")
        print(repr(e))
        print("Recomendacion: Verificar tu contraseña y que el servidor de Postgres esté abierto.")        
    
    finally:
        if conexion is not None:
            conexion.close()
            print("Conexion Cerrada.")
            
if __name__ == "__main__":
    probar_conexion()