# 📊 Análisis de Datos del Compresor

Aplicación web interactiva desarrollada con Streamlit para analizar datos de un compresor industrial.

## 📋 Características

La aplicación proporciona un análisis completo con las siguientes funcionalidades:

### 📈 Resumen General
- Métricas principales (total de registros, temperatura promedio, presión promedio)
- Estadísticas detalladas de temperatura y presión
- Distribución de estados del compresor

### 📉 Series Temporales
- Gráfico de temperatura de descarga en el tiempo
- Gráfico de presión interna en el tiempo
- Vista combinada de ambas variables

### 📊 Distribuciones
- Histogramas de temperatura y presión por estado
- Box plots para visualizar rangos y outliers
- Gráficos de violín para análisis de distribución detallado

### 🔄 Correlaciones
- Análisis de correlación entre temperatura y presión
- Matriz de correlación visual
- Análisis de correlación por estado del compresor

### 📋 Datos Detallados
- Tabla interactiva con los datos
- Opción de descarga de datos filtrados
- Estadísticas completas

## 🚀 Instalación

### 1. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
streamlit run app_analisis.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura de Archivos

```
├── app_analisis.py       # Aplicación principal de Streamlit
├── datos2.csv            # Archivo de datos del compresor
├── requirements.txt      # Dependencias de Python
└── README.md            # Este archivo
```

## 📊 Formato de Datos

El archivo CSV debe contener las siguientes columnas (separadas por punto y coma `;`):

1. **date** - Fecha en formato DD.MM.YYYY
2. **time** - Hora en formato HH:MM:SS
3. **Compressor status** - Estado del compresor (1 o 2)
4. **Airend discharge temp. ADT / °C** - Temperatura de descarga en grados Celsius
5. **Internal pressure / bar** - Presión interna en bar

**Nota:** Los decimales están separados por coma (`,`) en formato europeo.

## 🔍 Filtros Disponibles

La aplicación permite filtrar los datos por:
- **Estado del compresor** - Filtrar por estado específico o ver todos
- **Rango de fechas** - Seleccionar fecha de inicio y fin

## 💡 Uso

1. Al iniciar la aplicación, se carga automáticamente el archivo `datos2.csv`
2. Puedes usar los filtros en la barra lateral para personalizar el análisis
3. Navega por las diferentes pestañas para ver diferentes tipos de análisis
4. Descarga los datos filtrados desde la pestaña "Datos Detallados"

## 🛠️ Tecnologías Utilizadas

- **Streamlit** - Framework para la aplicación web
- **Pandas** - Procesamiento y análisis de datos
- **Plotly** - Gráficos interactivos
- **NumPy** - Operaciones numéricas

## 📝 Variables Analizadas

### Temperatura de Descarga (°C)
- Rango típico observado: 83-102°C
- Mediciones cada 30 segundos

### Presión Interna (bar)
- Rango típico observado: 1.5-8.2 bar
- Correlacionada con el estado del compresor

### Estado del Compresor
- **Estado 1**: Modo de operación 1
- **Estado 2**: Modo de operación 2

## 🎯 Casos de Uso

Esta aplicación es útil para:
- Monitoreo de rendimiento del compresor
- Detección de anomalías en temperatura y presión
- Análisis de patrones de operación
- Mantenimiento predictivo
- Generación de reportes

## 📞 Soporte

Para cualquier pregunta o problema, por favor contacta al desarrollador.

---

**Desarrollado con ❤️ usando Streamlit**

