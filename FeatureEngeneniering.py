# Importa el archivo .py
import Limpiezadatosenpy

# Llama a la función para obtener el DataFrame
df = Limpiezadatosenpy.df

import pandas as pd
# Leer el archivo CSV y convertirlo en un DataFrame
ocupacion_diaria = pd.read_csv("C:/Users/jpcan/OneDrive/Documentos/Andes Universidad/Proyecto de grado 1/Tesis final/hospital_data_with_occupancy.csv")
ocupacion_diaria['CodigoPrestador'] = ocupacion_diaria['CodigoPrestador'].astype(str)
# Convertir 'RangoDias' a solo fechas, eliminando las horas
ocupacion_diaria['RangoDias'] = pd.to_datetime(ocupacion_diaria['RangoDias']).dt.date

# Agrupar por CodigoPrestador y RangoDias, y sumar la columna Hospitaloccupancy
ocupacion_diaria_agrupada = ocupacion_diaria.groupby(['CodigoPrestador', 'RangoDias'], as_index=False)['Hospitaloccupancy'].sum()

# Mostrar el DataFrame agrupado y consolidado
print(ocupacion_diaria_agrupada.head())

# Realizar la unión entre ambos DataFrames usando 'left' para mantener todas las filas de df
df = df.merge(ocupacion_diaria, how='left', left_on=['CodigoPrestador', 'FechaIngreso'], right_on=['CodigoPrestador', 'RangoDias'])


import pandas as pd

# Asumiendo que tienes cargado tu dataset original en df
# Aquí solo cargarías tus datos reales en lugar de crear un DataFrame de ejemplo

# Eliminar las columnas no deseadas
columnas_a_eliminar = ['DestinoUsuario', 'EstadoSalida', 'CausaBasicaMuerteUrgencias', 
                       'FechaIngreso', 'HoraIngreso', 'FechaSalida', 'HoraSalida', 
                       'UnidadMedidaEdad', 'Ano',"NumeroFactura", "CodigoDiagnosticoPrincipal", 'CodigoDiagnosticoRelacionado_uno', 'CodigoDiagnosticoRelacionado_dos', 'CodigoDiagnosticoRelacionado_tres', 
                       "FechaHoraIngreso", "FechaHoraSalida", "CodMunicipio", "CodigoEAPB","CodigoPrestador", "CodDepto","RangoDias"]

df = df.drop(columns=columnas_a_eliminar)

df = df.dropna(subset=['Hospitaloccupancy'])