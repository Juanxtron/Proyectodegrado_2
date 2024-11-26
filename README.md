# Proyectodegrado_2
En este repositorio, se encuentra 2 cuadernos de python donde se hace el análisis exploratorio y el desarrollo de los modelos. Ademas, hay .py adicionales donde se hace la limpieza de los datos y la ingenieria de caracteristicas

# Base de datos
La base de datos la pueden descargar en este link: https://medata.gov.co/dataset/1-026-22-000128. En el documento se puede ver el detalle de esta base de datos. Ademas, esta pagina ofrece una descripción general de cada una de las variables. 

# Mapeo datos
Para poder correr el archivo de Limpiezadatosenpy.py se necesitan los archivos CodigosIPS.xlsx, CodigosEPS.xlsx, CodigoDeptoMun.xlsx y Codigos_finales_CIE10.xlsx. Por otro lado, Para poder correr el de FeatureEngeneniering.py se necesita el archivo hospital_data_with_occupancy.csv. Todos estos archivos se adjuntan acá en el repositorio.

# Requerimientos para correr cuaderno.
Para poder correr los cuadernos de ModeloLineal y AnalisisExploratoriotesis se necesitan los .py LimpiezaDatosenpy y FeatureEngeneniering. Ademas, para correr el cuaderno de ModeloLineal en la parte de importancia variables, se necesita el modelo serializado. Para esto se puede correr el modelo y serializarlo (En el codigo esta como hacerlo). Sin embargo, para ahorrar trabajo adjunto el modelo serializado de Catboost. Adjunto solo este ya que este fue el seleccionado para la herramienta dado que fue el que mejor MAE en validación dio. Con este ya se puede correr la parte de "Analisis impacto variables modelo Catboost".

# Aclaración variable a predecir. 

Tanto en el codigo para los modelos de ML como en este cuaderno, la variable a predecir es TiempoenUrgencias. En el documento de proyecto de grado se menciona es TiempoenObservación. Esto fue por que a ultimo momento se cambio el nombre de la variable por tema de interpretación dado que aunque la unidad de observación haga parte de urgencias, se puede malinterpretar ese nombre dado que hay mas unidades en Urgencias. En este trabajo de grado me enfocare unicamente en la unidad de observación. Al mismo tiempo hay algunas graficas que dicen tiempo en urgencias, sin embargo, lo que quiero decir ahí es tiempo en la unidad de observación. 
