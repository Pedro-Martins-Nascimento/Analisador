# 📂 Analisador de Moda - Uploader de Arquivos

Este projeto é uma interface gráfica de usuário (GUI) desenvolvida em Python para upload e gerenciamento de arquivos, simulando um "Analisador de Moda".

A interface permite que os usuários:
- Selecionem arquivos clicando ou arrastando e soltando (drag-and-drop)
- Visualizem os arquivos selecionados
- Removam arquivos individualmente
- Iniciem um processo de "análise" (atualmente simulado)

---

## ✨ Funcionalidades

- **Interface Moderna Escura:** Interface agradável com `customtkinter`
- **Seleção de Arquivos Múltipla:**
  - Clicando no botão ou na área designada
  - Suporte a arrastar e soltar (drag-and-drop)
- **Listagem de Arquivos:** Mostra os arquivos com rolagem
- **Remoção Individual:** Cada arquivo tem um botão "X" para remover
- **Adicionar Mais Arquivos:** Botão para adicionar arquivos à seleção
- **Feedback de Processamento:**
  - Modal de “Processando...” com barra de progresso indeterminada
  - Simulação em thread separada para não travar a interface
- **Limpeza Automática:** Lista de arquivos é limpa após o processamento

---

## 🖼️ Captura de Tela

> Substitua abaixo pelo caminho da imagem da interface:

```markdown
![Analisador de Moda](caminho/para/sua/imagem.png)
```

---

## ✅ Pré-requisitos

- Python **3.7 ou superior**

---

## 📦 Instalação de Dependências

```bash
pip install customtkinter
pip install tkinterdnd2
```

> 💡 No Linux, a instalação do `tkinterdnd2` pode exigir dependências adicionais.

---

## 🚀 Como Executar

1. Clone este repositório ou baixe o arquivo `app.py`.

2. Acesse o diretório do projeto:

```bash
cd nome-do-projeto
```

3. (Opcional) Crie um ambiente virtual:

```bash
python -m venv venv
```

### Ativar:

#### Windows
```bash
venv\Scripts\activate
```

#### macOS/Linux
```bash
source venv/bin/activate
```

4. Instale as dependências:

```bash
pip install customtkinter tkinterdnd2
```

5. Execute a aplicação:

```bash
python app.py
```

---

## 🧠 Estrutura do Código (`app.py`)

- **Importações:** bibliotecas necessárias (`customtkinter`, `tkinterdnd2`, `threading`, etc.)
- **AppBaseClass:** Decide se herda de `TkinterDnD.Tk` ou `CTk`
- **Classe Principal - `FileUploaderApp`:**
  - `__init__`: Define tema e inicializa UI
  - `_create_widgets`: Cria a interface
  - `update_unified_area`: Atualiza área de arquivos
  - `handle_main_frame_click`: Abre seletor de arquivos
  - `handle_drag_enter_main`, `handle_drag_leave_main`, `handle_drop_event`: Gerenciam DnD
  - `select_files_dialog`: Abre diálogo do sistema
  - `remove_file`: Remove arquivo da lista
  - `upload_files_action`: Inicia processamento
  - `show_processing_window` e `hide_processing_window`: Modal de progresso
  - `actual_processing_logic`: Simula análise (thread)
  - `on_processing_finished`: Limpa a interface

---

## 🔧 Possíveis Melhorias Futuras

- Integração real com API de análise de moda
- Tratamento de erros de API
- Barra de progresso real
- Validação de tipos de arquivos
- Miniaturas para imagens
- Suporte a múltiplos idiomas (i18n)
- Empacotamento com PyInstaller ou cx_Freeze

---

## 🤝 Contribuições

Contribuições são bem-vindas!  
Abra uma issue ou envie um pull request.

---

## 📝 Observações

- Salve este conteúdo como `README.md` na raiz do projeto.
- Substitua o caminho da imagem pela captura de tela real da interface.
