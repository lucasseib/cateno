
import tkinter as tk
import customtkinter as ctk
import pyperclip
import ctypes
import sys
import os

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

def alterar_modo(novo_modo):
    global modo_atual
    modo_atual = novo_modo

    cor_ativa = "#9db64a"
    cor_inativa = "#8d8d8d"

    # Se o botão Varchar for clicado:
    if modo_atual == "varchar":
        btn_aba_varchar.configure(fg_color=cor_ativa, text_color="#ffffff", hover_color="#839738") 
        btn_aba_virgula.configure(fg_color=cor_inativa, text_color="#fff9ef", hover_color="#7b7b7b") 

    # Se o botão Vírgula for clicado:
    elif modo_atual == "virgula":
        btn_aba_varchar.configure(fg_color=cor_inativa, text_color="#fff9ef", hover_color="#7b7b7b")
        btn_aba_virgula.configure(fg_color=cor_ativa, text_color="#ffffff", hover_color="#839738") 

    limpar_tudo()

    print(f"O modo atual é: {modo_atual}")

#---------------------------------AVISO FLUTUANTE TEMPORÁRIO--------------------------------------#

def mostrar_aviso(mensagem):
    
    # Cria um "quadro" (Frame) dentro do janela do app
    popup = ctk.CTkFrame(janela, fg_color="#77bcc1", corner_radius=6, bg_color="#393939")
    
    # Cria o texto de aviso e coloca dentro do Frame
    lbl = ctk.CTkLabel(popup, text=mensagem, 
                       text_color="#FFFFFF",   # cor da letra
                       font=("Inter", 12),       # fonte
                       fg_color="transparent")    
    lbl.pack(padx=15, pady=6) # Controla o tamanho do balão (espaçamento interno)

    # O .place flutua o item por cima dos outros widgets da janela
    # relx=0.5 e rely=0.5 significa 50% do eixo X e Y (exatamente no centro)
    popup.place(relx=0.5, rely=0.5, anchor="center")

    # Destrói apenas o Frame após 1.5 segundos
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

    resultado_completo_sql = "(" + ", ".join(itens_formatados) + ")" # Junta tudo com vírgula, espaço e coloca os parênteses (usado nos dois modos)

    # 5. Cria o PREVIEW (8 itens)
    preview_itens = itens_formatados[:8]
    resumo = "(" + ", ".join(preview_itens)

    if len (itens_formatados) > 8:
        resumo += ", ..." # Adiciona as reticências quando tiver mais de 8 códigos

    resumo += ")"

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

#---------------------------------INTERFACE VISUAL--------------------------------------# 

def criar_interface():
    
    global campo_texto, janela, btn_aba_varchar, btn_aba_virgula

    # 1. Cria a janela principal
    janela = ctk.CTk()                    # abre o processo da janela no windows

    janela.withdraw()  # esconde a janela

    # Altera a cor do fundo
    janela.configure(fg_color="#1E1E1E") 

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

    janela.update() # força o CustomTkinter a desenhar e ler o tamanho do monitor

    largura_monitor = janela.winfo_screenwidth()
    altura_monitor = janela.winfo_screenheight()

    largura_app = 350
    altura_app = 175

    # Cálculo para deixar a janela no canto inferior direito
    x = largura_monitor - largura_app - 110
    y = altura_monitor - altura_app - 155

    janela.geometry(f"{largura_app}x{altura_app}+{x}+{y}")

#--------------------------------------------------------------------------------------#

    janela.bind("<FocusOut>", minimizar_ao_perder_foco)  # diz: se a janela perder o foco, execute a função minimizar_ao_perder_foco

    # Deixar a janela sempre visivel 
    #janela.attributes('-topmost', True)

#---------------------------------ABAS SUPERIORES--------------------------------------#
  
    frame_abas = ctk.CTkFrame(janela, fg_color="transparent") # transparent faz o frame sumir e misturar com o fundo da janela
    frame_abas.pack(pady=(15, 0)) # significa: (cima, baixo)

    btn_aba_varchar = ctk.CTkButton(frame_abas, text="('varchar',)", width=147, height=28, corner_radius=8,
                                    font=("Inter SemiBold", 13),
                                    command=lambda: alterar_modo("varchar"))   # corner_radius é o nivel de arredondamento das bordas
    btn_aba_varchar.pack(side="left", padx=(11, 5))

    btn_aba_virgula = ctk.CTkButton(frame_abas, text="(int,)", width=147, height=28, corner_radius=8,
                                    font=("Inter SemiBold", 13),
                                    command=lambda: alterar_modo("virgula"))
    btn_aba_virgula.pack(side="left", padx=(5, 11))

    #---------------------------------CAMPO TEXTO--------------------------------------#

    # Campo que permite várias linhas
    campo_texto = ctk.CTkTextbox(janela, width=305, height= 55, state='disabled', 
                                 fg_color="#393939", text_color="#F1FFBE", corner_radius=8, # backup fg_color light #e0e6ed  text 2F5600'
                                font=("Consolas", 13))
    campo_texto.pack(pady=(15, 0), padx=10) # pack () posiciona o elemento na tela, posiciona um embaixo do outro. pady é o espaço (padding) vertical 
      
    #---------------------------------BOTÕES INFERIORES--------------------------------------#

    # Organiza os botões lado a lado
    frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
    frame_botoes.pack(pady=(15, 15))

    # Botão 1: Colar
    btn_colar = ctk.CTkButton(frame_botoes, text="Colar", width=95, height=28, corner_radius=8,
                              font=("Inter SemiBold", 13),
                              fg_color="#77bcc1", text_color="#ffffff", hover_color="#669da0", # hover_color define a cor quando passa o mouse
                              command=processar_e_formatar)
    btn_colar.pack(side="left", padx=5)

    # Botão 2: Copiar 
    btn_copiar = ctk.CTkButton(frame_botoes, text="Copiar", width=95, height=28, corner_radius=8,
                               font=("Inter SemiBold", 13),
                               fg_color="#9db64a", text_color="#ffffff", hover_color="#839738",  # text color fff8ec # fg color aac552
                               command=copiar_para_clipboard)
    btn_copiar.pack(side="left",padx=5)

    # Botão 3: Limpar
    btn_limpar = ctk.CTkButton(frame_botoes, text="Limpar", width=95, height=28, corner_radius=8,
                               font=("Inter SemiBold", 13),
                               fg_color="#f4713d", text_color="#ffffff", hover_color="#d06034",
                               command=limpar_tudo)
    btn_limpar.pack(side="left", padx=5)

    alterar_modo("varchar") # força atualização para o modo padrão ao abrir o programa

    janela.deiconify()  # revela a janela pronta e no lugar certo

    # 3. Inicia o loop da janela 
    janela.mainloop()

criar_interface()
