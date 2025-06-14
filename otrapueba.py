import pygame
import chess

# Configuración básica
ANCHO_VENTANA = 640
ALTO_VENTANA = 640
FILAS, COLUMNAS = 8, 8
TAM_CELDA = ANCHO_VENTANA // COLUMNAS

# Colores
BLANCO = (245, 245, 245)
GRIS = (125, 135, 150)
AZUL = (50, 130, 200)

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tablero de Ajedrez 8x8")


def cargar_imagenes(nombre_img):
    imagen = pygame.image.load(f"piezas imagenes/{nombre_img}.png").convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
    return imagen_escalada

#diccionario que va a usar cargar_imagenes para cargar y reescalar cada imagen
Nombres_piezas = {
    "rb": "rey_blanco",
    "db": "reina_blanco",
    "ab": "alfil_blanco",
    "tb": "torre_blanco",
    "cb": "caballo_blanco",
    "pb": "peon_blanco",
    "rn": "rey_negro",
    "dn": "reina_negro",
    "an": "alfil_negro",
    "tn": "torre_negro",
    "cn": "caballo_negro",
    "pn": "peon_negro",
}
#diccionario donde se van a cargar como clave la abreviacion de la pieza y como valor la imagen reescalada
PIEZAS = {}

for clave, nombre in Nombres_piezas.items():
    imagen = cargar_imagenes(nombre)
    PIEZAS[clave] = imagen

# Posiciones iniciales de las piezas (pieza, columna, fila)
posiciones_piezas = [
    ("tn", 0, 7), ("cn", 1, 7), ("an", 2, 7), ("dn", 3, 7), ("rn", 4, 7), ("an", 5, 7), ("cn", 6, 7), ("tn", 7, 7), #dn=reina negra
    *[("pn", i, 6) for i in range(8)],
    *[("pb", i, 1) for i in range(8)],
    ("tb", 0, 0), ("cb", 1, 0), ("ab", 2, 0), ("db", 3, 0), ("rb", 4, 0), ("ab", 5, 0), ("cb", 6, 0), ("tb", 7, 0),
]

# Clase para representar movimientos
class Movimiento:
    def __init__(self, inicio, final, pieza_movida, pieza_capturada):
        self.inicioFila = inicio[0]
        self.inicioCol = inicio[1]
        self.finalFila = final[0]
        self.finalCol = final[1]
        self.piezaMovida = pieza_movida
        self.piezaCapturada = pieza_capturada

#imprime donde empieza y termina el mov de una pieza
    def __str__(self):
        return f"{self.piezaMovida} de ({self.inicioFila},{self.inicioCol}) a ({self.finalFila},{self.finalCol})"

# Función para obtener pieza en una celda
def obtener_pieza_en(fila, col):
    for pieza, c, f in posiciones_piezas:
        if f == fila and c == col:
            return pieza
    return None                             # no hay pieza en esa celda

# Función para eliminar pieza en una casilla
def eliminar_pieza_en(fila, col):
    global posiciones_piezas
    posiciones_piezas = [(p, c, f) for (p, c, f) in posiciones_piezas if not (f == fila and c == col)]

# Función para mover pieza de una casilla a otra
def mover_pieza(inicio, final):
    pieza = obtener_pieza_en(*inicio)
    if pieza:
        eliminar_pieza_en(*inicio)
        eliminar_pieza_en(*final)                              # por si hay una pieza enemiga
        posiciones_piezas.append((pieza, final[1], final[0]))  #  (pieza, col, fila)

# Variables de control
running = True
celda_seleccionada = None
clicks_jugador = []
historial_movimientos = []

# Dibujar tablero y piezas
def dibujar_tablero():
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            color = BLANCO if (fila + col) % 2 == 0 else GRIS
            rect = pygame.Rect(col * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
            pygame.draw.rect(ventana, color, rect)

    if celda_seleccionada:
        fila, col = celda_seleccionada
        rect = pygame.Rect(col * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(ventana, AZUL, rect, 4)

    # Dibujar piezas
    for pieza, col, fila in posiciones_piezas:
        if pieza in PIEZAS:
            ventana.blit(PIEZAS[pieza], (col * TAM_CELDA, fila * TAM_CELDA))

# Bucle principal
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            fila = y // TAM_CELDA
            col = x // TAM_CELDA
            celda = (fila, col)

            if celda_seleccionada == celda:     #Si hace doble click a una pieza
                celda_seleccionada = None       #Se borra la seleccion de celda
                clicks_jugador = []             #se reinicia el contador de clicks
            else:
                celda_seleccionada = celda  
                clicks_jugador.append(celda)    #Se guarda la seleccion en el contador de clicks

                if len(clicks_jugador) == 2:        
                    inicio = clicks_jugador[0]              #se hace click en la pieza en su lugar inicial
                    final = clicks_jugador[1]               #se hace click en el lugar donde se quiere mover la pieza
                    pieza_movida = obtener_pieza_en(*inicio)    #guarda la posicion 
                    pieza_capturada = obtener_pieza_en(*final)

                    if pieza_movida:
                        mover_pieza(inicio, final)
                        movimiento = Movimiento(inicio, final, pieza_movida, pieza_capturada)
                        historial_movimientos.append(movimiento)
                        print(movimiento)

                    clicks_jugador = []
                    celda_seleccionada = None

    dibujar_tablero()
    pygame.display.flip()

pygame.quit()
