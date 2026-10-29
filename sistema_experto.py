# sistema_experto.py
# Sistema experto para diagnosticar fallas de una computadora usando
# MODUS PONENS y MODUS TOLLENS, validado con tablas de verdad,
# leyes de De Morgan y la gramatica de las entradas.
# Proyecto Unidad 1 - Modelos Discretos para la Ingenieria (ESPE)
#
# Ejecutar:  python3 sistema_experto.py

from itertools import product

from reglas import ALFABETO, DIAGNOSTICOS, PREGUNTAS, REGLAS


# ---------------------------------------------------------------
# 1. Funciones de apoyo para trabajar con proposiciones
# ---------------------------------------------------------------

def negar(literal):
    """negar("p") devuelve "~p" y negar("~p") devuelve "p"."""
    if literal.startswith("~"):
        return literal[1:]
    return "~" + literal


def valor(literal, hechos):
    """Devuelve True, False o None (None = todavia no se sabe)."""
    nombre = literal.replace("~", "")
    if nombre not in hechos:
        return None
    if literal.startswith("~"):
        return not hechos[nombre]
    return hechos[nombre]


def agregar(literal, hechos):
    """Guarda un literal como hecho: "p" guarda p=True y "~p" guarda p=False."""
    nombre = literal.replace("~", "")
    hechos[nombre] = not literal.startswith("~")


# ---------------------------------------------------------------
# 2. Reglas de inferencia
# ---------------------------------------------------------------

def modus_ponens(regla, hechos, pasos):
    """  p -> q,  p   entonces  q  """
    nombre, antecedentes, consecuente = regla
    if valor(consecuente, hechos) is not None:
        return False                      # el consecuente ya se conoce
    for a in antecedentes:
        if valor(a, hechos) is not True:
            return False                  # falta que algun antecedente sea verdadero
    agregar(consecuente, hechos)
    pasos.append((nombre, "Modus ponens", antecedentes, consecuente))
    return True


def modus_tollens(regla, hechos, pasos):
    """  p -> q,  ~q   entonces  ~p  """
    nombre, antecedentes, consecuente = regla
    if valor(consecuente, hechos) is not False:
        return False                      # el consecuente tiene que ser falso
    verdaderos = [a for a in antecedentes if valor(a, hechos) is True]
    desconocidos = [a for a in antecedentes if valor(a, hechos) is None]
    # Si todos los antecedentes son verdaderos menos uno que no se conoce,
    # ese que falta tiene que ser el falso.
    if len(desconocidos) == 1 and len(verdaderos) == len(antecedentes) - 1:
        conclusion = negar(desconocidos[0])
        agregar(conclusion, hechos)
        pasos.append((nombre, "Modus tollens", [negar(consecuente)] + verdaderos, conclusion))
        return True
    return False


def inferir(hechos, pasos, reglas=REGLAS):
    """Aplica MP y MT a todas las reglas hasta que ya no se deduzca nada nuevo."""
    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for regla in reglas:
            if modus_ponens(regla, hechos, pasos) or modus_tollens(regla, hechos, pasos):
                hubo_cambio = True


def diagnosticos_encontrados(hechos):
    return [d for d in DIAGNOSTICOS if hechos.get(d) is True]


# ---------------------------------------------------------------
# 3. Tablas de verdad
# ---------------------------------------------------------------

def implica(p, q):
    """El condicional p -> q solo es falso cuando p es V y q es F."""
    return (not p) or q


def equivale(a, b):
    """El bicondicional a <-> b es verdadero cuando a y b valen lo mismo."""
    return a == b


FORMAS = [
    ("Modus ponens       [(p -> q) y p] -> q",
     lambda p, q: implica(implica(p, q) and p, q)),
    ("Modus tollens      [(p -> q) y ~q] -> ~p",
     lambda p, q: implica(implica(p, q) and not q, not p)),
    ("FALACIA: afirmar el consecuente  [(p -> q) y q] -> p",
     lambda p, q: implica(implica(p, q) and q, p)),
    ("FALACIA: negar el antecedente    [(p -> q) y ~p] -> ~q",
     lambda p, q: implica(implica(p, q) and not p, not q)),
    ("De Morgan 1        ~(p y q) <-> (~p o ~q)",
     lambda p, q: equivale(not (p and q), (not p) or (not q))),
    ("De Morgan 2        ~(p o q) <-> (~p y ~q)",
     lambda p, q: equivale(not (p or q), (not p) and (not q))),
]


def mostrar_tablas():
    for nombre, formula in FORMAS:
        print("\n" + nombre)
        print("  p  q | resultado")
        es_tautologia = True
        for p, q in product([True, False], repeat=2):     # 11, 10, 01, 00
            resultado = formula(p, q)
            print(f"  {int(p)}  {int(q)} |    {int(resultado)}")
            if not resultado:
                es_tautologia = False
        print("  -> Tautologia: es VALIDA" if es_tautologia
              else "  -> No es tautologia: es una FALACIA")


# ---------------------------------------------------------------
# 4. Alfabeto, lenguaje y gramatica de las entradas
#    <entrada>   ::= <respuesta> | <respuesta> <entrada>
#    <respuesta> ::= s | n | ?
#    Lenguaje: cadenas de 1 a 7 simbolos del alfabeto
# ---------------------------------------------------------------

def es_respuesta(simbolo):
    """<respuesta> ::= s | n | ?"""
    return simbolo in ALFABETO


def es_entrada(cadena):
    """<entrada> ::= <respuesta> | <respuesta> <entrada>"""
    if len(cadena) == 0:
        return False
    if len(cadena) == 1:
        return es_respuesta(cadena)
    return es_respuesta(cadena[0]) and es_entrada(cadena[1:])


def pertenece_al_lenguaje(cadena):
    return es_entrada(cadena) and len(cadena) <= len(PREGUNTAS)


CADENAS_PRUEBA = [("sss", True), ("ssn?n", True), ("ssnnsss", True),
                  ("", False), ("sx", False), ("ssssssss", False)]


def validar_cadena():
    print("\nAlfabeto:", ", ".join(ALFABETO))
    cadena = input("Escriba una cadena de respuestas (ej. ssnn): ").strip().lower()
    if pertenece_al_lenguaje(cadena):
        print("La cadena SI pertenece al lenguaje de entradas del sistema.")
    else:
        print("La cadena NO pertenece al lenguaje de entradas del sistema.")


# ---------------------------------------------------------------
# 5. Mostrar resultados
# ---------------------------------------------------------------

def mostrar_pasos(pasos):
    for i, (regla, tipo, premisas, conclusion) in enumerate(pasos, start=1):
        print(f"  {i}. {regla} [{tipo}]  {', '.join(premisas)}  =>  {conclusion}")


def mostrar_diagnostico(hechos):
    encontrados = diagnosticos_encontrados(hechos)
    if not encontrados:
        print("No hay datos suficientes para dar un diagnostico.")
    for d in encontrados:
        texto, recomendacion = DIAGNOSTICOS[d]
        print("DIAGNOSTICO:", texto)
        print("Recomendacion:", recomendacion)


def diagnosticar():
    hechos = {}
    pasos = []
    cadena = ""
    print("\nResponda s (si), n (no) o ? (no se)")
    for sintoma, pregunta in PREGUNTAS:
        if sintoma in hechos:
            continue                      # ya se dedujo, no hace falta preguntar
        respuesta = input(pregunta + " ").strip().lower()
        while not es_respuesta(respuesta) or len(respuesta) != 1:
            respuesta = input("  Escriba s, n o ?: ").strip().lower()
        cadena += respuesta
        if respuesta != "?":
            hechos[sintoma] = (respuesta == "s")
            inferir(hechos, pasos)
        if diagnosticos_encontrados(hechos):
            break                         # ya se encontro la causa
    print("\nCadena de entrada:", cadena)
    print("Razonamiento:")
    mostrar_pasos(pasos)
    print()
    mostrar_diagnostico(hechos)


# Casos de prueba: (nombre, respuestas del usuario, diagnostico esperado)
CASOS = [
    ("Equipo sin energia", {"led_encendido": False}, "falla_fuente"),
    ("Pitidos al arrancar", {"led_encendido": True, "ventiladores_giran": True,
                             "pitidos": True}, "falla_ram"),
    ("Pantalla negra", {"led_encendido": True, "ventiladores_giran": True,
                        "pitidos": False, "hay_imagen": False}, "falla_video"),
    ("No carga el sistema", {"led_encendido": True, "ventiladores_giran": True,
                             "pitidos": False, "hay_imagen": True,
                             "carga_sistema": False}, "falla_disco"),
    ("Sin luz de red", {"led_encendido": True, "ventiladores_giran": True,
                        "pitidos": False, "hay_imagen": True, "carga_sistema": True,
                        "luz_red": False}, "falla_cable"),
    ("Red sin Internet", {"led_encendido": True, "ventiladores_giran": True,
                          "pitidos": False, "hay_imagen": True, "carga_sistema": True,
                          "luz_red": True, "hay_internet": False}, "falla_proveedor"),
    ("Todo funciona", {"led_encendido": True, "ventiladores_giran": True,
                       "pitidos": False, "hay_imagen": True, "carga_sistema": True,
                       "luz_red": True, "hay_internet": True}, "equipo_ok"),
]


def probar_casos():
    correctos = 0
    for nombre, respuestas, esperado in CASOS:
        hechos = dict(respuestas)
        pasos = []
        inferir(hechos, pasos)
        obtenido = diagnosticos_encontrados(hechos)
        print(f"\nCaso: {nombre}")
        mostrar_pasos(pasos)
        if obtenido == [esperado]:
            correctos += 1
            print("  Resultado: CORRECTO ->", esperado)
        else:
            print("  Resultado: ERROR -> se esperaba", esperado, "y se obtuvo", obtenido)
    print(f"\nCasos correctos: {correctos} de {len(CASOS)}")
    print("\nCadenas de entrada:")
    for cadena, esperado in CADENAS_PRUEBA:
        obtenido = pertenece_al_lenguaje(cadena)
        estado = "CORRECTO" if obtenido == esperado else "ERROR"
        print(f"  '{cadena}' pertenece: {obtenido}  -> {estado}")


def reglas_como_grafo():
    """Lista de adyacencia: cada antecedente apunta a su consecuente.
    Se usara en la Unidad 3 (grafos, arboles y automatas)."""
    grafo = {}
    for nombre, antecedentes, consecuente in REGLAS:
        for a in antecedentes:
            if a not in grafo:
                grafo[a] = []
            grafo[a].append(consecuente)
    return grafo


def mostrar_reglas():
    for nombre, antecedentes, consecuente in REGLAS:
        print(f"  {nombre}: {' y '.join(antecedentes)} -> {consecuente}")
    print("\nVista como grafo (lista de adyacencia):")
    for nodo, destinos in reglas_como_grafo().items():
        print(f"  {nodo} -> {', '.join(destinos)}")


# ---------------------------------------------------------------
# 6. Menu principal
# ---------------------------------------------------------------

def menu():
    while True:
        print("\n===== SISTEMA EXPERTO: DIAGNOSTICO DE FALLAS =====")
        print("1. Ver tablas de verdad (MP, MT, falacias y De Morgan)")
        print("2. Diagnosticar una computadora")
        print("3. Ejecutar casos de prueba")
        print("4. Ver reglas y grafo")
        print("5. Validar una cadena de entrada")
        print("0. Salir")
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            mostrar_tablas()
        elif opcion == "2":
            diagnosticar()
        elif opcion == "3":
            probar_casos()
        elif opcion == "4":
            mostrar_reglas()
        elif opcion == "5":
            validar_cadena()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida")


if __name__ == "__main__":
    menu()
