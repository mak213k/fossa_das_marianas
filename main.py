import pygame
import random
import sys
import os

# Inicialização
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Missão Mariana")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 100)


# for i in range (0,255):
#     print(AZUL(i,i,i))
#     exit(0)

VERMELHO = (200, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Submarino
# submarino_img = pygame.Surface((50, 30))
# submarino_img.fill((0, 100, 255))


# Variáveis de movimento
vel = 5

nivel_mar = 11000  # Arbitrário, quando atingir, "vence"
profundidade = 0
# Obstáculos
obstaculos = []

# Imagens
SUBMARINO_IMG = pygame.image.load(os.path.join("assets/img", "submarino.png")).convert_alpha()
SUBMARINO_IMG = pygame.transform.scale(SUBMARINO_IMG, (80, 40))
# submarino_rect = SUBMARINO_IMG
submarino_rect = SUBMARINO_IMG.get_rect(center=(LARGURA // 2, 50))


ROCHA_IMG = pygame.image.load(os.path.join("assets/img", "rocha.png")).convert_alpha()
ROCHA_IMG = pygame.transform.scale(ROCHA_IMG, (50, 70))

AGUA_VIVA_IMG = pygame.image.load(os.path.join("assets/img", "agua_viva.png")).convert_alpha()
AGUA_VIVA_IMG = pygame.transform.scale(AGUA_VIVA_IMG, (40, 60))

# Obstáculos
def criar_obstaculo():
    tipo = random.choice(['rocha', 'animal'])
    x = random.choice([random.randint(0, 150), random.randint(0, LARGURA)])
    y = random.randint(-100, -40)

    if tipo == 'rocha':
        imagem = ROCHA_IMG
        rect = imagem.get_rect(topleft=(x, y))
    else:
        imagem = AGUA_VIVA_IMG
        rect = imagem.get_rect(topleft=(x, y))

    return {'rect': rect, 'tipo': tipo, 'imagem': imagem}

def desenhar_obstaculos():
    for ob in obstaculos:
        if ob['imagem']:
            tela.blit(ob['imagem'], ob['rect'])
        else:
            pygame.draw.rect(tela, (255, 0, 255), ob['rect'])  # Fallback

def criar_bolha():
    x = random.randint(submarino_rect.left + 10, submarino_rect.right - 10)
    y = submarino_rect.bottom
    r = random.randint(2, 4)
    return {'x': x, 'y': y, 'r': r, 'vel': random.uniform(1, 2.5)}

def mover_bolhas():
    for bolha in bolhas:
        bolha['y'] -= bolha['vel']
    bolhas[:] = [b for b in bolhas if b['y'] > 0]

def mover_obstaculos():
    for ob in obstaculos:
        ob['rect'].y += 3

def verificar_colisoes():
    for ob in obstaculos:
        if submarino_rect.colliderect(ob['rect']):
            return True
    return False

def resetar_jogo():
    global submarino_rect, profundidade, obstaculos
    submarino_rect.center = (LARGURA // 2, 50)
    profundidade = 0
    obstaculos = []

def desenhar_bolhas():
    for b in bolhas:
        pygame.draw.circle(tela, (173, 216, 230), (int(b['x']), int(b['y'])), b['r'])

# Game loop
jogando = True
estado = "subindo"  # outros: "subindo", "vitoria", "fim"

def controle(teclas):
    if teclas[pygame.K_LEFT]:
        submarino_rect.x -= vel
    if teclas[pygame.K_RIGHT]:
        submarino_rect.x += vel
    if teclas[pygame.K_UP]:
        submarino_rect.y -= vel
    if teclas[pygame.K_DOWN]:
        submarino_rect.y += vel


while jogando:
    tela.fill(PRETO)
    """
    Objeto Submarino sendo criado. Ainda sem uma figura. Apenas um quadrado
    """
    pygame.draw.rect(tela, (0, 100, 200), submarino_rect)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogando = False

    teclas = pygame.key.get_pressed()
    
    controle(teclas)

    if estado in ["descendo", "subindo"]:
        if random.randint(1, 30) == 1:
            obstaculos.append(criar_obstaculo())

        mover_obstaculos()
        desenhar_obstaculos()
        print()
        if verificar_colisoes():
            # som_colisao.play()
            estado = "fim"

        elif profundidade >= nivel_mar:
            som_vitoria.play()
            estado = "subindo"
            obstaculos.clear()

        if estado == "descendo":
            profundidade -= 1
            # if profundidade >= nivel_mar:
            #     estado = "subindo"
            #     obstaculos.clear()
        elif estado == "subindo":
            profundidade += 1
            if profundidade >= nivel_mar:
                estado = "vitoria"
                
        # HUD com profundidade
        fonte_hud = pygame.font.SysFont(None, 28)
        texto_profundidade = fonte_hud.render(f"Altura: {profundidade} m", True, BRANCO)
        tela.blit(texto_profundidade, (10, 10))

    if estado == "fim":
        fonte = pygame.font.SysFont(None, 64)
        msg = fonte.render("Fim de Jogo", True, VERMELHO)
        tela.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2))
    elif estado == "vitoria":
        fonte = pygame.font.SysFont(None, 64)
        msg = fonte.render("Você venceu!", True, BRANCO)
        tela.blit(msg, (LARGURA//2 - msg.get_width()//2, ALTURA//2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()