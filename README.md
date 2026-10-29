# DiagnostiPC: sistema experto de diagnóstico de fallas

Proyecto ABP de la Unidad 1 (Lógica proposicional y funcional) de Modelos Discretos para la Ingeniería, ESPE Santo Domingo, NRC 32798.

**Autores:** Ander Humberto López Balcázar y Joseph Andrade Basurto
**Docente:** Mgtr. Javier José Cevallos Farías

## Descripción

El sistema hace preguntas de sí o no sobre una computadora que falla y, aplicando **modus ponens** y **modus tollens** sobre 16 reglas condicionales, encuentra la causa probable y muestra cada paso del razonamiento.

Temas de la Unidad 1 aplicados:

- Proposiciones y tablas de verdad
- Modus ponens y modus tollens
- Leyes de De Morgan
- Alfabeto, lenguaje y gramática de las entradas: Σ = {s, n, ?}

## Requisitos

- Python 3.8 o superior
- Sin librerías externas

## Ejecución

```
python3 sistema_experto.py
```

En Windows también se puede usar `python sistema_experto.py`.

## Menú

| Opción | Función |
|---|---|
| 1 | Tablas de verdad de MP, MT, las falacias y las leyes de De Morgan |
| 2 | Diagnosticar una computadora |
| 3 | Casos de prueba (7 diagnósticos y 6 cadenas de entrada) |
| 4 | Reglas y su vista como grafo |
| 5 | Validar una cadena de entrada |
| 0 | Salir |

## Ejemplo

Para un equipo que enciende y no tiene pitidos, pero no muestra imagen, las respuestas `s s n n` producen:

```
1. R2 [Modus ponens]  led_encendido, ventiladores_giran  =>  fuente_ok
2. R5 [Modus ponens]  fuente_ok, ~pitidos  =>  ram_ok
3. R7 [Modus tollens]  ~hay_imagen, fuente_ok  =>  ~video_ok
4. R9 [Modus ponens]  ram_ok, ~video_ok  =>  falla_video
DIAGNOSTICO: Falla de video
```

## Archivos

| Archivo | Contenido |
|---|---|
| `reglas.py` | Las 16 reglas, el alfabeto, las 7 preguntas y los diagnósticos |
| `sistema_experto.py` | Modus ponens, modus tollens, tablas de verdad, gramática de entradas, casos de prueba y menú |

## Modelo a futuro

En la Unidad 3 el funcionamiento del sistema se modelará como un autómata finito o árbol de decisión. La función `reglas_como_grafo()` ya representa las reglas como un grafo dirigido.
