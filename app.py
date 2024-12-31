import PyPDF2
import streamlit as st

# Cambiar la fuente personalizada
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Añadir el logo
st.image("https://upload.wikimedia.org/wikipedia/commons/a/ab/Logo_TV_2015.png", width=150)

# Encabezado personalizado
st.markdown(
    """
    <h1 style="text-align: center; color: #4CAF50;">Extractor de Diplomas</h1>
    <p style="text-align: center;">Sube un archivo PDF y extrae los diplomas de los participantes ingresando sus DNIs separados por espacios.</p>
    """,
    unsafe_allow_html=True
)

# Subida de PDF y entrada de DNIs
pdf_file = st.file_uploader("Cargar el archivo PDF", type=["pdf"])
dni_input = st.text_area("Introduce los DNIs separados por espacios:")

# Botón para realizar la extracción
if st.button("Extraer Diplomas"):
    if pdf_file and dni_input:
        lista_dnis = dni_input.split()  # Divide los DNIs por espacios
        escritor = PyPDF2.PdfWriter()
        lector = PyPDF2.PdfReader(pdf_file)
        paginas_por_dni = []

        for i, pagina in enumerate(lector.pages):
            texto = pagina.extract_text()
            for dni in lista_dnis:
                if dni.strip() in texto:
                    paginas_por_dni.append(i)
                    if i + 1 < len(lector.pages):
                        paginas_por_dni.append(i + 1)
                    break

        paginas_por_dni = sorted(set(paginas_por_dni))
        for pagina in paginas_por_dni:
            escritor.add_page(lector.pages[pagina])

        with open("resultado.pdf", "wb") as salida:
            escritor.write(salida)
        
        st.success("¡Diplomas extraídos!")
        st.download_button("Descargar el PDF", data=open("resultado.pdf", "rb"), file_name="diplomas_filtrados.pdf")
    else:
        st.error("Por favor, carga un PDF e introduce los DNIs.")

# Botón para reiniciar la aplicación
if st.button("Nueva Extracción"):
    st.experimental_rerun()
