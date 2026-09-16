# Cateno 🗄️

O **Cateno** é um aplicativo desktop desenvolvido em Python com CustomTkinter para transformar listas copiadas em uma única linha, com formatação personalizável.

## 📘 Sobre o projeto

O projeto nasceu para facilitar a preparação de listas para cláusulas `IN` de SQL. Com o uso no dia a dia, também passou a ajudar em outras tarefas que exigem reunir valores separados por linhas.

Na versão 2, você pode escolher entre os modos **Aspas simples** e **Sem aspas** e configurar, separadamente para cada um:

- O separador entre os valores.
- A inclusão de um espaço após o separador.
- O uso de parênteses ao redor do resultado.

As configurações são salvas no computador e recuperadas ao abrir o aplicativo novamente.

## 📦 Versão disponível

O código-fonte deste repositório contém a versão 2 em desenvolvimento.

Os executáveis da Release `v1.0.0` correspondem à primeira versão e não incluem as novas configurações. A distribuição da versão 2 será disponibilizada após sua finalização.

## 💡 Exemplos de uso

Copie uma lista com um valor por linha, escolha o modo e clique em **Colar**. O Cateno formata os valores e exibe uma prévia. Clique em **Copiar** para obter o resultado completo.

**Lista copiada:**

```text
123
456
789
```

### Com as configurações padrão

Os dois modos começam usando vírgula, espaço após o separador e parênteses ao redor do resultado.

**Modo Aspas simples:**

```text
('123', '456', '789')
```

**Modo Sem aspas:**

```text
(123, 456, 789)
```

O modo **Sem aspas** também aceita letras e outros textos; ele não está limitado a números.

### Com configurações personalizadas

Por exemplo, no modo **Sem aspas**, configure:

- **Separador:** `;`
- **Espaço após o separador:** desligado.
- **Envolver em parênteses:** desligado.

Clique em **Salvar**. Ao colar novamente a lista, o resultado será:

```text
123;456;789
```

Cada modo mantém suas próprias configurações. A seta de voltar descarta as alterações que ainda não foram salvas.

> A prévia mostra até oito valores. O botão **Copiar** copia todos os valores formatados, mesmo quando a prévia termina em reticências.


## ✨ Funcionalidades

- Conversão de listas com um valor por linha em uma única linha.
- Remoção de linhas vazias e espaços no início e no fim de cada valor.
- Modo **Aspas simples**, que envolve cada valor em aspas simples.
- Modo **Sem aspas**, para números ou textos sem adicionar aspas.
- Configurações independentes para cada modo:
  - Separador personalizável.
  - Espaço opcional após o separador.
  - Parênteses opcionais ao redor do resultado.
- Gravação das preferências em JSON, com recuperação ao iniciar.
- Prévia dos primeiros oito valores e cópia do resultado completo.
- Botão para limpar a prévia e o resultado.
- Interface com temas claro e escuro, alternância imediata e preferência salva automaticamente.
- Abertura centralizada e minimização ao perder o foco.

Se o campo Separador estiver vazio ao salvar, o aplicativo utilizará uma vírgula.

As preferências ficam em `%LOCALAPPDATA%\Cateno\configuracoes.json`, na pasta de dados do usuário do Windows.

## 🛠️ Tecnologias utilizadas

- **Python 3:** lógica e funcionamento do aplicativo.
- **CustomTkinter e Tkinter:** interface gráfica e eventos.
- **Pyperclip:** leitura e escrita na área de transferência.
- **Pillow:** desenho dos ícones de navegação.
- **JSON:** formato utilizado para armazenar as configurações, por meio do módulo `json` do Python.
- **ctypes:** integração com recursos do Windows.
- **PyInstaller:** empacotamento da versão executável.

## 🎨 Aparência

A versão 2 reúne os temas claro e escuro no mesmo aplicativo.

Para alternar, abra as configurações e clique no controle com sol e lua, à esquerda do botão Salvar. A mudança é aplicada imediatamente, sem precisar salvar ou reiniciar.

O símbolo indica o tema em uso:

- **Sol:** tema claro.
- **Lua:** tema escuro.

A preferência é salva automaticamente e recuperada ao abrir o Cateno novamente.

Trocar o tema não salva as alterações pendentes nos campos de formatação. Essas alterações continuam dependendo do botão **Salvar**; a seta de voltar as descarta, mantendo o tema escolhido.

## 📥 Distribuição da versão 2

A distribuição da versão 2 está em preparação. O objetivo é disponibilizar um instalador para Windows, com acesso ao aplicativo por atalhos, sem exigir que o usuário extraia um ZIP ou organize manualmente os arquivos necessários.

O instalador ainda não está disponível. Enquanto isso, a versão 2 pode ser executada pelo código-fonte, seguindo as instruções abaixo.

## 🗂️ Versão 1

A Release `v1.0.0` oferece os pacotes separados **Dark Mode** e **Light Mode**. Esses arquivos correspondem à versão anterior e não incluem as configurações da versão 2.

## 🚀 Como baixar e usar a versão 1

Se você não é desenvolvedor e quer apenas usar a ferramenta, disponibilizo duas pastas prontas: Cateno DM (Escuro) e Cateno LM (Claro).

1. Acesse a aba **Releases** no canto direito do GitHub.
2. Baixe o arquivo .zip da versão que você preferir (DM ou LM).
3. Extraia a pasta no seu computador (recomendável salvar na pasta Documentos).
4. Entre na pasta extraída, clique com o botão direito no arquivo `Cateno.exe` e escolha **Fixar na barra de tarefas** para ter acesso rápido sempre que precisar!

⚠️ **ATENÇÃO:** Nunca arraste o arquivo `Cateno.exe` para fora da sua pasta original! Ele precisa ficar sempre ao lado da pasta `_internal` para funcionar corretamente (ali está o "motor" do programa). 
Se quiser um ícone na sua Área de Trabalho, clique com o botão direito no `Cateno.exe`, escolha **"Criar atalho"** e mova apenas o atalho criado.

⚠️ **Aviso de Segurança do Windows:** Como este é um aplicativo independente e sem assinatura digital corporativa, o Windows (SmartScreen) exibirá uma tela azul dizendo *"O Windows protegeu o seu computador"* na primeira vez que você abri-lo. Isso é normal! Para prosseguir, clique em **"Mais informações"** e depois no botão **"Executar assim mesmo"**.


## 💻 Como executar a versão 2 pelo código-fonte

As instruções abaixo são para Windows, com Python 3 e Git instalados.

1. Clone o repositório:

   ```powershell
   git clone https://github.com/lucasseib/cateno.git
   ```

2. Entre na pasta do projeto:

   ```powershell
   cd cateno
   ```

3. Crie um ambiente virtual:

   ```powershell
   python -m venv .venv
   ```

4. Instale as dependências nesse ambiente:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install customtkinter pyperclip Pillow
   ```

5. Execute o aplicativo:

   ```powershell
   .\.venv\Scripts\python.exe Cateno.py
   ```

Execute os comandos dentro da pasta do projeto. Mantenha os arquivos `cateno.ico` e `Inter-VariableFont_slnt,wght.ttf` junto de `Cateno.py`, pois são utilizados pela interface.

Nas próximas vezes, basta entrar na pasta do projeto e repetir o comando do passo 5.