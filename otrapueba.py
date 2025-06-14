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
'''
# Cargar imágenes de las piezas
rey_blanco = pygame.image.load('piezas imagenes/rey_blanco.png').convert_alpha()
rey_blanco = pygame.transform.scale(rey_blanco, (TAM_CELDA, TAM_CELDA))
reina_blanca = pygame.image.load('piezas imagenes/reina_blanco.png').convert_alpha()
reina_blanca = pygame.transform.scale(reina_blanca, (TAM_CELDA, TAM_CELDA))
alfil_blanco = pygame.image.load('piezas imagenes/alfil_blanco.png').convert_alpha()
alfil_blanco = pygame.transform.scale(alfil_blanco, (TAM_CELDA, TAM_CELDA))
torre_blanca = pygame.image.load('piezas imagenes/torre_blanco.png').convert_alpha()
torre_blanca = pygame.transform.scale(torre_blanca, (TAM_CELDA, TAM_CELDA))
caballo_blanco = pygame.image.load('piezas imagenes/caballo_blanco.png').convert_alpha()
caballo_blanco = pygame.transform.scale(caballo_blanco, (TAM_CELDA, TAM_CELDA))
peon_blanco = pygame.image.load('piezas imagenes/peon_blanco.png').convert_alpha()
peon_blanco = pygame.transform.scale(peon_blanco, (TAM_CELDA, TAM_CELDA))

rey_negro = pygame.image.load('piezas imagenes/rey_negro.png').convert_alpha()
rey_negro = pygame.transform.scale(rey_negro, (TAM_CELDA, TAM_CELDA))
reina_negra = pygame.image.load('piezas imagenes/reina_negro.png').convert_alpha()
reina_negra = pygame.transform.scale(reina_negra, (TAM_CELDA, TAM_CELDA))
alfil_negro = pygame.image.load('piezas imagenes/alfil_negro.png').convert_alpha()
alfil_negro = pygame.transform.scale(alfil_negro, (TAM_CELDA, TAM_CELDA))
torre_negra = pygame.image.load('piezas imagenes/torre_negro.png').convert_alpha()
torre_negra = pygame.transform.scale(torre_negra, (TAM_CELDA, TAM_CELDA))
caballo_negro = pygame.image.load('piezas imagenes/caballo_negro.png').convert_alpha()
caballo_negro = pygame.transform.scale(caballo_negro, (TAM_CELDA, TAM_CELDA))
peon_negro = pygame.image.load('piezas imagenes/peon_negro.png').convert_alpha()
peon_negro = pygame.transform.scale(peon_negro, (TAM_CELDA, TAM_CELDA))
'''
def cargar_imagenes(nombre_img):
    imagen = pygame.image.load(f"piezas imagenes/{nombre_img}.png").convert_alpha()
    imagen_escalada = pygame.transform.scale(imagen, (TAM_CELDA, TAM_CELDA))
    return imagen_escalada

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

PIEZAS = {}

for clave, nombre in Nombres_piezas.items():
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

# Bucle principal
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: #fin del while si user cierra el programa 
            running = False

        elif evento.type == pygame.MOUSEBUTTONDOWN: #Detecto si el user hizo click en la ventana del juego
            x, y = pygame.mouse.get_pos() #Obtenemos cordenadas del click para luego identidicar la celda seleccionada
            fila = y // TAM_CELDA
            col = x // TAM_CELDA
            celda_seleccionada = (fila, col)

    dibujar_tablero()
    pygame.display.flip()

pygame.quit()
