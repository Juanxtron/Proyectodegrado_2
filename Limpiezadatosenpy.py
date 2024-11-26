import pandas as pd

# Leer el archivo CSV y convertirlo en un DataFrame
df = pd.read_csv("C:/Users/jpcan/OneDrive/Documentos/Andes Universidad/Proyecto de grado 1/BaseDatos/registro_atencion_unidad_observacion_urgencia.csv")


# Supongamos que ya has leído el archivo CSV en un DataFrame llamado df
# df = pd.read_csv('ruta/al/archivo.csv')



# Supongamos que ya has leído el archivo CSV en un DataFrame llamado df
# df = pd.read_csv('ruta/al/archivo.csv')

# Transformar los valores de 'Edad' a años dependiendo de 'UnidadMedidaEdad'
def transformar_edad(row):
    if row['UnidadMedidaEdad'] == 2:
        return row['Edad'] / 12  # Convertir meses a años
    elif row['UnidadMedidaEdad'] == 3:
        return row['Edad'] / 365  # Convertir días a años
    else:
        return row['Edad']  # Si ya está en años, no se modifica

df['Edad'] = df.apply(transformar_edad, axis=1)
df = df[df['CodDepto'] != 0.0]

# Asegurarse de que todos los valores en 'CodDepto' son cadenas de texto
df['CodDepto'] = df['CodDepto'].astype(str)



# Convertir 'CodDepto' a string para manejar todos los valores como texto
df['CodDepto'] = df['CodDepto'].astype(str)

# Eliminar decimales en valores que terminan en '.0'
df['CodDepto'] = df['CodDepto'].str.replace(r'\.0$', '', regex=True)

# Asegurarse de que '05' y '5' sean tratados como iguales (quitando ceros a la izquierda)
df['CodDepto'] = df['CodDepto'].str.lstrip('0')

# Eliminar registros donde 'CodDepto' sea '0' o esté vacío
df = df[df['CodDepto'].notna() & (df['CodDepto'] != '') & (df['CodDepto'] != '0')]

# Eliminar registros donde 'CodDepto' sea '0', NaN, o esté vacío
df = df[df['CodDepto'].notna() & (df['CodDepto'] != '') & (df['CodDepto'] != '0') & (df['CodDepto'] != 'nan')]

# Eliminar registros donde 'CodDepto' sea igual a '\\"\\'
df = df[df['CodDepto'] != r'\"\"']

# Convertir 'CodDepto' a string para manejar todos los valores como texto
df['CodMunicipio'] = df['CodMunicipio'].astype(str)

# Eliminar decimales en valores que terminan en '.0'
df['CodMunicipio'] = df['CodMunicipio'].str.replace(r'\.0$', '', regex=True)

# Asegurarse de que todos los valores tengan una longitud de 3 caracteres, añadiendo ceros a la izquierda si es necesario
df['CodMunicipio'] = df['CodMunicipio'].str.zfill(3)

# Convertir las columnas especificadas a tipo string (str)
columnas_a_convertir = ['CodigoPrestador', 'DestinoUsuario', 'TipoUsuario', 'UnidadMedidaEdad']

df[columnas_a_convertir] = df[columnas_a_convertir].astype(str)

# Supongamos que ya has leído el archivo CSV en un DataFrame llamado df
# df = pd.read_csv('ruta/al/archivo.csv')

# Combinar Fecha y Hora en una sola columna de tipo datetime para el ingreso y la salida
# Usar errors='coerce' para convertir fechas fuera de rango o mal formateadas a NaT
df['FechaHoraIngreso'] = pd.to_datetime(df['FechaIngreso'] + ' ' + df['HoraIngreso'], errors='coerce')
df['FechaHoraSalida'] = pd.to_datetime(df['FechaSalida'] + ' ' + df['HoraSalida'], errors='coerce')

# Calcular la diferencia en horas entre la fecha y hora de ingreso y de salida, ignorando valores NaT
df['TiempoenUrgencias'] = (df['FechaHoraSalida'] - df['FechaHoraIngreso']).dt.total_seconds() / 3600

# Eliminar los registros con diferencias negativas o iguales a 0
df = df[df['TiempoenUrgencias'] > 0]

df['Ano'] = df['Ano'].astype(str)


# Supongamos que ya has leído el archivo CSV en un DataFrame llamado df
# df = pd.read_csv('ruta/al/archivo.csv')
df['CausaExterna'] = df['CausaExterna'].astype(str)

# Definir los mapeos para cada columna según la descripción proporcionada
mapa_causa_externa = {
    "1": "Accidente de trabajo",
    "2": "Accidente de tránsito",
    "3": "Accidente rábico",
    "4": "Accidente ofídico",
    "5": "Otro tipo de accidente",
    "6": "Evento catastrófico",
    "7": "Lesión por agresión",
    "8": "Lesión auto infligida",
    "9": "Sospecha de maltrato físico",
    "10": "Sospecha de abuso sexual",
    "11": "Sospecha de violencia sexual",
    "12": "Sospecha de maltrato emocional",
    "13": "Enfermedad general",
    "14": "Enfermedad laboral",
    "15": "Otra"
}

mapa_destino_usuario = {
    "1": "Alta de urgencias",
    "2": "Remisión a otro nivel de complejidad",
    "3": "Hospitalización"
}

mapa_tipo_usuario = {
    "1": "Contributivo",
    "2": "Subsidiado",
    "3": "Vinculado",
    "4": "Particular",
    "5": "Otro",
    "6": "Víctima con afiliación al Régimen Contributivo",
    "7": "Víctima con afiliación al Régimen subsidiado",
    "8": "Víctima no asegurado (Vinculado)"
}

mapa_unidad_medida_edad = {
    "1": "Años",
    "2": "Meses",
    "3": "Días"
}

# Aplicar los mapeos a las respectivas columnas
df['CausaExterna'] = df['CausaExterna'].map(mapa_causa_externa)
df['DestinoUsuario'] = df['DestinoUsuario'].map(mapa_destino_usuario)
df['TipoUsuario'] = df['TipoUsuario'].map(mapa_tipo_usuario)
df['UnidadMedidaEdad'] = df['UnidadMedidaEdad'].map(mapa_unidad_medida_edad)


# Leer el archivo Excel utilizando el motor "xlrd"
df_Codigos_IPS = pd.read_excel("C:/Users/jpcan/OneDrive/Documentos/Andes Universidad/Proyecto de grado 1/BaseDatos/CodigosIPS.xlsx")


# Asegurar que los códigos de sede tengan dos dígitos en df_Codigos_IPS
df_Codigos_IPS['numero_sede'] = df_Codigos_IPS['numero_sede'].astype(str).str.zfill(2)

# Crear una nueva columna que concatene codigo_prestador y numero_sede en df_Codigos_IPS
df_Codigos_IPS['CodigoPrestadorCompleto'] = df_Codigos_IPS['codigo_prestador'].astype(str) + df_Codigos_IPS['numero_sede']

# Crear un diccionario para mapear CodigoPrestador con "nombre_Prestador - sede nombre"
codigo_dict = df_Codigos_IPS.set_index('CodigoPrestadorCompleto').apply(
    lambda row: f"{row['nombre_prestador']} - sede {row['nombre']}", axis=1
).to_dict()

# Agregar manualmente los códigos que mencionas
codigo_dict['50010425913'] = 'VIDA SANA IPS LTDA'
codigo_dict['50010558603'] = 'CLÍNICA VIDA SEDE HOSPITALARIA'

# Mapear 'CodigoPrestador' usando el diccionario, pero si no se encuentra una coincidencia, deja el valor original
df['NombrePrestadorSede'] = df['CodigoPrestador'].map(codigo_dict).fillna(df['CodigoPrestador'])

# Leer el archivo Excel utilizando el motor "xlrd"
df_Codigos_EPS = pd.read_excel("C:/Users/jpcan/OneDrive/Documentos/Andes Universidad/Proyecto de grado 1/BaseDatos/CodigosEPS.xlsx")

# Asegurarse de que ambas columnas que se van a unir estén en el mismo formato (str)
df['CodigoEAPB'] = df['CodigoEAPB'].astype(str)
df_Codigos_EPS['CodigoEAPB'] = df_Codigos_EPS['CodigoEAPB'].astype(str)

# Crear un diccionario para mapear CodigoEAPB con NombreEAPB
eps_dict = df_Codigos_EPS.set_index('CodigoEAPB')['NombreEAPB'].to_dict()

# Crear la nueva columna en df utilizando el diccionario de mapeo
df['nombreEAPB'] = df['CodigoEAPB'].map(eps_dict)

# Eliminar filas que tengan NaN en la columna 'nombreEAPB'
df = df.dropna(subset=['nombreEAPB'])

# Leer el archivo Excel utilizando el motor "xlrd"
df_Codigos_Depto_Municipio = pd.read_excel("C:/Users/jpcan/OneDrive/Documentos/Andes Universidad/Proyecto de grado 1/BaseDatos/CodigoDeptoMun.xlsx")

# Eliminar la primera fila que tiene valores NaN
df_Codigos_Depto_Municipio = df_Codigos_Depto_Municipio.dropna().reset_index(drop=True)

# Convertir los valores de 'Código Departamento' y 'Código Municipio' a enteros y luego a cadenas con formato específico
df_Codigos_Depto_Municipio['Código Departamento'] = df_Codigos_Depto_Municipio['Código Departamento'].astype(int).astype(str).str.zfill(2)
df_Codigos_Depto_Municipio['Código Municipio'] = df_Codigos_Depto_Municipio['Código Municipio'].astype(int).astype(str).str.zfill(3)


df['CodDepto'] = df['CodDepto'].astype(int).astype(str).str.zfill(2)

# Asegúrate de que las columnas CodDepto y CodMunicipio en df tengan el formato correcto
df['CodDepto'] = df['CodDepto'].astype(str).str.zfill(2)
df['CodMunicipio'] = df['CodMunicipio'].astype(str).str.zfill(3)

# Crear diccionarios de mapeo
depto_dict = df_Codigos_Depto_Municipio.set_index(['Código Departamento'])['Departamento'].to_dict()
municipio_dict = df_Codigos_Depto_Municipio.set_index(['Código Departamento', 'Código Municipio'])['Municipio'].to_dict()

# Mapear los nombres de departamentos y municipios a las nuevas columnas en df
df['NombreDepto'] = df['CodDepto'].map(depto_dict)
df['NombreMunicipio'] = df.set_index(['CodDepto', 'CodMunicipio']).index.map(municipio_dict)

# Eliminar filas que tengan NaN en la columna 'nombreEAPB'
df = df.dropna(subset=['NombreMunicipio'])

import re

def tiene_formato_incorrecto(cadena):
    # Detectar si la cadena contiene un paréntesis abierto '(' o cerrado ')'
    if isinstance(cadena, str) and (re.search(r'\(.*', cadena) or re.search(r'.*\)', cadena)):
        return True
    return False

# Filtrar las filas que no tienen el formato incorrecto en las columnas especificadas
df = df[
    ~df['NombreMunicipio'].apply(tiene_formato_incorrecto) 

]

# Renombrar las columnas
df = df.rename(columns={
    'CodigoDiagnosticoPrincipalSalida': 'CodigoDiagnosticoPrincipal',
    'CodigoDiagnosticoRelN1Salida': 'CodigoDiagnosticoRelacionado_uno',
    'CodigoDiagnosticoRelN2Salida': 'CodigoDiagnosticoRelacionado_dos',
    'CodigoDiagnosticoRelN3Salida': 'CodigoDiagnosticoRelacionado_tres'
})

import pandas as pd

# Cargar el archivo de Excel
ruta_excel = "C:\\Users\\jpcan\\OneDrive\\Documentos\\Andes Universidad\\Proyecto de grado 1\\BaseDatos\\Codigos_finales_CIE10.xlsx"
df_Cie10 = pd.read_excel(ruta_excel, sheet_name="Hoja2")

# Convertir la columna 'Codigo-Enfermedad' a cadena de texto y eliminar espacios
df_Cie10['Codigo-Enfermedad'] = df_Cie10['Codigo-Enfermedad'].astype(str).str.strip()

# Eliminar guiones al inicio de las celdas y cualquier otro espacio
df_Cie10['Codigo-Enfermedad'] = df_Cie10['Codigo-Enfermedad'].str.lstrip('-').str.strip()

# Expresión regular para identificar el patrón de los códigos (letras seguidas de números y guiones)
codigo_pattern = r'^[A-Za-z0-9\-]+'

# Crear listas para almacenar códigos y descripciones
codigos = []
descripciones = []

# Recorrer cada fila y separar el código y la descripción con regex
for i, row in df_Cie10.iterrows():
    match = re.match(codigo_pattern, row['Codigo-Enfermedad'])
    
    if match:
        codigo = match.group(0)  # El código es el primer match del patrón
        descripcion = row['Codigo-Enfermedad'][len(codigo):].strip()  # El resto es la descripción
    else:
        codigo = row['Codigo-Enfermedad']
        descripcion = ''  # Descripción vacía si no hay match
    
    # Agregar los resultados a las listas
    codigos.append(codigo)
    descripciones.append(descripcion)

# Crear un nuevo DataFrame con los resultados
df_resultado = pd.DataFrame({
    'Codigo': codigos,
    'Descripción': descripciones
})


import pandas as pd

# Asegurarnos de que los códigos en el DataFrame estén en formato string
df['CodigoDiagnosticoPrincipal'] = df['CodigoDiagnosticoPrincipal'].astype(str)
df['CodigoDiagnosticoRelacionado_uno'] = df['CodigoDiagnosticoRelacionado_uno'].astype(str)
df['CodigoDiagnosticoRelacionado_dos'] = df['CodigoDiagnosticoRelacionado_dos'].astype(str)
df['CodigoDiagnosticoRelacionado_tres'] = df['CodigoDiagnosticoRelacionado_tres'].astype(str)

# Mapeo manual proporcionado
mapeo_manual = {
    "U071": "pneumonia or other manifestations",
    "U072": "Covid-19"
}


# Tabla general de capítulos de códigos CIE-10
tabla_general = {
    'A00-B99': 'Ciertas enfermedades infecciosas y parasitarias',
    'C00-D48': 'Neoplasias',
    'D50-D89': 'Enfermedades de la sangre y de los órganos hematopoyéticos y otros trastornos que afectan el mecanismo de la inmunidad',
    'E00-E90': 'Enfermedades endocrinas, nutricionales y metabólicas',
    'F00-F99': 'Trastornos mentales y del comportamiento',
    'G00-G99': 'Enfermedades del sistema nervioso',
    'H00-H59': 'Enfermedades del ojo y sus anexos',
    'H60-H95': 'Enfermedades del oído y de la apófisis mastoides',
    'I00-I99': 'Enfermedades del aparato circulatorio',
    'J00-J99': 'Enfermedades del aparato respiratorio',
    'K00-K93': 'Enfermedades del aparato digestivo',
    'L00-L99': 'Enfermedades de la piel y el tejido subcutáneo',
    'M00-M99': 'Enfermedades del sistema osteomuscular y del tejido conectivo',
    'N00-N99': 'Enfermedades del aparato genitourinario',
    'O00-O99': 'Embarazo, parto y puerperio',
    'P00-P96': 'Ciertas afecciones originadas en el periodo perinatal',
    'Q00-Q99': 'Malformaciones congénitas, deformidades y anomalías cromosómicas',
    'R00-R99': 'Síntomas, signos y hallazgos anormales clínicos y de laboratorio, no clasificados en otra parte',
    'S00-T98': 'Traumatismos, envenenamientos y algunas otras consecuencias de causa externa',
    'V01-Y98': 'Causas externas de morbilidad y de mortalidad',
    'Z00-Z99': 'Factores que influyen en el estado de salud y contacto con los servicios de salud',
    'U00-U99': 'Códigos para situaciones especiales'
}

# Crear un diccionario de mapeo de rangos a descripciones desde df_resultado
def obtener_mapeo_rango(df_resultado):
    mapeo = {}
    for _, row in df_resultado.iterrows():
        rango_codigo = row['Codigo']
        descripcion = row['Descripción']
        
        # Verificar si hay un guion en el código (indicando un rango)
        if '-' in rango_codigo:
            rango_inicial, rango_final = rango_codigo.split('-')
        else:
            # Si no hay guion, tratamos el código como un código individual
            rango_inicial = rango_codigo
            rango_final = rango_codigo

        mapeo[rango_inicial] = {'inicio': rango_inicial, 'fin': rango_final, 'descripcion': descripcion}
    return mapeo

# Crear el mapeo a partir de df_resultado
cie_10_mapeo_rangos = obtener_mapeo_rango(df_resultado)

# Función para buscar en la tabla general si no se encuentra en los rangos detallados
def buscar_en_tabla_general(codigo):
    for rango, descripcion in tabla_general.items():
        inicio, fin = rango.split('-')
        if inicio <= codigo <= fin:
            return descripcion
    return codigo  # Si no encuentra, devolver el código original

# Función para mapear el código usando mapeo manual y luego mapeo basado en rango
def mapear_codigo(codigo):
    if pd.isna(codigo):
        return codigo  # Si es nulo, dejar el código tal como está
    
    # Primero verificar en el mapeo manual
    if codigo in mapeo_manual:
        return mapeo_manual[codigo]
    
    # Luego verificar el código en los rangos de df_resultado
    codigo_base = codigo[:3]  # Los primeros tres caracteres del código
    for rango, valores in cie_10_mapeo_rangos.items():
        # Verificar si el código se encuentra en el rango
        if valores['inicio'] <= codigo_base <= valores['fin']:
            return valores['descripcion']
    
    # Si no se encuentra ni en el mapeo manual ni en los rangos, buscar en la tabla general
    return buscar_en_tabla_general(codigo_base)

# Aplicar el mapeo a las columnas de diagnóstico
df['DescripcionDiagnosticoPrincipal'] = df['CodigoDiagnosticoPrincipal'].apply(mapear_codigo)
df['DescripcionDiagnosticoRelacionado_uno'] = df['CodigoDiagnosticoRelacionado_uno'].apply(mapear_codigo)
df['DescripcionDiagnosticoRelacionado_dos'] = df['CodigoDiagnosticoRelacionado_dos'].apply(mapear_codigo)
df['DescripcionDiagnosticoRelacionado_tres'] = df['CodigoDiagnosticoRelacionado_tres'].apply(mapear_codigo)

# Mostrar el DataFrame resultante
print(df.head())

import numpy as np
# Reemplazar valores NaN y '""' con "No tuvo" en las columnas especificadas
df['DescripcionDiagnosticoPrincipal'].replace({np.nan: "No tuvo", 'nan': "No tuvo", '\\"\\': "No tuvo"}, inplace=True)
df['DescripcionDiagnosticoRelacionado_uno'].replace({np.nan: "No tuvo", 'nan': "No tuvo", '\\"\\': "No tuvo"}, inplace=True)
df['DescripcionDiagnosticoRelacionado_dos'].replace({np.nan: "No tuvo", 'nan': "No tuvo", '\\"\\': "No tuvo"}, inplace=True)
df['DescripcionDiagnosticoRelacionado_tres'].replace({np.nan: "No tuvo", 'nan': "No tuvo", '\\"\\': "No tuvo"}, inplace=True)

df = df[df['Sexo'] != 'I']

# Definir el umbral de 0.5 horas (media hora)
umbral = 0.5

# Filtrar las filas donde TiempoenUrgencias es mayor o igual a media hora
df = df[df['TiempoenUrgencias'] >= umbral]

df['FechaIngreso'] = pd.to_datetime(df['FechaIngreso'], format='%Y-%m-%d').dt.date

# Eliminar las filas donde 'DescripcionDiagnosticoPrincipal' tenga valores nulos
df = df.dropna(subset=['DescripcionDiagnosticoPrincipal'])
df = df.dropna(subset=['NombrePrestadorSede'])

df = df[df['ZonaResidencia'] != r'\"\"']

df = df[df['Edad'] < 110]
# Crear el diccionario con los valores que deseas reemplazar manualmente
manual_mapping = {
    "50018509280": "Clínica del Norte S.A.",
    "50010480601": "Prosalco - Cooperativa de Trabajo Asociado",
    "50010558604": "Clínica Medellín S.A., sede norte",
    "50010558606": "Clínica Medellín S.A., sede oriente",
    "50010909901": "Hospital General de Medellín Luz Castro de Gutiérrez",
    "50011616301": "Bienestar IPS Sede Medellín"
}

# Reemplazar manualmente los valores en `NombrePrestadorSede` usando el código como clave
df["NombrePrestadorSede"] = df["NombrePrestadorSede"].replace(manual_mapping)
