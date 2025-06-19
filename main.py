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

tablero = chess.Board()
# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ajedrez en Python!")


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

for clave, nombre in Nombres_piezas.items(): #clave = rb, nombre = rey_blanco
    imagen = cargar_imagenes(nombre)
    PIEZAS[clave] = imagen

# Posiciones iniciales de las piezas (pieza, columna, fila)
posiciones_piezas = [
    ("tn", 0, 0), ("cn", 1, 0), ("an", 2, 0), ("dn", 3, 0), ("rn", 4, 0), ("an", 5, 0), ("cn", 6, 0), ("tn", 7, 0),
    *[("pn", i, 1) for i in range(8)],
    *[("pb", i, 6) for i in range(8)],
    ("tb", 0, 7), ("cb", 1, 7), ("ab", 2, 7), ("db", 3, 7), ("rb", 4, 7), ("ab", 5, 7), ("cb", 6, 7), ("tb", 7, 7),
]

# Control de ejecución
running = True

#Variables de control
pieza_seleccionada = None 
celda_seleccionada = None

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

#----------------------------------------------------------------------------------------------------------------------------------
# Bucle principal
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: #fin del while si user cierra el programa 
            running = False

        elif evento.type == pygame.MOUSEBUTTONDOWN: #Detecto si el user hizo click en la ventana del juego
            x, y = pygame.mouse.get_pos() #Obtenemos cordenadas del click para luego identidicar la celda seleccionada
            fila = y // TAM_CELDA
            col = x // TAM_CELDA

            if celda_seleccionada:
                fila_origen, col_origen = celda_seleccionada
                fila_destino, col_destino = fila, col

                #convierto las coord de pygame a las de python-chess
                origen = chess.square(col_origen, 7 - fila_origen)
                destino = chess.square(col_destino, 7 - fila_destino)

                movimiento = chess.Move(origen, destino)

                if movimiento in tablero.legal_moves:
                    tablero.push(movimiento)

                    # Actualizar visualmente la pieza movida
                    for i, (pieza, c, f) in enumerate(posiciones_piezas):
                        if (f, c) == (fila_origen, col_origen):
                            posiciones_piezas[i] = (pieza, col_destino, fila_destino)
                            break
                else:
                    print("Movimiento ilegal")

                celda_seleccionada = None
            else:
                # Selección inicial
                celda_seleccionada = (fila, col)

    dibujar_tablero()
    pygame.display.flip()

pygame.quit()
