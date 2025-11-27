@echo off
echo ========================================
echo   Iniciando Analisis de Datos del Compresor
echo ========================================
echo.
echo Verificando dependencias...
python -m pip install -r requirements.txt --quiet
echo.
echo Iniciando aplicacion Streamlit...
echo La aplicacion se abrira automaticamente en tu navegador.
echo.
echo Para detener la aplicacion, presiona Ctrl+C
echo ========================================
echo.
streamlit run app_analisis.py
pause

