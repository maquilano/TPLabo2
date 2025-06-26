import pygame
import chess
import time

#Ayuda a modularizar y gestionar la logica de la partida
class EstadoPartida:

    def __init__(self):
        self.tablero = chess.Board()
        self.posiciones = self._inicializar_posiciones()
        self.seleccion = None #(fila, col) o no

    def _inicializar_posiciones(self):
        return [
            ("tn", 0, 0), ("cn", 1, 0), ("an", 2, 0), ("dn", 3, 0), ("rn", 4, 0), ("an", 5, 0), ("cn", 6, 0), ("tn", 7, 0),
            *[("pn", i, 1) for i in range(8)],
            *[("pb", i, 6) for i in range(8)],
            ("tb", 0, 7), ("cb", 1, 7), ("ab", 2, 7), ("db", 3, 7), ("rb", 4, 7), ("ab", 5, 7), ("cb", 6, 7), ("tb", 7, 7),
        ]
    
    #Convierte (col,fila) a square de python-chess.
    def _a_square(self, col: int, fila: int) -> chess.Square:
        return chess.square(col, 7 - fila)
    
    #Valida los mov y devuelve true en caso de que sea un mov legal
    def mover(self, origen: chess.Square, destino: chess.Square) -> bool:
        #obtengo la pieza del origen
        pieza   = self.tablero.piece_at(origen)
        #detecto si la pieza que muevo es un peon
        es_peon = pieza and pieza.piece_type == chess.PAWN
        #el peon corona en caso de que pieza = peon y fila_destino sea 0 o 7
        if es_peon:
            fila_destino = chess.square_rank(destino)  #devuelve la fila de destino (0 a 7)
            if fila_destino == 0 or fila_destino == 7:
                promo = chess.QUEEN #constante en python-chess para indicar que la pieza de promoción es una reina.
            else:
                promo = None
        else:
            promo = None
        #instancio al objeto Move de python-chess para obtener las coord de orig y dest y estado de promocion del peon
        jugada  = chess.Move(origen, destino, promotion=promo)
        if jugada in self.tablero.legal_moves:
            self.tablero.push(jugada)#en caso que el mov sea legal, pusheo el mov
            # Actualizo también la lista de posiciones visuales para reflejar el cambio en pantalla
            self._sincronizar_posiciones(origen, destino, promo)
            
            #JAQUE MATE
            
            if self.tablero.is_checkmate():
                self.jaque_mate = True

                if self.tablero.turn == chess.WHITE:
                    self.gana = "Negras"
                else:
                    self.gana = "Blancas"

            return True
        return False  
    def _mover_torre_enroque(self, nuevas_posiciones, origen, destino):
        for idx, (pieza_id, col, fila) in enumerate(nuevas_posiciones):
            if (col, fila) == origen and pieza_id.startswith("t"):
                nuevas_posiciones[idx] = (pieza_id, destino[0], destino[1])
                break

    def _sincronizar_posiciones(self, origen: chess.Square, destino: chess.Square, promo):
        #Lista donde van a generarse las nuevas pos luego de la jugada
        nuevas_posiciones = []

        columna_destino = chess.square_file(destino)
        fila_destino = 7 - chess.square_rank(destino)

        #eliminar pieza capturada en caso de que hubiera
        for pieza_id, columna, fila in self.posiciones:
            #si en el destino habia una pieza del rival la omitimos y no la agregamos a la lista de nuevas piezas
            if fila == fila_destino and columna == columna_destino:
                continue
            #aqui solo estan las piezas que no estan capturadas con su pos correspondiente
            nuevas_posiciones.append((pieza_id, columna, fila))

        #mover la pieza de origen a destino
        columna_origen = chess.square_file(origen)
        fila_origen    = 7 - chess.square_rank(origen)

        for idx, (pieza_id, columna, fila) in enumerate(nuevas_posiciones):
            if fila == fila_origen and columna == columna_origen:
                #reemplazamos la tupla de coord antigua con las nuevas
                nuevas_posiciones[idx] = (pieza_id, columna_destino, fila_destino)
                break
        # Detectar enroques
        if pieza_id.startswith("r"):
            if (pieza_id == "rb" and (columna_origen, fila_origen) == (4, 7)):
                if (columna_destino, fila_destino) == (6, 7):  # corto blanco
                    self._mover_torre_enroque(nuevas_posiciones, (7, 7), (5, 7))
                elif (columna_destino, fila_destino) == (2, 7):  # largo blanco
                    self._mover_torre_enroque(nuevas_posiciones, (0, 7), (3, 7))
            elif (pieza_id == "rn" and (columna_origen, fila_origen) == (4, 0)):
                if (columna_destino, fila_destino) == (6, 0):  # corto negro
                    self._mover_torre_enroque(nuevas_posiciones, (7, 0), (5, 0))
                elif (columna_destino, fila_destino) == (2, 0):  # largo negro
                    self._mover_torre_enroque(nuevas_posiciones, (0, 0), (3, 0))    
                    
        #Promocion de peon
        for idx, (pieza_id, columna, fila) in enumerate(nuevas_posiciones):
            if pieza_id == "pb" and fila == 0:
                nuevas_posiciones[idx] = ("db", columna, fila)
                print("Peón blanco se convirtió en reina")
            elif pieza_id == "pn" and fila == 7:
                nuevas_posiciones[idx] = ("dn", columna, fila)
                print("Peón negro se convirtió en reina")
        #Actualizamos el estado
        self.posiciones = nuevas_posiciones






     #este metodo devuelve un bool y recibe la (fila,col) donde el usario hizo click
    def seleccionar(self, fila: int, col: int) -> bool: 
        # 1) Primer clic: seleccionar pieza propia
        if not self.seleccion:
            for pieza, c, f in self.posiciones:
                if (f, c) == (fila, col):
                    # solo puedes seleccionar si coincide con el turno actual
                    if (self.tablero.turn == chess.WHITE) == pieza.endswith("b"):
                        self.seleccion = (fila, col)
                    break
            return False

        # 2) Segundo clic: intentar mover
        origen_f, origen_c = self.seleccion
        origen  = self._a_square(origen_c, origen_f)
        destino = self._a_square(col, fila)
        exito = self.mover(origen, destino)
        self.seleccion = None #reset el estado de seleccion aguardando nuevo 1er click
        return exito


# Configuración básica

ALTO_BARRA_TIMER = 40
ANCHO_VENTANA = 640
FILAS, COLUMNAS = 8, 8
TAM_CELDA = ANCHO_VENTANA // COLUMNAS
ALTO_VENTANA = TAM_CELDA * FILAS + 2 * ALTO_BARRA_TIMER


# Colores
BLANCO = (245, 245, 245)
GRIS = (125, 135, 150)
AZUL = (50, 130, 200)


# Inicializar Pygame
pygame.init()
estado = EstadoPartida()
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

# Control de ejecución
running = True


#gracias a este offset los cliks y la pos del mouse no se ve afectada por el tam de la ventana
y_offset = ALTO_BARRA_TIMER 

def dibujar_tablero(posiciones, seleccion):
    
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            color = BLANCO if (fila + col) % 2 == 0 else GRIS
            rect = pygame.Rect(col * TAM_CELDA, y_offset + fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
            pygame.draw.rect(ventana, color, rect)


    if seleccion:
        fila_s, col_s = seleccion
        rect = pygame.Rect(col_s * TAM_CELDA, ALTO_BARRA_TIMER + fila_s * TAM_CELDA, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(ventana, AZUL, rect, 4)

    for pieza_id, col, fila in posiciones:
        ventana.blit(PIEZAS[pieza_id], (col * TAM_CELDA, ALTO_BARRA_TIMER + fila * TAM_CELDA))

    #dibujar barras para timers
    pygame.draw.rect(ventana,BLANCO,(0,0, ANCHO_VENTANA, ALTO_BARRA_TIMER))
    pygame.draw.rect(ventana,BLANCO,(0, ALTO_VENTANA - ALTO_BARRA_TIMER, ANCHO_VENTANA, ALTO_BARRA_TIMER))

def dibujar_tiempos(tiempo_blancas, tiempo_negras):
    tiempo_b_str = time.strftime('%M:%S', time.gmtime(tiempo_blancas))
    tiempo_n_str = time.strftime('%M:%S', time.gmtime(tiempo_negras))

    texto_blanco = fuente.render(f"Blancas: {tiempo_b_str}", True, (0, 0, 0))
    texto_negro = fuente.render(f"Negras: {tiempo_n_str}", True, (0, 0, 0))

    ventana.blit(texto_negro, (10, 10))
    ventana.blit(texto_blanco, (10, ALTO_VENTANA - ALTO_BARRA_TIMER + 10))

#Variables de tiempo
tiempo_total=300
tiempo_blancas=tiempo_total
tiempo_negras=tiempo_total
turno_blanco = True



# Fuente para mostrar tiempo en pantalla
fuente = pygame.font.SysFont("Arial", 24)
    
#----------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------Bucle principal---------------------------------------------------------------------
running = True
# Última vez que se actualizó el temporizador
ultimo_tiempo = time.time()

while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del mouse y convertir a fila y columna del tablero
            x, y = pygame.mouse.get_pos()
            if y < y_offset:
                continue
            #convertir a coord de tablero
            fila = (y - y_offset) // TAM_CELDA
            col = x // TAM_CELDA

            estado.seleccionar(fila, col)

     # Actualizar temporizadores segun el turno actual
    ahora = time.time()
    delta = ahora - ultimo_tiempo
    ultimo_tiempo = ahora

    if estado.tablero.turn == chess.WHITE:
        tiempo_blancas -= delta
    else:
        tiempo_negras -= delta
    # Si alguno llega a 0, termina el juego
    if tiempo_blancas <= 0:
        print("¡Las negras ganan por tiempo!")
        texto = fuente.render(f"¡Las negras ganan por tiempo!",True, (255,0,0))
        ventana.blit(texto,(ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2))
        pygame.display.flip()
        pygame.time.delay(5000)
        running = False
    elif tiempo_negras <= 0:
        print("¡Las blancas ganan por tiempo!")
        texto = fuente.render(f"¡Las blancas ganan por tiempo!",True, (255,0,0))
        ventana.blit(texto,(ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2))
        pygame.display.flip()
        pygame.time.delay(5000)
        running = False

#Renderizado de la ventana
    dibujar_tablero(estado.posiciones, estado.seleccion)
    dibujar_tiempos(tiempo_blancas, tiempo_negras)
    pygame.display.flip()

    if hasattr(estado,"jaque_mate") and estado.jaque_mate:
        texto = fuente.render(f"JAQUE MATE!!! {estado.gana} gana.",True, (255,0,0))
        ventana.blit(texto,(ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2))
        pygame.display.flip()
        pygame.time.delay(5000)
        running = False

pygame.quit()