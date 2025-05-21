
import streamlit as st
import sqlite3

# Conectar con la base de datos
def get_connection():
    return sqlite3.connect("curriculo.db")

# Función para obtener criterios agrupados por competencia
def obtener_criterios(ciclo, area):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT competencia, id_criterio, criterio, descriptores, saberes_asociados
        FROM criterios
        WHERE ciclo = ? AND area = ?
        ORDER BY competencia, id_criterio
    """, (ciclo, area))
    datos = cursor.fetchall()
    conn.close()
    return datos

# Título general
st.sidebar.title("📚 Menú principal")
pagina = st.sidebar.radio("Ir a:", ["Inicio", "Crear unidad", "Programación", "Cobertura curricular", "Configuración curricular"])

if pagina == "Inicio":
    st.title("📘 Bienvenida al Planificador Curricular")
    st.markdown("Esta aplicación permite crear unidades didácticas a partir del currículo oficial con criterios e indicadores graduados.")
    st.markdown("Usa el menú lateral para navegar entre secciones.")

elif pagina == "Crear unidad":
    st.title("🧩 Crear unidad didáctica")

    conn = get_connection()
    cursor = conn.cursor()
    ciclos = sorted(set(row[0] for row in cursor.execute("SELECT DISTINCT ciclo FROM criterios")))
    areas = sorted(set(row[0] for row in cursor.execute("SELECT DISTINCT area FROM criterios")))
    conn.close()

    ciclo = st.selectbox("Selecciona el ciclo", ciclos)
    area = st.selectbox("Selecciona el área", areas)

    titulo = st.text_input("Título de la unidad")
    duracion = st.number_input("Duración (en semanas)", min_value=1, max_value=10)
    temporalizacion = st.text_input("Temporalización (ej. 1º trimestre)")

    criterios_seleccionados = []
    st.subheader("📌 Selección de criterios")
    criterios = obtener_criterios(ciclo, area)

    competencias = {}
    for comp, id_crit, texto, descriptores, saberes in criterios:
        if comp not in competencias:
            competencias[comp] = []
        competencias[comp].append((id_crit, texto, descriptores, saberes))

    for comp, lista in competencias.items():
        with st.expander(f"🔹 {comp}"):
            for id_crit, texto, descriptores, saberes in lista:
                if st.checkbox(f"{id_crit} - {texto}", key=id_crit):
                    indicadores = st.text_area(f"Indicadores ({id_crit})", value=descriptores or "")
                    saberes_lista = [s.strip() for s in (saberes or "").split(";") if s.strip()]
                    saberes_sel = st.multiselect(f"Saberes asociados ({id_crit})", options=saberes_lista, default=saberes_lista, key=f"sab_{id_crit}")
                    criterios_seleccionados.append({
                        "id": id_crit,
                        "texto": texto,
                        "indicadores": indicadores,
                        "saberes": saberes_sel,
                        "competencia": comp
                    })

    if st.button("💾 Guardar unidad"):
        st.success("Unidad guardada (aún sin almacenamiento persistente).")
        st.json({
            "titulo": titulo,
            "ciclo": ciclo,
            "area": area,
            "duracion": duracion,
            "temporalizacion": temporalizacion,
            "criterios": criterios_seleccionados
        })

elif pagina == "Programación":
    st.title("📋 Programación didáctica")
    st.markdown("Aquí se mostrarán las unidades didácticas creadas. (Próximamente)")

elif pagina == "Cobertura curricular":
    st.title("📈 Cobertura curricular")
    st.markdown("Visualización del grado de cobertura del currículo. (Próximamente)")

elif pagina == "Configuración curricular":
    st.title("⚙️ Configuración curricular")
    st.markdown("Aquí podrás editar los criterios o añadir indicadores graduados. (Próximamente)")
