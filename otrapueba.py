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

PIEZAS = {
    "rb": rey_blanco,
    "db": reina_blanca,
    "ab": alfil_blanco,
    "tb": torre_blanca,
    "cb": caballo_blanco,
    "pb": peon_blanco,
    "rn": rey_negro,
    "dn": reina_negra,
    "an": alfil_negro,
    "tn": torre_negra,
    "cn": caballo_negro,
    "pn": peon_negro,
}

# Posiciones iniciales de las piezas (pieza, columna, fila)
posiciones_piezas = [
    ("tn", 0, 7), ("cn", 1, 7), ("an", 2, 7), ("dn", 3, 7), ("rn", 4, 7), ("an", 5, 7), ("cn", 6, 7), ("tn", 7, 7),
    *[("pn", i, 6) for i in range(8)],
    *[("pb", i, 1) for i in range(8)],
    ("tb", 0, 0), ("cb", 1, 0), ("ab", 2, 0), ("db", 3, 0), ("rb", 4, 0), ("ab", 5, 0), ("cb", 6, 0), ("tb", 7, 0),
]

# Control de ejecución
running = True
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
        if evento.type == pygame.QUIT:
            running = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            fila = y // TAM_CELDA
            col = x // TAM_CELDA
            celda_seleccionada = (fila, col)

    dibujar_tablero()
    pygame.display.flip()

pygame.quit()
