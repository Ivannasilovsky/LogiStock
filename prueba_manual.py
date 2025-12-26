from inventario import GestorInventario

mi_gestor = GestorInventario()

print("Agregar monitor")
mensaje = mi_gestor.agregar_producto("Monitor 24", "Electronica", 8, 150.00, 5)
print(mensaje)

print("Agregar mouse")
mi_gestor.agregar_producto("Mouse Gamer", "Perifericos", 2, 25.00, 10)

print("Lista completa de productos")
productos = mi_gestor.obtener_productos()
for p in productos:
    print(p)

print("Alertas stock")
alertas = mi_gestor.obtener_alertas()
for a in alertas:
    print(f"Alerta, el producto, {a[1]}, tiene solo {a[3]} unidades.")
