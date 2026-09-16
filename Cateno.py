
import tkinter as tk
import customtkinter as ctk
import pyperclip
import ctypes
import sys
import os
import json
import math
from PIL import Image, ImageDraw

# Paleta do aplicativo: cada par segue a ordem (CLARO, ESCURO)

CORES = {
    "fundo_janela": ("#fcf7f1", "#1E1E1E"),
    "fundo_previa": ("#e0e6ed", "#393939"),
    "texto_previa": ("#2F5600", "#F1FFBE"),

    "colar": ("#7fc7cc", "#77bcc1"),
    "colar_hover": ("#70b0b5", "#669da0"),

    "acao_verde": ("#b8d558", "#9db64a"),
    "acao_verde_hover": ("#96ae3f", "#839738"),

    "limpar": ("#f4713d", "#f4713d"),
    "limpar_hover": ("#d06034", "#d06034"),

    "modo_inativo": ("#c8c8c8", "#8d8d8d"),
    "modo_inativo_hover": ("#a1a1a1", "#7b7b7b"),

    "texto_botao": ("#ffffff", "#ffffff"),
    "texto_modo_inativo": ("#fff9ef", "#fff9ef"),

    "fundo_aviso": ("#7fc7cc", "#77bcc1"),
    "texto_aviso": ("#ffffff", "#ffffff"),

    "fundo_titulo": ("#e0e6ed", "#393939"),
    "texto_titulo": ("#2F5600", "#F1FFBE"),

    "fundo_separador": ("#e0e6ed", "#343638"),
    "texto_separador": ("#2F5600", "#DCE4EE"),
    "borda_separador": ("#A5ADB5", "#565B5E"),

    "switch_desligado": ("#B8BEC5", "#555555"),
    "switch_circulo": ("#626D78", "#F2F2F2"),
    "switch_circulo_hover": ("#57616A", "#D9D9D9"),

    "texto_configuracao": ("#333333", "#DCE4EE"),

    "icone_hover": ("#E0E6ED", "#393939"),

    "icone_voltar": ("#505860", "#FFFFFF"),

    "icone_configuracoes": ("#626D78", "#A0A0A0"),
}

# Local para guardar as configurações do usuário

pasta_dados_usuario = os.getenv("LOCALAPPDATA") # consulta o caminho que o Windows disponibiliza para os dados locais do usuário

if not pasta_dados_usuario:
    pasta_dados_usuario = os.path.join(   # junta as partes do caminho
        os.path.expanduser("~"),
        "AppData",
        "Local"
    )

pasta_configuracoes = os.path.join(pasta_dados_usuario, "Cateno") # aponta para a pasta do Cateno
caminho_configuracoes = os.path.join(  # aponta para o arquivo dentro dela
    pasta_configuracoes,
    "configuracoes.json",
)

def obter_caminho(nome_arquivo):
    # Pega o caminho correto do arquivo, seja rodando no VS Code ou no .exe final
    try:
        # Quando vira .exe, o PyInstaller guarda os arquivos nessa pasta termporária
        caminho_base = sys._MEIPASS
    except Exception:
        # Quando tá sendo rodado no VS Code
        caminho_base = os.path.abspath(".")
    return os.path.join(caminho_base, nome_arquivo)

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# --- Configurações Visuais do CustomTkinter
ctk.set_appearance_mode("dark") # ativa o modo escuro, podendo ser "dark", "light" ou "system"
ctk.set_default_color_theme("blue") # Tema padrão dos botões (não é considerado pois a cor foi definida na próxima função)


# --- 1. Variáveis Globais
# Ela fica fora das funções para que todas elas possam exergá-la
resultado_completo_sql = ""
modo_atual = "varchar"  # O programa sempre vai abrir com o modo varchar ativado
tema_atual = "dark"

# --- Configurações Independentes para cada modo de formatação
configuracoes = {
    "varchar": {
        "separador": ",",
        "espaco_apos_separador": True,
        "fechar_parenteses": True,
    },
    "virgula": {
            "separador": ",",
            "espaco_apos_separador": True,
            "fechar_parenteses": True,
}
}

def alterar_modo(novo_modo):
    global modo_atual
    modo_atual = novo_modo

    if modo_atual == "varchar":
        btn_aba_varchar.configure(
            fg_color=CORES["acao_verde"],
            text_color=CORES["texto_botao"],
            hover_color=CORES["acao_verde_hover"],
        )
        btn_aba_virgula.configure(
            fg_color=CORES["modo_inativo"],
            text_color=CORES["texto_modo_inativo"],
            hover_color=CORES["modo_inativo_hover"],
        )

    elif modo_atual == "virgula":
        btn_aba_varchar.configure(
            fg_color=CORES["modo_inativo"],
            text_color=CORES["texto_modo_inativo"],
            hover_color=CORES["modo_inativo_hover"],
        )
        btn_aba_virgula.configure(
            fg_color=CORES["acao_verde"],
            text_color=CORES["texto_botao"],
            hover_color=CORES["acao_verde_hover"],
        )

    limpar_tudo()

    print(f"O modo atual é: {modo_atual}")

#---------------------------------AVISO FLUTUANTE TEMPORÁRIO--------------------------------------#

def mostrar_aviso(mensagem):
    # Escolhe onde o aviso será exibido
    if tela_configuracoes.winfo_ismapped():
        area_aviso = tela_configuracoes
        cor_fundo = janela.cget("fg_color")
    else:
        area_aviso = campo_texto
        cor_fundo = campo_texto.cget("fg_color")

    # Cria o balão dentro da área escolhida
    popup = ctk.CTkFrame(
        area_aviso,
        fg_color=CORES["fundo_aviso"],
        corner_radius=6,
        bg_color=cor_fundo,
    )

    lbl = ctk.CTkLabel(
        popup,
        text=mensagem,
        text_color=CORES["texto_aviso"],
        font=("Inter", 12),
        fg_color="transparent",
    )
    lbl.pack(padx=15, pady=6)

    # Centraliza o aviso dentro dessa área
    popup.place(relx=0.5, rely=0.5, anchor="center")
    popup.lift()

    # Remove o aviso após 1,5 segundo
    janela.after(1500, popup.destroy)
    
#---------------------------------COLAR E FORMATAR--------------------------------------#

def processar_e_formatar():     
    global resultado_completo_sql, modo_atual # informa que será usada a variável inicial

    # Pega o texto da área de transferência (clipboard)
    texto_bruto = pyperclip.paste()

    if not texto_bruto.strip():
        mostrar_aviso("Área de transferência vazia!")
        return
    

    # 1. Divide o texto por quebras de linha e cria uma lista
    linhas = texto_bruto.splitlines()  # transforma o texto em uma lista, cortando onde tem um Enter

    # 2. Limpa espaços e remove linhas vazias (list comprehension)
    itens_limpos = [linha.strip() for linha in linhas if linha.strip()]     # cria uma lista de nome itens_limpos contendo todas as linhas da
                                                                            # lista "linhas", já sem espaços, somente as que não estiverem vazias.
                                                                            # strip() remove espaços do inicio e do fim.
                                                                            # if linha.strip() só deixa avançar se tiver conteúdo.

    # 3 e 4. Verifica qual modo está ativo e aplica a formatação correspondente
    if modo_atual == "varchar":
        # REGRA 1: Com aspas simples
        itens_formatados = [f"'{item}'" for item in itens_limpos]
    else:
        # REGRA 2: Sem aspas
        itens_formatados = [f"{item}" for item in itens_limpos]

    # Consulta as configurações do modo selecionado
    config_atual = configuracoes[modo_atual]

    # Monta o separador com ou sem espaço adicional
    separador = config_atual["separador"]

    if config_atual["espaco_apos_separador"]:
        separador += " "

    # Une os valores usando o separador configurado
    resultado_completo_sql = separador.join(itens_formatados)

    # Adiciona parênteses quando essa opção estiver ativada
    if config_atual["fechar_parenteses"]:
        resultado_completo_sql = "(" + resultado_completo_sql + ")"

    # 5. Cria o PREVIEW (8 itens)
    preview_itens = itens_formatados[:8]
    resumo = separador.join(preview_itens)

    if len (itens_formatados) > 8:
        resumo += separador + "..." # Adiciona as reticências quando tiver mais de 8 códigos

    if config_atual["fechar_parenteses"]:
        resumo = "(" + resumo + ")"

    # 6. Limpa o campo de texto e escreve o resumo
    campo_texto.configure(state='normal')  # Destranca o campo para o Python poder escrever
    
    campo_texto.delete("1.0", tk.END)   # Limpa o que tinha antes
    campo_texto.insert("1.0", resumo)   # Escreve o novo resumo de 8 itens

    campo_texto.configure(state='disabled') # Tranca o campo novamente

#----------------------------------COPIAR--------------------------------------#

def copiar_para_clipboard():
    if resultado_completo_sql:
        pyperclip.copy(resultado_completo_sql)
        mostrar_aviso("Copiado!")
    else:
        mostrar_aviso("Campo vazio!")

#---------------------------------LIMPAR TUDO--------------------------------------#

def limpar_tudo():
    global resultado_completo_sql
    resultado_completo_sql = ""

    campo_texto.configure(state='normal') # Destranca o campo para o Python poder apagar

    campo_texto.delete("1.0", tk.END)

    campo_texto.configure(state='disabled') # Tranca o campo novamente

#---------------------------------MINIMIZAR AO PERDER O FOCO--------------------------------------#

def minimizar_ao_perder_foco(event):
    def checar_foco():                        
        if janela.focus_get() is None and janela.state() != "iconic":      # janela.focus_get() verifica o que está selecionado no momento
            janela.iconify() # minimiza o app                              # só minimiza se o foco for None e a janela nao estiver minimizada
    
    janela.after(200, checar_foco) #.after diz pra esperar o tempo escrito (200 milissegundos) antes de checar

def ativar_minimizacao(event):
    # Ignora eventos recebidos por componentes internos
    if event.widget != janela:
        return

    # Ativa a minimização após a janela receber foco
    janela.bind("<FocusOut>", minimizar_ao_perder_foco)

    # Remove apenas este vínculo de ativação
    janela.unbind("<FocusIn>", vinculo_ativacao_minimizacao)


#---------------------------------NAVEGAÇÃO ENTRE TELAS--------------------------------------#

def ajustar_foco_configuracoes(event):
    componente = event.widget

    # Percorre o componente clicado e seus conteineres
    while componente is not None:
        # Se o clique foi dentro de um campo, mantém a edição
        if isinstance(componente, ctk.CTkEntry):
            return

        # Se chegou a tela sem encontrar um campo, retira o foco
        if componente == tela_configuracoes:
            tela_configuracoes.focus_set()
            return

        componente = getattr(componente, "master", None)

def abrir_configuracoes():
    tela_principal.pack_forget()
    janela.geometry("350x340")
    tela_configuracoes.pack(fill="both", expand=True)
    tela_configuracoes.focus_set()

def voltar_para_principal():
    # Restaura o separador salvo do Varchar    
    campo_separador_varchar.delete(0, "end")
    campo_separador_varchar.insert(
        0,
        configuracoes["varchar"]["separador"],
    )

    # Restaura a opção salva de espaço do Int
    if configuracoes["virgula"]["espaco_apos_separador"]:
        opcao_espaco_int.select()
    else:
        opcao_espaco_int.deselect()

    # Restaura a opção salva de parênteses do Int
    if configuracoes["virgula"]["fechar_parenteses"]:
        opcao_parenteses_int.select()
    else:
        opcao_parenteses_int.deselect()

    # Restaura a opção salva de espaço do Varchar
    if configuracoes["varchar"]["espaco_apos_separador"]:
        opcao_espaco_varchar.select()
    else:
        opcao_espaco_varchar.deselect()

    # Restaura a opção salva de parênteses do Varchar

    if configuracoes["varchar"]["fechar_parenteses"]:
        opcao_parenteses_varchar.select()
    else:
        opcao_parenteses_varchar.deselect()

    # Restaura o separador salvo do Int
    campo_separador_int.delete(0, "end")
    campo_separador_int.insert(
        0,
        configuracoes["virgula"]["separador"],
    )

    # Retorna à tela principal
    tela_configuracoes.pack_forget()
    janela.geometry("350x200")
    tela_principal.pack(fill="both", expand=True)

#---------------------------------CARREGA AS CONFIGURAÇÕES--------------------------------------# 

def carregar_configuracoes():
    global tema_atual

    try:
        with open(caminho_configuracoes, "r", encoding="utf-8") as arquivo: # "r" abre o arquivo para leitura
            dados = json.load(arquivo) # transforma o conteúdo JSON em estruturas do Python, incluindo dicionários e booleanos

    except FileNotFoundError:
        # Na primeira execução, o arquivo ainda não existe
        return

    except (OSError, ValueError) as erro:
        print(f"Não foi possível carregar as configurações: {erro}")
        return

    # O conteúdo principal precisa ser um dicionário
    if not isinstance(dados, dict): # verifica o tipo do dado antes de utilizá-lo
        return

    # Recupera o tema, aceitando apenas os valores esperados
    tema_salvo = dados.get("tema")

    if tema_salvo in ("light", "dark"):
        tema_atual = tema_salvo

    # Verifica separadamente as configurações de cada modo
    for modo in configuracoes: 
        dados_modo = dados.get(modo)

        if not isinstance(dados_modo, dict):
            continue

        separador = dados_modo.get("separador")

        if isinstance(separador, str):
            configuracoes[modo]["separador"] = separador or ","

        for opcao in ("espaco_apos_separador", "fechar_parenteses"):
            valor = dados_modo.get(opcao)

            if isinstance(valor, bool):
                configuracoes[modo][opcao] = valor

#---------------------------------SALVAR--------------------------------------# 

def salvar_configuracoes():
    # Reúne as escolhas feitas nos campos da interface
    novas_configuracoes = {
        "varchar": {
            "separador": campo_separador_varchar.get() or ",",
            "espaco_apos_separador": opcao_espaco_varchar.get() == 1,
            "fechar_parenteses": opcao_parenteses_varchar.get() == 1,
        },
        "virgula": {
            "separador": campo_separador_int.get() or ",",
            "espaco_apos_separador": opcao_espaco_int.get() == 1,
            "fechar_parenteses": opcao_parenteses_int.get() == 1,
        },
    }

    try:
        # Cria a pasta caso ela ainda não exista
        os.makedirs(pasta_configuracoes, exist_ok=True)

        # Grava as escolhas no arquivo JSON
        with open(caminho_configuracoes, "w", encoding="utf-8") as arquivo: # abre o arquivo pra escrita, criando ou substituindo seu conteúdo
            json.dump(
                {
                    **novas_configuracoes,
                    "tema": tema_atual,
                },
                arquivo,
                ensure_ascii=False,
                indent=4,
            )

    except OSError as erro:  # trata problemas de acesso ou escrita no arquivo
        print(f"Erro ao salvar as configurações: {erro}")
        mostrar_aviso("Não foi possível salvar.")
        return

    # Aplica as escolhas depois que a gravação termina
    configuracoes.update(novas_configuracoes)  # aplica os valores ao dicionário utilizado pelo programa

    limpar_tudo()
    voltar_para_principal()

#----------------------------CRIA ICONE TEMA-----------------------------------#

def criar_icone_tema():
    imagens = []

    for tema in ("light", "dark"):
        imagem = Image.new("RGBA", (136, 72), (0, 0, 0, 0))
        desenho = ImageDraw.Draw(imagem)

        if tema == "light":
            cor_barra = CORES["limpar"][0]
            centro_x = 100
        else:
            cor_barra = "#315A91"
            centro_x = 36

        # Cápsula externa
        desenho.rounded_rectangle(
            (0, 0, 135, 71),
            radius=36,
            fill=cor_barra,
        )

        # Círculo: à direita no claro e à esquerda no escuro
        desenho.ellipse(
            (centro_x - 28, 8, centro_x + 28, 64),
            fill="#F2F2F2",
        )

        if tema == "light":
            # Centro do sol
            desenho.ellipse(
                (centro_x - 8, 28, centro_x + 8, 44),
                fill=cor_barra,
            )

            # Oito raios ao redor do sol
            for indice in range(8):
                angulo = math.radians(indice * 45)

                inicio = (
                    centro_x + 13 * math.cos(angulo),
                    36 + 13 * math.sin(angulo),
                )
                fim = (
                    centro_x + 19 * math.cos(angulo),
                    36 + 19 * math.sin(angulo),
                )

                desenho.line([inicio, fim], fill=cor_barra, width=3)
        else:
            # Lua: sobrepõe dois círculos para formar o crescente
            desenho.ellipse(
                (centro_x - 13, 23, centro_x + 13, 49),
                fill=cor_barra,
            )
            desenho.ellipse(
                (centro_x - 5, 19, centro_x + 19, 43),
                fill="#F2F2F2",
            )

        imagens.append(imagem)

    return ctk.CTkImage(
        light_image=imagens[0],
        dark_image=imagens[1],
        size=(34, 18),
    )

#---------------------------------ALTERA O TEMA--------------------------------------# 

def alternar_tema():
    global tema_atual

    if tema_atual == "dark":
        novo_tema = "light"
    else:
        novo_tema = "dark"

    # Usa as configurações já salvas, sem ler os campos da tela
    dados_para_salvar = {
        **configuracoes,
        "tema": novo_tema,
    }

    try:
        os.makedirs(pasta_configuracoes, exist_ok=True)

        with open(caminho_configuracoes, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados_para_salvar,
                arquivo,
                ensure_ascii=False,
                indent=4,
            )

    except OSError as erro:
        print(f"Erro ao salvar o tema: {erro}")
        mostrar_aviso("Não foi possível salvar o tema.")
        return

    tema_atual = novo_tema
    ctk.set_appearance_mode(tema_atual)

#---------------------------------INTERFACE VISUAL--------------------------------------# 

def criar_interface():
    
    global campo_texto, janela, btn_aba_varchar, btn_aba_virgula
    global tela_principal, tela_configuracoes
    global campo_separador_varchar
    global campo_separador_int
    global opcao_espaco_int
    global opcao_parenteses_int
    global opcao_espaco_varchar
    global opcao_parenteses_varchar
    global vinculo_ativacao_minimizacao


    # 1. Cria a janela principal
    janela = ctk.CTk()                    # abre o processo da janela no windows

    janela.withdraw()  # esconde a janela

    # Altera a cor do fundo conforme o tema ativo
    janela.configure(fg_color=CORES["fundo_janela"])

    janela.title("Cateno")

    # ICONE E FONTES EMBUTIDOS

    # 1. Carrega o item de forma segura para o .exe
    caminho_icone = obter_caminho("cateno.ico" )
    janela.iconbitmap(caminho_icone)

    # 2. Carrega as fontes na memória RAM do usuário
    caminho_fonte_inter = obter_caminho("Inter-VariableFont_slnt,wght.ttf")

    ctk.FontManager.load_font(caminho_fonte_inter)
    
    #janela.attributes('-topmost', True)  # Deixar a janela sempre visivel 

#---------------------------------CALCULO MONITOR--------------------------------------#

    largura_app = 350
    altura_app = 200

    # Define o tamanho; a posição será calculada após montar a janela
    janela.geometry(f"{largura_app}x{altura_app}")
    
#--------------------------------------------------------------------------------------#

    # janela.bind("<FocusOut>", minimizar_ao_perder_foco)  # diz: se a janela perder o foco, execute a função minimizar_ao_perder_foco

    # Deixar a janela sempre visivel 
    # janela.attributes('-topmost', True)

    tela_principal = ctk.CTkFrame(janela, fg_color="transparent")
    tela_principal.pack(fill="both", expand= True)

#---------------------------------ABAS SUPERIORES--------------------------------------#
  
    frame_abas = ctk.CTkFrame(tela_principal, fg_color="transparent") # transparent faz o frame sumir e misturar com o fundo da janela
    frame_abas.pack(pady=(15, 0)) # significa: (cima, baixo)

    btn_aba_varchar = ctk.CTkButton(frame_abas, text="Aspas simples", width=147, height=28, corner_radius=8,
                                    font=("Inter SemiBold", 13),
                                    command=lambda: alterar_modo("varchar"))   # corner_radius é o nivel de arredondamento das bordas
    btn_aba_varchar.pack(side="left", padx=(11, 5))

    btn_aba_virgula = ctk.CTkButton(frame_abas, text="Sem aspas", width=147, height=28, corner_radius=8,
                                    font=("Inter SemiBold", 13),
                                    command=lambda: alterar_modo("virgula"))
    btn_aba_virgula.pack(side="left", padx=(5, 11))

    #---------------------------------CAMPO TEXTO--------------------------------------#

    # Campo que permite várias linhas
    campo_texto = ctk.CTkTextbox(
        tela_principal,
        width=305,
        height=55,
        state="disabled",
        fg_color=CORES["fundo_previa"],
        text_color=CORES["texto_previa"],
        corner_radius=8,
        font=("Consolas", 13),
    )
    campo_texto.pack(pady=(15, 0), padx=10) # pack () posiciona o elemento na tela, posiciona um embaixo do outro. pady é o espaço (padding) vertical 
      
    #---------------------------------BOTÕES INFERIORES--------------------------------------#

    # Organiza os botões lado a lado
    frame_botoes = ctk.CTkFrame(tela_principal, fg_color="transparent")
    frame_botoes.pack(pady=(15, 5))

    # Botão 1: Colar
    btn_colar = ctk.CTkButton(
        frame_botoes,
        text="Colar",
        width=95,
        height=28,
        corner_radius=8,
        font=("Inter SemiBold", 13),
        fg_color=CORES["colar"],
        text_color=CORES["texto_botao"],
        hover_color=CORES["colar_hover"],
        command=processar_e_formatar,
    )
    btn_colar.pack(side="left", padx=5)

    # Botão 2: Copiar 
    btn_copiar = ctk.CTkButton(
        frame_botoes,
        text="Copiar",
        width=95,
        height=28,
        corner_radius=8,
        font=("Inter SemiBold", 13),
        fg_color=CORES["acao_verde"],
        text_color=CORES["texto_botao"],
        hover_color=CORES["acao_verde_hover"],
        command=copiar_para_clipboard,
    )
    btn_copiar.pack(side="left", padx=5)

    # Botão 3: Limpar
    btn_limpar = ctk.CTkButton(
        frame_botoes,
        text="Limpar",
        width=95,
        height=28,
        corner_radius=8,
        font=("Inter SemiBold", 13),
        fg_color=CORES["limpar"],
        text_color=CORES["texto_botao"],
        hover_color=CORES["limpar_hover"],
        command=limpar_tudo,
    )
    btn_limpar.pack(side="left", padx=5)

    # Acesso as configurações na tela principal

# Calcula os pontos do desenho uma única vez
    pontos_engrenagem = []

    for indice in range(32):
        angulo = math.radians(indice * 360 / 32)

        if indice % 4 in (1, 2):
            raio = 34
        else:
            raio = 27

        x = 40 + raio * math.cos(angulo)
        y = 40 + raio * math.sin(angulo)

        pontos_engrenagem.append((x, y))

    # Desenha uma versão da engrenagem para cada tema
    imagens_engrenagem = []

    for cor in CORES["icone_configuracoes"]:
        imagem_engrenagem = Image.new(
            "RGBA",
            (80, 80),
            (0, 0, 0, 0),
        )
        desenho_engrenagem = ImageDraw.Draw(imagem_engrenagem)

        desenho_engrenagem.polygon(
            pontos_engrenagem,
            fill=cor,
        )

        desenho_engrenagem.ellipse(
            (28, 28, 52, 52),
            fill=(0, 0, 0, 0),
        )

        imagens_engrenagem.append(imagem_engrenagem)

    icone_configuracoes = ctk.CTkImage(
        light_image=imagens_engrenagem[0],
        dark_image=imagens_engrenagem[1],
        size=(16, 16),
    )

    btn_configuracoes = ctk.CTkButton(
        tela_principal,
        text="",
        image=icone_configuracoes,
        width=30,
        height=28,
        fg_color="transparent",
        hover_color=CORES["icone_hover"],
        command=abrir_configuracoes,
    )
    btn_configuracoes.pack(side="right", padx=(0, 23), pady=(0, 10))

    # Segunda tela: criada agora, mas exibida apenas quando clicar na engrenagem

    tela_configuracoes = ctk.CTkFrame(
        janela,
        fg_color="transparent",
    )

    # TITULO ASPAS SIMPLES TELA CONFIGURACOES

    titulo_configuracoes = ctk.CTkLabel(
        tela_configuracoes,
        text="Aspas simples",
        width=147,
        height=28,
        corner_radius=8,
        fg_color=CORES["fundo_titulo"],
        text_color=CORES["texto_titulo"],
        font=("Inter", 13, "bold"),
    )
    titulo_configuracoes.pack(anchor="w", padx=15, pady=(15, 0))

    # Linha da configuração de separador do Varchar
    linha_separador_varchar = ctk.CTkFrame(
        tela_configuracoes,
        fg_color="transparent",
    )
    linha_separador_varchar.pack(fill="x", padx=15, pady=(10, 0))

    rotulo_separador_varchar = ctk.CTkLabel(
        linha_separador_varchar,
        text="Separador",
        font=("Inter", 13),
        text_color=CORES["texto_configuracao"],
        height=24,
    )
    rotulo_separador_varchar.pack(side="left")

    campo_separador_varchar = ctk.CTkEntry(
        linha_separador_varchar,
        width=50,
        height=24,
        font=("Inter", 13),
        justify="center",
        corner_radius=8,
        fg_color=CORES["fundo_separador"],
        text_color=CORES["texto_separador"],
        border_color=CORES["borda_separador"],
    )
    campo_separador_varchar.pack(side="right", padx=(0, 6))

    campo_separador_varchar.insert(
        0,
        configuracoes["varchar"]["separador"],
    )

    # Linha da configuração de espaço do Varchar

    linha_espaco_varchar = ctk.CTkFrame(
        tela_configuracoes,
        fg_color="transparent",
    )
    linha_espaco_varchar.pack(fill="x", padx=15, pady=(5, 0))

    rotulo_espaco_varchar = ctk.CTkLabel(
        linha_espaco_varchar,
        text="Espaço após o separador",
        font=("Inter", 13),
        text_color=CORES["texto_configuracao"],
        height=24,
    )
    rotulo_espaco_varchar.pack(side="left")

    opcao_espaco_varchar = ctk.CTkSwitch(
        linha_espaco_varchar,
        text="",
        width=40,
        height=24,
        switch_width=34,  # tamanho da barra
        switch_height=18, # tamanho da barra
        corner_radius=9, # arredondamento
        border_width=0, # remove a borda que reduz a área colorida da barra, deixando-a com a altura completa
        button_length=0, # - remove o trecho reto adicional do marcador. As extremidades arredondadas continuam sendo desenhadas, formando um
        fg_color=CORES["switch_desligado"], # cor da barra desligada                           círculo — o zero não faz o marcador desaparecer.
        progress_color=CORES["acao_verde"], # cor da barra ligada
        button_color=CORES["switch_circulo"], # cor do círculo
        button_hover_color=CORES["switch_circulo_hover"],
        onvalue=1, # valor de ligado
        offvalue=0, # valor de desligado
    )
    opcao_espaco_varchar.pack(side="right")

    if configuracoes["varchar"]["espaco_apos_separador"]:
        opcao_espaco_varchar.select()
    else:
        opcao_espaco_varchar.deselect()

    # Linha da configuração de parênteses do Varchar

    linha_parenteses_varchar = ctk.CTkFrame(
        tela_configuracoes,
        fg_color="transparent"
    )
    linha_parenteses_varchar.pack(fill="x", padx=15, pady=(5, 0))

    rotulo_parenteses_varchar = ctk.CTkLabel(
        linha_parenteses_varchar,
        text="Envolver em parênteses",
        font=("Inter", 13),
        text_color=CORES["texto_configuracao"],
        height=24,
    )
    rotulo_parenteses_varchar.pack(side="left")

    opcao_parenteses_varchar = ctk.CTkSwitch(
        linha_parenteses_varchar,
        text="",
        width=40,
        height=24,
        switch_width=34,
        switch_height=18,
        corner_radius=9,
        border_width=0,
        button_length=0,
        fg_color=CORES["switch_desligado"],
        progress_color=CORES["acao_verde"],
        button_color=CORES["switch_circulo"],
        button_hover_color=CORES["switch_circulo_hover"],
        onvalue=1,
        offvalue=0,
    )
    opcao_parenteses_varchar.pack(side="right")

    if configuracoes["varchar"]["fechar_parenteses"]:
        opcao_parenteses_varchar.select()
    else:
        opcao_parenteses_varchar.deselect()

    # CONFIGURACOES SEM ASPAS INT

    # TITULO 
    titulo_int = ctk.CTkLabel(
        tela_configuracoes,
        text="Sem aspas",
        width=147,
        height=28,
        corner_radius=8,
        fg_color=CORES["fundo_titulo"],
        text_color=CORES["texto_titulo"],
        font=("Inter", 13, "bold"),
    )
    titulo_int.pack(anchor="w", padx=15, pady=(20, 0))

    # Linha da configuração de separador do Int

    linha_separador_int = ctk.CTkFrame(
        tela_configuracoes,
        fg_color="transparent",
    )
    linha_separador_int.pack(fill="x", padx=15, pady=(10, 0))

    rotulo_separador_int = ctk.CTkLabel(
        linha_separador_int,
        text="Separador",
        font=("Inter", 13),
        text_color=CORES["texto_configuracao"],
        height=24,
    )
    rotulo_separador_int.pack(side="left")

    campo_separador_int = ctk.CTkEntry(
        linha_separador_int,
        width=50,
        height=24,
        font=("Inter", 13),
        justify="center",
        corner_radius=8,
        fg_color=CORES["fundo_separador"],
        text_color=CORES["texto_separador"],
        border_color=CORES["borda_separador"],
    )
    campo_separador_int.pack(side="right", padx=(0, 6))

    campo_separador_int.insert(
        0,
        configuracoes["virgula"]["separador"],
    )

    # Linha da configuração de espaço do Int
    linha_espaco_int = ctk.CTkFrame(
        tela_configuracoes,
        fg_color="transparent",
    )
    linha_espaco_int.pack(fill="x", padx=15, pady=(5, 0))

    rotulo_espaco_int = ctk.CTkLabel(
        linha_espaco_int,
        text="Espaço após o separador",
        font=("Inter", 13),
        text_color=CORES["texto_configuracao"],
        height=24,
    )
    rotulo_espaco_int.pack(side="left")

    opcao_espaco_int = ctk.CTkSwitch(
        linha_espaco_int,
        text="",
        width=40,
        height=24,
        switch_width=34,
        switch_height=18,
        corner_radius=9,
        border_width=0,
        button_length=0,
        fg_color=CORES["switch_desligado"],
        progress_color=CORES["acao_verde"],
        button_color=CORES["switch_circulo"],
        button_hover_color=CORES["switch_circulo_hover"],
        onvalue=1,
        offvalue=0,
    )
    opcao_espaco_int.pack(side="right")

    if configuracoes["virgula"]["espaco_apos_separador"]:
        opcao_espaco_int.select()
    else:
        opcao_espaco_int.deselect()

    # Linha da configuração de parênteses do Int
    linha_parenteses_int = ctk.CTkFrame(
        tela_configuracoes,
        fg_color="transparent",
    )
    linha_parenteses_int.pack(fill="x", padx=15, pady=(5, 0))

    rotulo_parenteses_int = ctk.CTkLabel(
        linha_parenteses_int,
        text="Envolver em parênteses",
        font=("Inter", 13),
        text_color=CORES["texto_configuracao"],
        height=24,
    )
    rotulo_parenteses_int.pack(side="left")

    opcao_parenteses_int = ctk.CTkSwitch(
        linha_parenteses_int,
        text="",
        width=40,
        height=24,
        switch_width=34,
        switch_height=18,
        corner_radius=9,
        border_width=0,
        button_length=0,
        fg_color=CORES["switch_desligado"],
        progress_color=CORES["acao_verde"],
        button_color=CORES["switch_circulo"],
        button_hover_color=CORES["switch_circulo_hover"],
        onvalue=1,
        offvalue=0,
    )
    opcao_parenteses_int.pack(side="right")

    if configuracoes["virgula"]["fechar_parenteses"]:
        opcao_parenteses_int.select()
    else:
        opcao_parenteses_int.deselect()

    # RODAPÉ TELA DE CONFIGURACOES

    rodape_configuracoes = ctk.CTkFrame(
        tela_configuracoes,
        fg_color="transparent",
    )
    rodape_configuracoes.pack(
        side="bottom",
        fill="x",
        padx=15,
        pady=(10, 20),
    )

    rodape_configuracoes.grid_columnconfigure(0, weight=1, uniform="laterais")
    rodape_configuracoes.grid_columnconfigure(1, weight=0)
    rodape_configuracoes.grid_columnconfigure(2, weight=1, uniform="laterais")

    btn_tema = ctk.CTkButton(
        rodape_configuracoes,
        text="",
        image=criar_icone_tema(),
        width=40,
        height=24,
        border_spacing=0,
        fg_color="transparent",
        hover=False,
        command=alternar_tema,
    )
    btn_tema.grid(row=0, column=0, sticky="w")

    # BOTAO SALVAR

    btn_salvar = ctk.CTkButton(
        rodape_configuracoes,
        text="Salvar",
        width=95,
        height=28,
        font=("Inter SemiBold", 13),
        fg_color=CORES["acao_verde"],
        text_color=CORES["texto_botao"],
        hover_color=CORES["acao_verde_hover"],
        command=salvar_configuracoes,
    )
    btn_salvar.grid(row=0, column=1)

    # Desenha uma versão da seta para cada tema
    imagens_seta = []

    for cor in CORES["icone_voltar"]:
        imagem_seta = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
        desenho_seta = ImageDraw.Draw(imagem_seta)

        desenho_seta.line(
            [(32, 20), (8, 20)],
            fill=cor,
            width=3,
        )
        desenho_seta.line(
            [(18, 10), (8, 20), (18, 30)],
            fill=cor,
            width=3,
        )

        imagens_seta.append(imagem_seta)

    icone_voltar = ctk.CTkImage(
        light_image=imagens_seta[0],
        dark_image=imagens_seta[1],
        size=(20, 20),
    )

    btn_voltar = ctk.CTkButton(
        rodape_configuracoes,
        text="",
        image=icone_voltar,
        width=30,
        height=28,
        fg_color="transparent",
        hover_color=CORES["icone_hover"],
        command=voltar_para_principal,
    )
    btn_voltar.grid(row=0, column=2, sticky="e", padx=(0, 6)) # sticky="e" posiciona a seta na extremidade direita de sua coluna

    # Trata cliques fora dos campos na tela de configuracoes 

    janela.bind(
        "<Button-1>",
        ajustar_foco_configuracoes,
        add="+",
    )

    alterar_modo("varchar") # força atualização para o modo padrão ao abrir o programa

    # Mantém a janela transparente enquanto calcula sua posição
    
    janela.attributes("-alpha", 0.0)
    janela.deiconify()
    janela.update()

    # Mede as bordas e a barra de título do Windows
    borda = janela.winfo_rootx() - janela.winfo_x()
    topo = janela.winfo_rooty() - janela.winfo_y()

    # Mede o tamanho total da janela, considerando a escala
    largura_real = janela.winfo_width() + (2 * borda)
    altura_real = janela.winfo_height() + topo + borda

    # Calcula o centro da tela
    x = (janela.winfo_screenwidth() - largura_real) // 2
    y = (janela.winfo_screenheight() - altura_real) // 2

    # Aplica a posição antes de tornar a janela visível
    janela.geometry(f"+{x}+{y}")
    janela.update_idletasks()

    # Prepara a ativação da minimização ao receber foco
    vinculo_ativacao_minimizacao = janela.bind(
        "<FocusIn>",
        ativar_minimizacao,
        add="+",
    )

    # Revela a janela pronta e direciona o foco para ela
    janela.attributes("-alpha", 1.0)
    janela.focus_force()

    # 3. Inicia o loop da janela 
    janela.mainloop()

carregar_configuracoes()
ctk.set_appearance_mode(tema_atual)
criar_interface()
