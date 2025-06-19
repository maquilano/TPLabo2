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
        if evento.type == pygame.QUIT:
            running = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del mouse y convertir a fila y columna del tablero
            x, y = pygame.mouse.get_pos()
            fila = y // TAM_CELDA
            col = x // TAM_CELDA

            # Si ya hay una celda seleccionada (primer clic ya hecho)
            if celda_seleccionada:
                fila_origen, col_origen = celda_seleccionada
                fila_destino, col_destino = fila, col

                # Convertir coordenadas de Pygame a sistema de python-chess
                square_origen = chess.square(col_origen, 7 - fila_origen)
                square_destino = chess.square(col_destino, 7 - fila_destino)

                # Crear un objeto de movimiento de python-chess
                movimiento = chess.Move(square_origen, square_destino)

                # Verificar si el movimiento es legal según las reglas de ajedrez
                if movimiento in tablero.legal_moves:
                    # Aplicar el movimiento en el tablero lógico
                    tablero.push(movimiento)

                    # ----------- ACTUALIZAR LA PARTE VISUAL -----------

                    # Paso 1: eliminar la pieza que haya en la posición destino (si hay una pieza para capturar)
                    nuevas_piezas = []
                    for pieza, c, f in posiciones_piezas:
                        if f == fila_destino and c == col_destino:
                            continue  # Esta pieza es capturada
                        else:
                            nuevas_piezas.append((pieza, c, f))
                    posiciones_piezas = nuevas_piezas

                    # Paso 2: mover la pieza desde origen a destino
                    for i, (pieza, c, f) in enumerate(posiciones_piezas):
                        if f == fila_origen and c == col_origen:
                            posiciones_piezas[i] = (pieza, col_destino, fila_destino)
                            break

                else:
                    print("Movimiento ilegal")

                # Resetear la celda seleccionada
                celda_seleccionada = None

            else:
                # No había celda seleccionada: seleccionamos una pieza
                pieza_en_celda = None
                for pieza, c, f in posiciones_piezas:
                    if f == fila and c == col:
                        pieza_en_celda = pieza
                        break

                if pieza_en_celda:
                    pieza_es_blanca = pieza_en_celda.endswith("b")
                    turno_blancas = tablero.turn == chess.WHITE

                    if (turno_blancas and pieza_es_blanca) or (not turno_blancas and not pieza_es_blanca):
                        celda_seleccionada = (fila, col)
                    else:
                        print("No es tu turno")


    dibujar_tablero()
    pygame.display.flip()

pygame.quit()
