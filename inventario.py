import psycopg2
from database import DB_CONFIG

class GestorInventario:
    def __init__(self):
        pass

    def _conectar(self):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except Exception as e:
            print(f"Error al conectar: {e}")
            return None
    
    def agregar_producto(self, nombre, categoria, cantidad, precio, stock_minimo):
        
        if int(cantidad) < 0:
            return "Error la cantidad no puede ser negetiva."
        
        conn = self._conectar()    
        if not conn:
            return "Error a la hora de conectar la base de datos."
        
        try:
            cursor = conn.cursor()
            
            # Usamos %s como 'marcadores' de seguridad (evita hackeos SQL Injection)
            query = """
                INSERT INTO productos (nombre, categoria, cantidad, precio, stock_minimo)
                VALUES (%s, %s, %s, %s, %s)
                """
            cursor.execute(query, (nombre, categoria, cantidad, precio, stock_minimo))
                
            conn.commit()
            return "Producto guardado correctamente."    
        
        except Exception as e:    
            conn.rollback #deshacer cambios en caso de fallo  
            return f"Error al guardar en bade de datos: {e}"
        
        finally:
            conn.close()  
    
    def obtener_productos(self):
        conn = self._conectar()
        
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM productos ORDER BY id ASC")
            resultados = cursor.fetchall() #trae todo
            return resultados
        except Exception as E:
            print(f"Error al leer los datos: {e}")
            return []
        finally:
            conn.close() 
    
    def obtener_alertas(self):
        conn = self._conectar()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM productos WHERE cantidad < stock_minimo ")   
            return cursor.fetchall()
        finally:
            conn.close()
            
    def eliminar_producto(self, id_producto):        
        conn = self._conectar()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            query = "DELETE FROM productos WHERE id = %s"
            cursor.execute(query, (id_producto,)) 
            
            conn.commit()# ¡OBLIGATORIO para guardar cambios (Insert, Update, Delete)!
            
        except Exception as e:
            conn.rollback()
            return f"Error al eliminar el producto: {e}"
        finally:
            conn.close()
    
    def actualizar_stock(self, id_producto, cantidad_cambio):
        conn = self._conectar()
        if not conn:
            return "Error de conexion."
        
        try:
            cursor = conn.cursor()
            query = "SELECT cantidad FROM productos WHERE id = %s"
            
            cursor.execute(query, (id_producto,))
            resultado = cursor.fetchone() #trae una sola fila
            
            if not resultado:
                  return "Producto no encontrado."

            stock_actual = resultado[0]
            nuevo_stock = stock_actual + cantidad_cambio
            
            if nuevo_stock < 0:
                return f"Error: No puedes restar {abs(cambio_cambio)}. Stock actual: {stock_actual}"
            
            query = "UPDATE productos SET cantidad = %s WHERE id = %s"
            cursor.execute(query, (nuevo_stock, id_producto))
            conn.commit()

            return f"Stock actualizado. Nuevo total: {nuevo_stock}"
        
        except Exception as e:
            conn.rollback()
            return f"Error al actualizar: {e}"
        finally:
            conn.close()
    
    def modificar_producto(self, id_prod, nueva_cat, nuevo_precio, nuevo_min):
        conn = self._conectar()
        if not conn:
            return "Error de conexión."

        try:
            cursor = conn.cursor()
            
            # SQL: UPDATE campos SET valor = nuevo_valor WHERE id = producto_elegido
            query = """UPDATE productos 
                       SET categoria = %s, precio = %s, stock_minimo = %s 
                       WHERE id = %s"""
            
            cursor.execute(query, (nueva_cat, nuevo_precio, nuevo_min, id_prod))
            conn.commit()
            
            return "Producto modificado correctamente."

        except Exception as e:
            conn.rollback()
            return f"Error al modificar: {e}"
        finally:
            conn.close()
            
