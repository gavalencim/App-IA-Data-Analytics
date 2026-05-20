# Aplicacion de analítica de datos con IA

## Introducción

Actualmente, el análisis de datos se ha convertido en una herramienta fundamental para la toma de decisiones en áreas como negocios, salud, educación, seguridad y ciencias sociales. Sin embargo, muchas personas que poseen conjuntos de datos no cuentan con conocimientos técnicos en programación, estadística o herramientas de visualización, lo que dificulta la exploración y comprensión de la información disponible.

Tradicionalmente, el análisis de datasets requiere conocimientos en herramientas como Python, SQL, Power BI o Excel avanzado, además de experiencia en interpretación de datos, estadística y construcción de visualizaciones. Esto genera una barrera importante para usuarios no técnicos que desean obtener información útil de sus datos de forma rápida e intuitiva.

Adicionalmente, las herramientas convencionales de análisis suelen requerir configuraciones manuales para seleccionar tipos de gráficos, limpiar datos o construir consultas específicas, lo que puede consumir tiempo y generar errores en usuarios con poca experiencia en análisis de información.

Con el crecimiento reciente de los modelos de Inteligencia Artificial generativa y procesamiento de lenguaje natural (NLP), surge la posibilidad de crear sistemas capaces de interpretar datasets automáticamente, recomendar visualizaciones relevantes y responder preguntas realizadas en lenguaje natural por parte del usuario.

Este proyecto propone el desarrollo de una aplicación web inteligente llamada AI Data Analyst, construida con Django y técnicas de Inteligencia Artificial, que permita:

* Cargar datasets en formato CSV.
* Analizar automáticamente la estructura del dataset.
* Recomendar y generar visualizaciones apropiadas mediante IA.
* Permitir interacción conversacional mediante un chatbot inteligente.
* Responder preguntas sobre los datos utilizando consultas generadas dinámicamente con Pandas.
* Explicar resultados en lenguaje natural para facilitar la interpretación de la información.

La relevancia del proyecto radica en democratizar el análisis de datos mediante el uso de Inteligencia Artificial, permitiendo que usuarios sin conocimientos avanzados en programación puedan explorar información compleja de manera visual e interactiva.

Además, el proyecto integra múltiples conceptos vistos en el curso, incluyendo:

* Procesamiento de Lenguaje Natural (NLP)
* Sistemas expertos
* Generación automática de consultas
* Inteligencia Artificial generativa
* Automatización de análisis de datos
* Interacción humano-computador

Finalmente, el sistema busca servir como una base escalable para futuros desarrollos, incorporando funcionalidades avanzadas como generación automática de reportes, análisis predictivo, dashboards inteligentes y agentes conversacionales especializados en datos.

## Objetivo general

Desarrollar una aplicación web inteligente capaz de analizar datasets en formato CSV mediante técnicas de Inteligencia Artificial, generando visualizaciones automáticas y permitiendo consultas en lenguaje natural a través de un chatbot interactivo.

## Metodología

El desarrollo del proyecto se realizó siguiendo una metodología incremental basada en prototipado rápido y arquitectura modular, permitiendo construir un MVP funcional y posteriormente agregar nuevas capacidades de Inteligencia Artificial.

El flujo general del sistema es el siguiente:

```text
Usuario carga CSV
        ↓
Procesamiento del dataset
        ↓
Detección de tipos de variables
        ↓
Generación de perfil del dataset
        ↓
IA analiza metadatos del dataset
        ↓
Recomendación de visualizaciones
        ↓
Generación automática de gráficos
        ↓
Interfaz interactiva para el usuario
        ↓
Chatbot recibe preguntas
        ↓
IA selecciona columnas relevantes
        ↓
Generación automática de consultas Pandas
        ↓
Ejecución segura de consultas
        ↓
Respuesta en lenguaje natural
```

La metodología implementada combina técnicas de:

* Ingeniería de software modular
* Procesamiento de lenguaje natural
* Sistemas basados en reglas
* Generación automática de código
* Visualización de datos
* Arquitectura orientada a servicios

El sistema fue dividido en servicios independientes para facilitar su escalabilidad y mantenimiento.

## Desarrollo

#### Arquitectura General del Sistema

El proyecto fue desarrollado como una aplicación web utilizando el framework Django bajo una arquitectura modular basada en servicios, permitiendo escalabilidad, mantenibilidad y futuras integraciones con modelos más avanzados o arquitecturas distribuidas.

La aplicación está compuesta por los siguientes módulos principales:

| Módulo | Responsabilidad |
|---|---|
| CSV Service | Carga, validación y perfilamiento de datasets CSV |
| AI Analysis Service | Uso de IA para analizar semánticamente el dataset y recomendar visualizaciones |
| Visualization Service | Generación automática de gráficos estadísticos |
| Dataset RAG Service | Chatbot inteligente con consultas sobre el dataset |
| Frontend | Interfaz web interactiva para análisis y visualización |

#### Flujo General del Sistema

1. El usuario carga un archivo CSV.
2. El sistema analiza automáticamente las columnas y tipos de datos.
3. Se genera un perfil estadístico inicial del dataset.
4. El usuario selecciona las columnas relevantes y el objetivo del análisis.
5. La IA recomienda los gráficos más adecuados según el contexto de los datos.
6. El sistema genera automáticamente las visualizaciones.
7. El usuario puede interactuar con un chatbot inteligente para realizar preguntas sobre el dataset en lenguaje natural.
8. El chatbot transforma las preguntas en consultas Pandas ejecutables y devuelve respuestas explicadas en lenguaje natural.

#### Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Django | Framework backend |
| Pandas | Manipulación y análisis de datos |
| Matplotlib | Generación de visualizaciones |
| Gemini API | Inteligencia artificial generativa |
| HTML/CSS/JavaScript | Interfaz de usuario |
| GitHub | Control de versiones |

#### Implementación del Análisis Inteligente

Al cargar un CSV, el sistema identifica automáticamente:

* Columnas numéricas
* Columnas categóricas
* Tipos de datos
* Valores únicos
* Valores de ejemplo

Esto permite suministrar contexto estructurado al modelo de IA.

#### Recomendación Inteligente de Visualizaciones

Se implementó un sistema basado en IA generativa que analiza:

* El tipo semántico de las columnas
* El objetivo de análisis escrito por el usuario
* Relaciones potenciales entre variables

La IA recomienda automáticamente:

* Histogramas
* Gráficos de barras
* Comparaciones categóricas
* Relaciones entre variables cuantitativas y cualitativas

Ejemplo:

```json
{
  "x_column": "VENDEDOR",
  "y_column": "VENTAS",
  "recommended_chart": "bar_numeric"
}
```

#### Generación Automática de Gráficos

El sistema implementa múltiples tipos de visualizaciones automáticas:

| Tipo	| Uso |
|---|---|
| Histogramas	| Distribución de variables numéricas
| Barras categóricas	| Frecuencia de categorías
| Barras numéricas	| Relación entre categorías y métricas
| Scatter plots	| Relación entre variables numéricas

#### Implementación del Chatbot Inteligente

El chatbot fue desarrollado utilizando un enfoque tipo RAG (Retrieval-Augmented Generation) adaptado para datasets tabulares.

Funcionamiento: 

1. El usuario realiza una pregunta en lenguaje natural.
2. El sistema identifica las columnas relevantes usando IA.
3. La IA genera código Pandas seguro.
4. El backend ejecuta el código dinámicamente.
5. Los resultados son convertidos a lenguaje natural.

## Resultados Funcionales

El sistema logró:

Analizar datasets CSV automáticamente
Clasificar tipos de variables
Recomendar visualizaciones usando IA
Generar gráficos automáticamente
Responder preguntas sobre datasets en lenguaje natural
Ejecutar consultas dinámicas usando Pandas

## Discusión

#### Comparación con Herramientas Existentes

Actualmente existen herramientas como:

* Power BI
* Tableau
* Looker Studio

Sin embargo, muchas requieren:

* Conocimiento técnico
* Configuración manual
* Construcción manual de gráficos

El sistema desarrollado busca reducir esa barrera mediante IA generativa.

#### Aportes del Proyecto

El proyecto aporta:

* Automatización del análisis exploratorio
* Generación automática de visualizaciones
* Interacción conversacional con datasets
* Interpretación de resultados mediante IA

#### Limitaciones Encontradas

Durante el desarrollo se identificaron algunas limitaciones como la ambigüedad aemántica. La IA puede interpretar incorrectamente términos como: “mujeres”, “femenino”, “sexo femenino”, cuando el dataset utiliza nomenclaturas diferentes. El desempeño depende de calidad del prompt, calidad del dataset, consistencia de nombres de columnas. Además, el uso de modelos generativos puede generar mayor latencia, consumo de tokens, costos en APIs externas. 

#### Mejoras futuras

Se proponen futuras mejoras como:

* Embeddings semánticos para columnas
* Vectorización de datasets
* Fine-tuning especializado
* Dashboards interactivos avanzados
* Exportación automática de reportes
* Detección automática de anomalías
* Machine Learning predictivo
* Integración con bases de datos SQL

## Conclusión

El proyecto demuestra cómo la Inteligencia Artificial generativa puede integrarse exitosamente con análisis de datos para construir herramientas accesibles, intuitivas y automatizadas. La combinación de procesamiento de lenguaje natural, generación automática de código, visualización de datos, arquitecturas modulares, permitió desarrollar una plataforma funcional con potencial real de crecimiento hacia aplicaciones profesionales y comerciales.
