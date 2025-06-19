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

# Definiendo tiempos

TIEMPO_TOTAL = 300  # 5 minutos en segundos
tiempo_blancas = TIEMPO_TOTAL
tiempo_negras = TIEMPO_TOTAL
ultimo_tiempo = pygame.time.get_ticks()
turno_blancas = True

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
    
        fuente = pygame.font.SysFont("Arial", 24)
    texto_blancas = fuente.render(f"Blancas: {int(tiempo_blancas)}s", True, (0, 0, 0))
    texto_negras = fuente.render(f"Negras: {int(tiempo_negras)}s", True, (0, 0, 0))
    ventana.blit(texto_blancas, (10, 10))
    ventana.blit(texto_negras, (10, 40))
    

# Bucle principal
while running:
     # Calcular tiempo transcurrido desde el último frame
    tiempo_actual = pygame.time.get_ticks()
    delta = (tiempo_actual - ultimo_tiempo) / 1000  # En segundos
    ultimo_tiempo = tiempo_actual

    # Restar al jugador correspondiente
    if turno_blancas:
        tiempo_blancas -= delta
    else:
        tiempo_negras -= delta

    # Verificar si algún jugador se quedó sin tiempo
    if tiempo_blancas <= 0:
        print("¡Se acabó el tiempo de las BLANCAS! Negras ganan.")
        running = False
    elif tiempo_negras <= 0:
        print("¡Se acabó el tiempo de las NEGRAS! Blancas ganan.")
        running = False

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
