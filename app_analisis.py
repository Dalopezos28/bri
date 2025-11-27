import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Datos del Compresor",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("📊 Análisis de Datos del Compresor")
st.markdown("---")

# Función para cargar y procesar el archivo
@st.cache_data
def cargar_datos(archivo):
    try:
        # Leer el CSV con separador punto y coma y decimal coma
        df = pd.read_csv(
            archivo, 
            sep=';',
            decimal=',',
            encoding='latin-1'
        )
        
        # Renombrar columnas para facilitar el trabajo
        df.columns = ['fecha', 'hora', 'estado_compresor', 'temperatura', 'presion']
        
        # Crear columna datetime combinando fecha y hora
        df['fecha_hora'] = pd.to_datetime(df['fecha'] + ' ' + df['hora'], format='%d.%m.%Y %H:%M:%S')
        
        # Convertir estado a string para mejor visualización
        df['estado_compresor'] = df['estado_compresor'].astype(str)
        
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return None

# Sidebar para cargar archivo
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Opción para cargar archivo o usar el predeterminado
    usar_archivo_default = st.checkbox("Usar archivo datos2.csv del proyecto", value=True)
    
    if usar_archivo_default:
        archivo = "datos2.csv"
        df = cargar_datos(archivo)
    else:
        archivo_subido = st.file_uploader("Cargar archivo CSV", type=['csv'])
        if archivo_subido is not None:
            df = cargar_datos(archivo_subido)
        else:
            df = None
    
    if df is not None:
        st.success(f"✅ Archivo cargado: {len(df):,} registros")
        
        # Filtros
        st.markdown("---")
        st.subheader("🔍 Filtros")
        
        # Filtro por estado del compresor
        estados = ['Todos'] + list(df['estado_compresor'].unique())
        estado_seleccionado = st.selectbox("Estado del compresor", estados)
        
        # Filtro por rango de fechas
        fecha_min = df['fecha_hora'].min().date()
        fecha_max = df['fecha_hora'].max().date()
        
        fecha_inicio = st.date_input("Fecha inicio", fecha_min, min_value=fecha_min, max_value=fecha_max)
        fecha_fin = st.date_input("Fecha fin", fecha_max, min_value=fecha_min, max_value=fecha_max)

# Contenido principal
if df is not None:
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if estado_seleccionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['estado_compresor'] == estado_seleccionado]
    
    df_filtrado = df_filtrado[
        (df_filtrado['fecha_hora'].dt.date >= fecha_inicio) &
        (df_filtrado['fecha_hora'].dt.date <= fecha_fin)
    ]
    
    # Tabs para organizar el contenido
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Resumen General", 
        "📉 Series Temporales", 
        "📊 Distribuciones",
        "🔄 Correlaciones",
        "📋 Datos Detallados"
    ])
    
    # TAB 1: RESUMEN GENERAL
    with tab1:
        st.header("Resumen Estadístico General")
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total de Registros",
                f"{len(df_filtrado):,}",
                help="Número total de mediciones"
            )
        
        with col2:
            temp_promedio = df_filtrado['temperatura'].mean()
            st.metric(
                "Temperatura Promedio",
                f"{temp_promedio:.1f} °C",
                help="Temperatura promedio de descarga"
            )
        
        with col3:
            presion_promedio = df_filtrado['presion'].mean()
            st.metric(
                "Presión Promedio",
                f"{presion_promedio:.2f} bar",
                help="Presión interna promedio"
            )
        
        with col4:
            # Calcular tiempo en cada estado
            conteo_estados = df_filtrado['estado_compresor'].value_counts()
            estado_dominante = conteo_estados.index[0]
            porcentaje = (conteo_estados.iloc[0] / len(df_filtrado)) * 100
            st.metric(
                "Estado Dominante",
                f"Estado {estado_dominante}",
                f"{porcentaje:.1f}%"
            )
        
        st.markdown("---")
        
        # Estadísticas detalladas
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Estadísticas de Temperatura")
            stats_temp = df_filtrado['temperatura'].describe()
            
            stats_df_temp = pd.DataFrame({
                'Métrica': ['Mínima', 'Máxima', 'Promedio', 'Mediana', 'Desv. Est.', 'Q1 (25%)', 'Q3 (75%)'],
                'Valor (°C)': [
                    f"{stats_temp['min']:.2f}",
                    f"{stats_temp['max']:.2f}",
                    f"{stats_temp['mean']:.2f}",
                    f"{stats_temp['50%']:.2f}",
                    f"{stats_temp['std']:.2f}",
                    f"{stats_temp['25%']:.2f}",
                    f"{stats_temp['75%']:.2f}"
                ]
            })
            st.dataframe(stats_df_temp, width='stretch', hide_index=True)
        
        with col2:
            st.subheader("📊 Estadísticas de Presión")
            stats_presion = df_filtrado['presion'].describe()
            
            stats_df_presion = pd.DataFrame({
                'Métrica': ['Mínima', 'Máxima', 'Promedio', 'Mediana', 'Desv. Est.', 'Q1 (25%)', 'Q3 (75%)'],
                'Valor (bar)': [
                    f"{stats_presion['min']:.3f}",
                    f"{stats_presion['max']:.3f}",
                    f"{stats_presion['mean']:.3f}",
                    f"{stats_presion['50%']:.3f}",
                    f"{stats_presion['std']:.3f}",
                    f"{stats_presion['25%']:.3f}",
                    f"{stats_presion['75%']:.3f}"
                ]
            })
            st.dataframe(stats_df_presion, width='stretch', hide_index=True)
        
        st.markdown("---")
        
        # Gráfico de torta para estados del compresor
        st.subheader("🔄 Distribución de Estados del Compresor")
        
        conteo_estados = df_filtrado['estado_compresor'].value_counts().reset_index()
        conteo_estados.columns = ['Estado', 'Cantidad']
        
        fig_pie = px.pie(
            conteo_estados,
            values='Cantidad',
            names='Estado',
            title='Distribución del Tiempo por Estado',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label+value')
        st.plotly_chart(fig_pie, width='stretch')
    
    # TAB 2: SERIES TEMPORALES
    with tab2:
        st.header("Series Temporales")
        
        # Gráfico de temperatura en el tiempo
        st.subheader("🌡️ Temperatura de Descarga en el Tiempo")
        
        fig_temp = go.Figure()
        
        for estado in df_filtrado['estado_compresor'].unique():
            df_estado = df_filtrado[df_filtrado['estado_compresor'] == estado]
            fig_temp.add_trace(go.Scatter(
                x=df_estado['fecha_hora'],
                y=df_estado['temperatura'],
                mode='lines',
                name=f'Estado {estado}',
                line=dict(width=1)
            ))
        
        fig_temp.update_layout(
            xaxis_title="Fecha y Hora",
            yaxis_title="Temperatura (°C)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_temp, width='stretch')
        
        # Gráfico de presión en el tiempo
        st.subheader("⚡ Presión Interna en el Tiempo")
        
        fig_presion = go.Figure()
        
        for estado in df_filtrado['estado_compresor'].unique():
            df_estado = df_filtrado[df_filtrado['estado_compresor'] == estado]
            fig_presion.add_trace(go.Scatter(
                x=df_estado['fecha_hora'],
                y=df_estado['presion'],
                mode='lines',
                name=f'Estado {estado}',
                line=dict(width=1)
            ))
        
        fig_presion.update_layout(
            xaxis_title="Fecha y Hora",
            yaxis_title="Presión (bar)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_presion, width='stretch')
        
        # Gráfico combinado con subplots
        st.subheader("📊 Vista Combinada: Temperatura y Presión")
        
        fig_combined = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Temperatura de Descarga', 'Presión Interna'),
            vertical_spacing=0.1
        )
        
        # Temperatura
        fig_combined.add_trace(
            go.Scatter(x=df_filtrado['fecha_hora'], y=df_filtrado['temperatura'],
                      mode='lines', name='Temperatura', line=dict(color='red', width=1)),
            row=1, col=1
        )
        
        # Presión
        fig_combined.add_trace(
            go.Scatter(x=df_filtrado['fecha_hora'], y=df_filtrado['presion'],
                      mode='lines', name='Presión', line=dict(color='blue', width=1)),
            row=2, col=1
        )
        
        fig_combined.update_xaxes(title_text="Fecha y Hora", row=2, col=1)
        fig_combined.update_yaxes(title_text="Temperatura (°C)", row=1, col=1)
        fig_combined.update_yaxes(title_text="Presión (bar)", row=2, col=1)
        fig_combined.update_layout(height=700, showlegend=True)
        
        st.plotly_chart(fig_combined, width='stretch')
    
    # TAB 3: DISTRIBUCIONES
    with tab3:
        st.header("Distribuciones de Variables")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma de temperatura
            st.subheader("📊 Distribución de Temperatura")
            fig_hist_temp = px.histogram(
                df_filtrado,
                x='temperatura',
                color='estado_compresor',
                nbins=50,
                title='Histograma de Temperatura por Estado',
                labels={'temperatura': 'Temperatura (°C)', 'estado_compresor': 'Estado'},
                marginal='box'
            )
            st.plotly_chart(fig_hist_temp, width='stretch')
            
            # Box plot de temperatura
            st.subheader("📦 Box Plot de Temperatura")
            fig_box_temp = px.box(
                df_filtrado,
                x='estado_compresor',
                y='temperatura',
                color='estado_compresor',
                title='Distribución de Temperatura por Estado',
                labels={'temperatura': 'Temperatura (°C)', 'estado_compresor': 'Estado'}
            )
            st.plotly_chart(fig_box_temp, width='stretch')
        
        with col2:
            # Histograma de presión
            st.subheader("📊 Distribución de Presión")
            fig_hist_presion = px.histogram(
                df_filtrado,
                x='presion',
                color='estado_compresor',
                nbins=50,
                title='Histograma de Presión por Estado',
                labels={'presion': 'Presión (bar)', 'estado_compresor': 'Estado'},
                marginal='box'
            )
            st.plotly_chart(fig_hist_presion, width='stretch')
            
            # Box plot de presión
            st.subheader("📦 Box Plot de Presión")
            fig_box_presion = px.box(
                df_filtrado,
                x='estado_compresor',
                y='presion',
                color='estado_compresor',
                title='Distribución de Presión por Estado',
                labels={'presion': 'Presión (bar)', 'estado_compresor': 'Estado'}
            )
            st.plotly_chart(fig_box_presion, width='stretch')
        
        # Violin plots
        st.markdown("---")
        st.subheader("🎻 Gráficos de Violín")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_violin_temp = px.violin(
                df_filtrado,
                x='estado_compresor',
                y='temperatura',
                color='estado_compresor',
                box=True,
                title='Violin Plot - Temperatura',
                labels={'temperatura': 'Temperatura (°C)', 'estado_compresor': 'Estado'}
            )
            st.plotly_chart(fig_violin_temp, width='stretch')
        
        with col2:
            fig_violin_presion = px.violin(
                df_filtrado,
                x='estado_compresor',
                y='presion',
                color='estado_compresor',
                box=True,
                title='Violin Plot - Presión',
                labels={'presion': 'Presión (bar)', 'estado_compresor': 'Estado'}
            )
            st.plotly_chart(fig_violin_presion, width='stretch')
    
    # TAB 4: CORRELACIONES
    with tab4:
        st.header("Análisis de Correlaciones")
        
        # Scatter plot temperatura vs presión
        st.subheader("🔗 Relación entre Temperatura y Presión")
        
        fig_scatter = px.scatter(
            df_filtrado,
            x='presion',
            y='temperatura',
            color='estado_compresor',
            title='Temperatura vs Presión por Estado del Compresor',
            labels={'presion': 'Presión (bar)', 'temperatura': 'Temperatura (°C)', 'estado_compresor': 'Estado'},
            opacity=0.6,
            trendline='ols'
        )
        st.plotly_chart(fig_scatter, width='stretch')
        
        # Matriz de correlación
        st.subheader("📊 Matriz de Correlación")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Calcular correlación
            df_numeric = df_filtrado[['temperatura', 'presion']].copy()
            corr_matrix = df_numeric.corr()
            
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=['Temperatura', 'Presión'],
                y=['Temperatura', 'Presión'],
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values,
                texttemplate='%{text:.3f}',
                textfont={"size": 16},
                colorbar=dict(title="Correlación")
            ))
            
            fig_corr.update_layout(
                title='Matriz de Correlación',
                height=400
            )
            st.plotly_chart(fig_corr, width='stretch')
        
        with col2:
            st.markdown("### Interpretación")
            corr_value = corr_matrix.loc['temperatura', 'presion']
            
            st.metric("Correlación Temperatura-Presión", f"{corr_value:.3f}")
            
            if abs(corr_value) > 0.7:
                st.info("🔴 Correlación fuerte")
            elif abs(corr_value) > 0.4:
                st.info("🟡 Correlación moderada")
            else:
                st.info("🟢 Correlación débil")
            
            st.markdown("""
            **Valores de correlación:**
            - 1.0: Correlación positiva perfecta
            - 0.0: Sin correlación
            - -1.0: Correlación negativa perfecta
            """)
        
        # Análisis por estado
        st.markdown("---")
        st.subheader("📈 Correlación por Estado del Compresor")
        
        estados_unicos = df_filtrado['estado_compresor'].unique()
        cols = st.columns(len(estados_unicos))
        
        for idx, estado in enumerate(sorted(estados_unicos)):
            df_estado = df_filtrado[df_filtrado['estado_compresor'] == estado]
            corr_estado = df_estado[['temperatura', 'presion']].corr().loc['temperatura', 'presion']
            
            with cols[idx]:
                st.metric(f"Estado {estado}", f"{corr_estado:.3f}")
    
    # TAB 5: DATOS DETALLADOS
    with tab5:
        st.header("Datos Detallados")
        
        # Mostrar información del dataset
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Total de registros:** {len(df_filtrado):,}")
        with col2:
            st.info(f"**Rango de fechas:** {df_filtrado['fecha_hora'].min().date()} a {df_filtrado['fecha_hora'].max().date()}")
        with col3:
            duracion = df_filtrado['fecha_hora'].max() - df_filtrado['fecha_hora'].min()
            st.info(f"**Duración:** {duracion.days} días, {duracion.seconds//3600} horas")
        
        st.markdown("---")
        
        # Opciones de visualización
        st.subheader("📋 Tabla de Datos")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            num_registros = st.number_input(
                "Número de registros a mostrar",
                min_value=10,
                max_value=1000,
                value=100,
                step=10
            )
        
        with col2:
            orden = st.selectbox(
                "Ordenar por",
                ['fecha_hora', 'temperatura', 'presion'],
                index=0
            )
            ascendente = st.checkbox("Orden ascendente", value=True)
        
        # Mostrar tabla
        df_mostrar = df_filtrado.sort_values(by=orden, ascending=ascendente).head(num_registros)
        
        st.dataframe(
            df_mostrar[['fecha_hora', 'estado_compresor', 'temperatura', 'presion']],
            width='stretch',
            hide_index=True
        )
        
        # Botón para descargar datos filtrados
        st.markdown("---")
        st.subheader("💾 Descargar Datos")
        
        csv = df_filtrado.to_csv(index=False, sep=';', decimal=',')
        st.download_button(
            label="📥 Descargar datos filtrados como CSV",
            data=csv,
            file_name=f"datos_compresor_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Estadísticas adicionales
        st.markdown("---")
        st.subheader("📊 Estadísticas Completas")
        
        st.dataframe(df_filtrado[['temperatura', 'presion']].describe(), width='stretch')

else:
    # Mensaje cuando no hay datos cargados
    st.info("👈 Por favor, carga un archivo CSV desde la barra lateral para comenzar el análisis.")
    
    st.markdown("""
    ### 📝 Formato esperado del archivo CSV:
    
    El archivo debe contener las siguientes columnas (separadas por punto y coma):
    1. **date** - Fecha en formato DD.MM.YYYY
    2. **time** - Hora en formato HH:MM:SS
    3. **Compressor status** - Estado del compresor (numérico)
    4. **Airend discharge temp. ADT / °C** - Temperatura de descarga en grados Celsius
    5. **Internal pressure / bar** - Presión interna en bar
    
    **Nota:** Los decimales deben estar separados por coma (,) en formato europeo.
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>💡 Desarrollado con Streamlit | 📊 Análisis de Datos del Compresor</p>
    </div>
    """,
    unsafe_allow_html=True
)

