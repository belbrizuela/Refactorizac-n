class Mapa:
    """Inicializo mis atributos de instancia"""
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [['.' for _ in range(columnas)] for _ in range(filas)]

    def agregar_obstaculos(self, posiciones): # Agrego mis obstaculos verificando que esten dentro de las coordenadas de mi mapa
        for fila, columna in posiciones:
            if 0 <= fila < self.filas and 0 <= columna < self.columnas:
                self.matriz[fila][columna] = 'O'

    def quitar_obstaculo(self, fila, columna): # quito los obstaculos
        if 0 <= fila < self.filas and 0 <= columna < self.columnas and self.matriz[fila][columna] == 'O':
            self.matriz[fila][columna] = '.'

    def agregar_entrada_salida(self, entrada, salida):
        if 0 <= entrada[0] < self.filas and 0 <= entrada[1] < self.columnas:
            self.matriz[entrada[0]][entrada[1]] = 'E'
        if 0 <= salida[0] < self.filas and 0 <= salida[1] < self.columnas:
            self.matriz[salida[0]][salida[1]] = 'S'

    def mostrar_matriz(self): #imprimo mi matriz y hago que haga un salto de linea con join
        for fila in self.matriz:
            print(" ".join(fila))
        print()

class AStarAlgoritmo:
    def __init__(self, mapa): # Inicializo mi mapa con mi atributo
        self.mapa = mapa

    def heuristica(self, posicion_actual, salida): #creo mi funcion heuristica para que me haga el calculo absoluto
        return abs(posicion_actual[0] - salida[0]) + abs(posicion_actual[1] - salida[1])

    def encontrar_vecinos(self, nodo): # Busco y actualizo a mis vecinos
        x, y = nodo
        vecinos = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.mapa.filas and 0 <= ny < self.mapa.columnas and self.mapa.matriz[nx][ny] != 'O':
                vecinos.append((nx, ny))
        return vecinos

    def reconstruir_camino(self, de_donde_viene, inicio, meta): #Reconstruyo mi camino con reverse para que se invierta las coordenadas
        actual = meta
        camino = [actual]
        while actual != inicio:
            actual = de_donde_viene[actual]
            camino.append(actual)
        camino.reverse()
        return camino

    def a_star(self, entrada, salida):
        conjunto_abierto = {entrada}
        de_donde_viene = {}
        # Defino mis costos actualies y totales para llamar a mi funcion heristica
        g_score = {entrada: 0}
        f_score = {entrada: self.heuristica(entrada, salida)}

        while conjunto_abierto: 
            actual = min(conjunto_abierto, key=lambda x: f_score.get(x, float('inf')))
            if actual == salida: # Si llegue a la salida, que se reconstruya mi camino
                return self.reconstruir_camino(de_donde_viene, entrada, salida)

            conjunto_abierto.remove(actual) # si no, que se almacene en mi conjunto abierto como posicion ya visitada
            for vecino in self.encontrar_vecinos(actual): # y que siga iterando para seguir buscando
                puntaje_g_tentativo = g_score[actual] + 1
                #si mi puntaje tentativo es manyor a la actual, que se actualice
                if puntaje_g_tentativo < g_score.get(vecino, float('inf')):
                    de_donde_viene[vecino] = actual
                    g_score[vecino] = puntaje_g_tentativo
                    f_score[vecino] = g_score[vecino] + self.heuristica(vecino, salida)
                    # si no, que se almacene en mi conjunto abierto, como vecino ya visitado
                    if vecino not in conjunto_abierto:
                        conjunto_abierto.add(vecino)

        return []  # Retorna una lista vacía si no se encuentra un camino

def obtener_obstaculos(): 
    posiciones = []
    while True:
        entrada = input("Por favor ingrese la posición del obstáculo 'fila,columna' o 's' para terminar: ")
        if entrada.lower() == 's':
            break
        try:
            fila, columna = map(int, entrada.split(','))
            posiciones.append((fila, columna))
        except ValueError:
            print("Entrada no válida. Por favor, ingrese de nuevo en el formato 'fila,columna'.")
    return posiciones

def obtener_coordenada(tipo):
    while True:
        entrada = input(f"Ingrese la posición de la {tipo} en el formato 'fila,columna': ")
        try:
            fila, columna = map(int, entrada.split(','))
            return (fila, columna)
        except ValueError:
            print("Entrada no válida. Por favor, ingrese de nuevo en el formato 'fila,columna'.")

def quitar_obstaculo(mapa):
    while True:
        entrada = input("Ingrese la posición del obstáculo a quitar en el formato 'fila,columna' o 's' para salir: ")
        if entrada.lower() == 's':
            break
        try:
            fila, columna = map(int, entrada.split(','))
            mapa.quitar_obstaculo(fila, columna)
            print("Obstáculo eliminado.")
            mapa.mostrar_matriz()
        except ValueError:
            print("Entrada no válida. Por favor, ingrese de nuevo en el formato 'fila,columna'.")

def main(): # Inicializo mi funcion principal con los valores ya obtenidos 

    filas, columnas = 5, 5  # Tamaño de la matriz
    mapa = Mapa(filas, columnas)
    mapa.mostrar_matriz()
    
    print("Ingrese las posiciones de los obstáculos.")
    posiciones_obstaculos = obtener_obstaculos()
    mapa.agregar_obstaculos(posiciones_obstaculos)
    
    entrada = obtener_coordenada("entrada")
    salida = obtener_coordenada("salida")
    mapa.agregar_entrada_salida(entrada, salida)
    
    mapa.mostrar_matriz()
    
    while True:
        opcion = input("¿Desea eliminar algún obstáculo? (s/n): ")
        if opcion.lower() == 's':
            quitar_obstaculo(mapa)
        else:
            break
    
    #llamo a mi algoritmo para que me imprima en coordenadas la distancia total obtenida con mi funcion heuristica
    algoritmo_astar = AStarAlgoritmo(mapa)
    print(f"Distancia heurística desde la entrada hasta la salida: {algoritmo_astar.heuristica(entrada, salida)}")
    
    #imprimo mi recorrido obtenido en coordenadas
    camino = algoritmo_astar.a_star(entrada, salida)
    if camino:
        print("Recorrido:")
        for paso in camino:
            print(paso)
        for (f, c) in camino:
            if mapa.matriz[f][c] not in ['E', 'S']:
                mapa.matriz[f][c] = '*'
    else:
        print("No se encontró un camino.")

    mapa.mostrar_matriz()

if __name__ == "__main__":
    main()
