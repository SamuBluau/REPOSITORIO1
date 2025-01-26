import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Generador de Input para Bibliometrix")
st.write("Sube tus archivos CSV exportados de Scopus, WoS o PubMed para crear un archivo limpio sin repeticiones de DOI.")

# Subida de archivos CSV
uploaded_files = st.file_uploader(
    "Sube uno o más archivos CSV", 
    type=["csv"], 
    accept_multiple_files=True
)

# Procesar archivos subidos
if uploaded_files:
    all_dataframes = []

    # Iterar sobre los archivos subidos
    for uploaded_file in uploaded_files:
        try:
            # Leer el archivo CSV
            df = pd.read_csv(uploaded_file)

            # Asegurarse de que exista la columna DOI
            if "DOI" not in df.columns:
                st.error(f"El archivo '{uploaded_file.name}' no contiene una columna llamada 'DOI'.")
                continue

            # Agregar los datos al conjunto
            all_dataframes.append(df)
            st.success(f"Archivo '{uploaded_file.name}' cargado exitosamente.")

        except Exception as e:
            st.error(f"Error al leer el archivo '{uploaded_file.name}': {e}")

    if all_dataframes:
        # Combinar todos los DataFrames
        combined_df = pd.concat(all_dataframes, ignore_index=True)

        # Eliminar duplicados basados en la columna DOI
        cleaned_df = combined_df.drop_duplicates(subset=["DOI"])

        st.write("### Vista previa de los datos procesados:")
        st.dataframe(cleaned_df.head())

        # Botón para descargar el archivo procesado
        st.cache_data(\n        
        def convert_df_to_csv(df):\n            
        return df.to_csv(index=False).encode('utf-8')\n\n        
        csv = convert_df_to_csv(cleaned_df)\n\n        
        st.download_button(\n            
        label=\"Descargar archivo limpio\",\n            
        data=csv,\n            
        file_name=\"input_bibliometrix.csv\",\n            
        mime=\"text/csv\"\n        
        )\n\n``
