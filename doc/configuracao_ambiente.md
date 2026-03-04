# Configuração do Ambiente Virtual (venv)

Este guia explica como criar e ativar um ambiente virtual Python para este projeto.

## 1. Pré-requisitos

Certifique-se de ter o Python instalado. Você pode verificar executando:

```bash
python --version
```

## 2. Criar o Ambiente Virtual

Execute o seguinte comando na raiz do projeto para criar uma pasta chamada `venv` contendo o ambiente isolado:

```bash
python -m venv venv
```

## 3. Ativar o Ambiente Virtual

### Windows (PowerShell)

```powershell
.\venv\Scripts\activate
```

_Nota: Se encontrar erro de permissão, pode ser necessário executar `Set-ExecutionPolicy Unrestricted -Scope Process` antes._

### Windows (CMD)

```cmd
venv\Scripts\activate.bat
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 4. Verificar Ativação

Após a ativação, o terminal deve mostrar `(venv)` no início da linha de comando.

## 5. Instalar Dependências

Com o ambiente ativado, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

## 6. Desativar

Para sair do ambiente virtual, basta executar:

```bash
deactivate
```

## 7. Executar a Aplicação

Para iniciar o dashboard localmente (localhost):

```powershell
streamlit run scripts/main_app.py
```
