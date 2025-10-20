import heapq

class Grafo:
    def __init__(self, dirigido=True):
        self.dirigido = dirigido
        self.grafo = {}

    def agregar_nodo(self, nodo):
        if nodo not in self.grafo:
            self.grafo[nodo] = {}

    def agregar_arista(self, origen, destino, peso):
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.grafo[origen][destino] = peso
        if not self.dirigido:
            self.grafo[destino][origen] = peso

    def mostrar_grafo(self):
        for nodo, conexiones in self.grafo.items():
            print(f"{nodo} -> {conexiones}")

    def dijkstra(self, inicio, fin):
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0
        predecesores = {nodo: None for nodo in self.grafo}
        cola = [(0, inicio)]

        while cola:
            distancia_actual, nodo_actual = heapq.heappop(cola)

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino, peso in self.grafo[nodo_actual].items():
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola, (nueva_distancia, vecino))

        camino = []
        nodo = fin
        while nodo is not None:
            camino.insert(0, nodo)
            nodo = predecesores[nodo]

        return distancias[fin], camino


