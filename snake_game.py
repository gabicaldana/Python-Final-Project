# PROJETO PYTHON
# Snake Game

from tkinter import *
import random

# Configurações do Jogo
LARGURA = 700  # Largura da área de jogo
ALTURA = 700  # Altura da área de jogo
VELOCIDADE = 80  # Velocidade da cobra
TAMANHO_ITENS = 50  # Tamanho dos itens (cobra e comida)
PARTES_CORPO = 3  # Partes iniciais da cobra
COR_COBRA = '#FF6EC7'  # Rosa
COR_COMIDA = '#A020F0'  # Roxo
COR_FUNDO = '#000000'  # Preto

# Estado inicial do jogo
jogo_em_andamento = False

class Cobra:
    def __init__(self):
        self.tamanho_corpo = PARTES_CORPO
        self.coordenadas = []
        self.segmentos = []

        for i in range(0, PARTES_CORPO):
            self.coordenadas.append([0, 0])

        for x, y in self.coordenadas:
            segmento = canvas.create_rectangle(
                x, y, x + TAMANHO_ITENS, y + TAMANHO_ITENS, fill=COR_COBRA, tag="cobra"
            )
            self.segmentos.append(segmento)

class Comida:
    def __init__(self):
        x = random.randint(0, (LARGURA // TAMANHO_ITENS) - 1) * TAMANHO_ITENS
        y = random.randint(0, (ALTURA // TAMANHO_ITENS) - 1) * TAMANHO_ITENS

        self.coordenadas = [x, y]
        canvas.create_oval(
            x, y, x + TAMANHO_ITENS, y + TAMANHO_ITENS, fill=COR_COMIDA, tag="comida"
        )

def animar_comida(x, y):
    """Efeito de pulsação ao comer comida."""
    for i in range(3):  # Número de pulsos
        oval = canvas.create_oval(
            x - i * 5, y - i * 5, x + TAMANHO_ITENS + i * 5, y + TAMANHO_ITENS + i * 5,
            outline="yellow", width=2
        )
        janela.update()  # Atualiza a tela para mostrar a animação
        janela.after(50)  # Pequena pausa entre os pulsos
        canvas.delete(oval)  # Remove o efeito após exibição

def proxima_jogada(cobra, comida):
    """Define a próxima jogada do jogo."""
    if not jogo_em_andamento:
        return

    global direcao
    x, y = cobra.coordenadas[0]

    if direcao == "cima":
        y -= TAMANHO_ITENS
    elif direcao == "baixo":
        y += TAMANHO_ITENS
    elif direcao == "esquerda":
        x -= TAMANHO_ITENS
    elif direcao == "direita":
        x += TAMANHO_ITENS

    cobra.coordenadas.insert(0, (x, y))

    segmento = canvas.create_rectangle(
        x, y, x + TAMANHO_ITENS, y + TAMANHO_ITENS, fill=COR_COBRA
    )
    cobra.segmentos.insert(0, segmento)

    if x == comida.coordenadas[0] and y == comida.coordenadas[1]:
        global pontuacao
        pontuacao += 1
        label.config(text="Pontuação: {}".format(pontuacao))
        
        # Chamar animação de comida
        animar_comida(comida.coordenadas[0], comida.coordenadas[1])
        
        canvas.delete("comida")
        comida = Comida()
    else:
        del cobra.coordenadas[-1]
        canvas.delete(cobra.segmentos[-1])
        del cobra.segmentos[-1]

    if checar_colisoes(cobra):
        fim_de_jogo()
    else:
        janela.after(VELOCIDADE, proxima_jogada, cobra, comida)

def mudar_direcao(nova_direcao):
    """Muda a direção da cobra, evitando movimentos opostos."""
    global direcao
    if nova_direcao == "esquerda" and direcao != "direita":
        direcao = nova_direcao
    elif nova_direcao == "direita" and direcao != "esquerda":
        direcao = nova_direcao
    elif nova_direcao == "cima" and direcao != "baixo":
        direcao = nova_direcao
    elif nova_direcao == "baixo" and direcao != "cima":
        direcao = nova_direcao

def checar_colisoes(cobra):
    """Verifica se a cobra colidiu com as paredes ou com ela mesma."""
    x, y = cobra.coordenadas[0]

    # Colisão com paredes
    if x < 0 or x >= LARGURA or y < 0 or y >= ALTURA:
        return True

    # Colisão com o próprio corpo
    for parte_corpo in cobra.coordenadas[1:]:
        if x == parte_corpo[0] and y == parte_corpo[1]:
            return True

    return False

def fim_de_jogo():
    """Finaliza o jogo e exibe a mensagem de fim."""
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("Comic Sans Ms", 50),
        text="FIM DE JOGO",
        fill="red",
        tag="fimdejogo",
    )

def iniciar_jogo(event):
    """Inicia o jogo ao pressionar uma tecla."""
    global jogo_em_andamento
    if not jogo_em_andamento:
        jogo_em_andamento = True
        proxima_jogada(cobra, comida)

# Configuração da janela principal
janela = Tk()
janela.title("Jogo da Cobra")
janela.resizable(False, False)

pontuacao = 0
direcao = "baixo"

# Pontuação
label = Label(janela, text="Pontuação: {}".format(pontuacao), font=("Comic Sans Ms", 40))
label.pack()

# Área de Jogo
canvas = Canvas(janela, bg=COR_FUNDO, height=ALTURA, width=LARGURA)
canvas.pack()

# Centralizar janela na tela
janela.update()
largura_janela = janela.winfo_width()
altura_janela = janela.winfo_height()
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
x = int((largura_tela / 2) - (largura_janela / 2))
y = int((altura_tela / 2) - (altura_janela / 2))
janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

# Controles
janela.bind("<Left>", lambda event: [mudar_direcao("esquerda"), iniciar_jogo(event)])
janela.bind("<Right>", lambda event: [mudar_direcao("direita"), iniciar_jogo(event)])
janela.bind("<Up>", lambda event: [mudar_direcao("cima"), iniciar_jogo(event)])
janela.bind("<Down>", lambda event: [mudar_direcao("baixo"), iniciar_jogo(event)])

# Inicializar cobra e comida
cobra = Cobra()
comida = Comida()

# Iniciar o loop principal
janela.mainloop()
