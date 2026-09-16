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

O código-fonte deste repositório corresponde à versão 2 do Cateno.

O instalador da versão `2.0.0` foi gerado e testado localmente. Sua publicação no GitHub Releases está em preparação.

A Release `v1.0.0` permanece disponível como versão anterior, sem as novas configurações e a alternância de temas.

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
- **Inno Setup:** criação do instalador para Windows.

## 🎨 Aparência

A versão 2 reúne os temas claro e escuro no mesmo aplicativo.

Para alternar, abra as configurações e clique no controle com sol e lua, à esquerda do botão Salvar. A mudança é aplicada imediatamente, sem precisar salvar ou reiniciar.

O símbolo indica o tema em uso:

- **Sol:** tema claro.
- **Lua:** tema escuro.

A preferência é salva automaticamente e recuperada ao abrir o Cateno novamente.

Trocar o tema não salva as alterações pendentes nos campos de formatação. Essas alterações continuam dependendo do botão **Salvar**; a seta de voltar as descarta, mantendo o tema escolhido.

## 📥 Instalação da versão 2

A versão 2 utiliza um instalador para Windows que inclui o aplicativo e suas dependências. Não é necessário instalar Python nem extrair arquivos ZIP.

Após a publicação da Release `v2.0.0`:

1. Acesse [Releases](https://github.com/lucasseib/cateno/releases).
2. Baixe o arquivo `Cateno-Setup-2.0.0.exe`.
3. Execute o instalador e siga as instruções.
4. Se desejar, marque a opção de criar um atalho na Área de Trabalho.
5. Abra o Cateno pelo menu Iniciar ou pelo atalho criado.

A instalação é feita apenas para o usuário atual, sem solicitar privilégios de administrador. Em computadores corporativos, políticas da empresa ainda podem exigir liberação do TI.

### Acesso pela barra de tarefas

Abra o Cateno instalado, clique com o botão direito em seu ícone na barra de tarefas e selecione **Fixar na barra de tarefas**.

### Compartilhamento

Para compartilhar o aplicativo, envie somente `Cateno-Setup-2.0.0.exe`. O instalador já contém os arquivos necessários.

Depois da instalação, o arquivo de instalação pode ser apagado. Os arquivos instalados são gerenciados pelo instalador e não precisam ser movidos.

### Desinstalação

Para remover o aplicativo, procure **Cateno** na lista de aplicativos instalados nas Configurações do Windows e escolha **Desinstalar**.

As preferências em `%LOCALAPPDATA%\Cateno\configuracoes.json` são preservadas.

## 🗂️ Versão anterior

A Release `v1.0.0` permanece disponível com os pacotes separados Dark Mode e Light Mode. Ela não inclui as funcionalidades da versão 2.


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