# reglas.py
# Base de conocimiento del sistema experto.
# Cada regla tiene la forma:  (nombre, [antecedentes], consecuente)
# y se lee:  SI todos los antecedentes son verdaderos ENTONCES el consecuente es verdadero.
# El simbolo "~" delante de una proposicion significa negacion (NO).

REGLAS = [
    ("R1",  ["fuente_ok"],                          "led_encendido"),
    ("R2",  ["led_encendido", "ventiladores_giran"], "fuente_ok"),
    ("R3",  ["~fuente_ok"],                         "falla_fuente"),
    ("R4",  ["ram_ok"],                             "~pitidos"),
    ("R5",  ["fuente_ok", "~pitidos"],              "ram_ok"),
    ("R6",  ["~ram_ok"],                            "falla_ram"),
    ("R7",  ["fuente_ok", "video_ok"],              "hay_imagen"),
    ("R8",  ["fuente_ok", "hay_imagen"],            "video_ok"),
    ("R9",  ["ram_ok", "~video_ok"],                "falla_video"),
    ("R10", ["video_ok", "disco_ok"],               "carga_sistema"),
    ("R11", ["~disco_ok"],                          "falla_disco"),
    ("R12", ["cable_ok"],                           "luz_red"),
    ("R13", ["~cable_ok"],                          "falla_cable"),
    ("R14", ["luz_red", "proveedor_ok"],            "hay_internet"),
    ("R15", ["~proveedor_ok"],                      "falla_proveedor"),
    ("R16", ["carga_sistema", "hay_internet"],      "equipo_ok"),
]

# Alfabeto de las entradas: cada respuesta del usuario es un simbolo
# s = si, n = no, ? = no se
ALFABETO = ("s", "n", "?")

# Preguntas que se le hacen al usuario (sintomas que puede observar)
PREGUNTAS = [
    ("led_encendido",     "¿Se enciende la luz (LED) de encendido?"),
    ("ventiladores_giran", "¿Giran los ventiladores?"),
    ("pitidos",           "¿Se escuchan pitidos al arrancar?"),
    ("hay_imagen",        "¿Aparece imagen en el monitor?"),
    ("carga_sistema",     "¿Carga el sistema operativo?"),
    ("luz_red",           "¿Esta encendida la luz del puerto de red o hay Wi-Fi?"),
    ("hay_internet",      "¿Se puede abrir una pagina web?"),
]

# Diagnosticos posibles con su recomendacion
DIAGNOSTICOS = {
    "falla_fuente":    ("Falla en la fuente de poder", "Revisar el cable de poder o cambiar la fuente."),
    "falla_ram":       ("Falla en la memoria RAM", "Limpiar los modulos de RAM y volver a colocarlos."),
    "falla_video":     ("Falla de video", "Revisar el cable del monitor o probar otro monitor."),
    "falla_disco":     ("Falla en el disco o en el arranque", "Revisar en la BIOS si se detecta el disco."),
    "falla_cable":     ("Falla en el cable o adaptador de red", "Cambiar el cable o activar el Wi-Fi."),
    "falla_proveedor": ("Falla del proveedor de Internet", "Reiniciar el router o llamar al proveedor."),
    "equipo_ok":       ("El equipo funciona correctamente", "No se necesita hacer nada."),
}
