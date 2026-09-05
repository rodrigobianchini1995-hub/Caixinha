@echo off
title Iniciando Dashboard Caixinha...
color 0A

:: Entra na pasta atual onde o script est
cd /d "%~dp0"

echo ===================================================
echo      DASHBOARD CAIXINHA - INICIALIZADOR
echo ===================================================
echo.

:: 1. Verifica se o Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado no seu computador!
    echo Por favor, peca para a pessoa instalar o Python (marcando a opcao "Add Python to PATH" durante a instalacao).
    echo Pressione qualquer tecla para sair...
    pause >nul
    exit
)

:: 2. Verifica se as ferramentas (Streamlit/Pandas) ja estao instaladas na pasta .venv
:: O streamlit.exe so vai existir se a instalacao tiver sido concluida.
if not exist ".venv\Scripts\streamlit.exe" (
    echo [AVISO] Primeira execucao detectada neste computador!
    echo [INFO] Preparando o ambiente e baixando bibliotecas... 
    echo Isso pode demorar alguns minutos. Por favor, aguarde e nao feche a tela...
    
    :: Se a pasta .venv existir (copiada por engano do Drive de outro pc), apagamos para evitar erro de caminho.
    if exist ".venv" rmdir /s /q ".venv"
    
    :: Cria o ambiente virtual
    python -m venv .venv
    
    :: Ativa o ambiente virtual
    call .venv\Scripts\activate.bat
    
    :: Atualiza o instalador e instala as dependencias que colocamos no requirements.txt
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
    
    echo.
    echo [SUCESSO] Ambiente preparado com sucesso!
) else (
    echo [INFO] Ambiente ja configurado. Ativando...
    call .venv\Scripts\activate.bat
)

:: 3. Inicia o Dashboard
echo [INFO] Iniciando o Dashboard...
echo Se o navegador nao abrir sozinho, acesse: http://localhost:8501
streamlit run app.py

pause
