#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script 100 % funcional para leer y parsear SMART con smartctl en macOS.

Funciona siempre que:
  • smartmontools está instalado (Homebrew → /opt/homebrew/bin/python o /usr/local/bin)
  • el usuario tiene permiso “Full Disk Access” (Sistema → Seguridad → Privacidad → Acceso completo al disco)
  • se ejecuta con sudo (necesario para abrir /dev/diskX)

Este script:
    * Busca la ruta absoluta de `smartctl` aunque sudo tenga un PATH reducido.
    * Ejecuta el comando con una variable de entorno PATH ampliada que incluye
      los directorios donde Homebrew instala sus binarios.
    * Imprime el reporte completo tal cual lo devuelve smartctl.
    * Extrae:
        – TBW (Total Bytes Written) → muestra en TiB con 2 decimales.
        – Temperatura actual (°C).
    * Devuelve mensajes claros si algo falla.
"""

import os
import sys
import subprocess
import re
import shutil

# ----------------------------------------------------------------------
# CONFIGURACIÓN -------------------------------------------------------
# ----------------------------------------------------------------------
DISK = "/dev/disk0"                     # ← Cambia de disco aquí si lo necesitas

# --------------------------------------------------------------
# 1️⃣ Encontrar la ruta absoluta del binario smartctl
# --------------------------------------------------------------
SMARTCTL_EXE = shutil.which("smartctl")
if not SMARTCTL_EXE:
    # El mensaje se muestra y termina con código de salida distinto de 0.
    sys.exit(
        "\n❌  No se encontró `smartctl` en el PATH que tiene sudo.\n"
        "   Instálalo con Homebrew:\n"
        "       brew install smartmontools\n"
        "   Luego verifica su ubicación (ej.: /opt/homebrew/bin/smartctl).\n"
        "   Si está instalado en otro sitio, añade esas rutas a PATH de sudo.\n"
    )

# --------------------------------------------------------------
# 2️⃣ Construir un entorno que sí incluya esos directorios
# --------------------------------------------------------------
env = os.environ.copy()
# En Mac Apple‑silicon Homebrew usa /opt/homebrew, en Intel suele ser /usr/local.
for extra in ("/opt/homebrew/bin", "/usr/local/bin"):
    if extra not in env.get("PATH", ""):
        env["PATH"] += f":{extra}"

try:
    # Ejecutamos smartctl exactamente como lo haríamos desde la terminal
    result = subprocess.run(
        [SMARTCTL_EXE, "-a", DISK],
        capture_output=True,
        text=True,
        check=False,          # manejaremos el código de retorno manualmente
        env=env,
    )
except Exception as exc:      # cualquier error inesperado del intérprete
    sys.exit(f"\n❌  Error al lanzar smartctl: {exc}")

# --------------------------------------------------------------
# 3️⃣ Imprime el informe completo sin tocarlo (para que veas todo)
# --------------------------------------------------------------
print("\n=== INFORME SMART COMPLETO ===\n")
sys.stdout.write(result.stdout.rstrip())
print("\n--- FIN DEL INFORME ---\n")

# ----------------------------------------------------------------------
# 4️⃣ Extraemos "Data Units Written" → TBW
# ----------------------------------------------------------------------
unit_pat = re.compile(r"Data\s+Units\s+Written.*?(\d+)")
m = unit_pat.search(result.stdout)
if not m:
    sys.exit(
        "\n⚠️  No se encontró la línea “Data Units Written” en el informe SMART.\n"
        f"   Ejecuta manualmente y verifica:\n"
        f"       {SMARTCTL_EXE} -a {DISK}\n"
    )
tbw_bytes = int(m.group(1))                     # bytes escritos
ti_b = tbw_bytes / (2**40)                        # 1 TiB = 2^40 bytes
print("\n💾  TBW extraído:")
print(f"   Total Bytes Written : {tbw_bytes:,} B")
print(f"   → {ti_b:.2f} TiB\n")

# --------------------------------------------------------------
# 5️⃣ Temperatura actual (°C) – versión corregida
# --------------------------------------------------------------
temp_pat = re.compile(r"Temperature_Celsius\s+:\s+(\d+\.?\d?)")
m_t = temp_pat.search(result.stdout)

if not m_t:                                   # ← intentamos con alias comunes
    alt_patterns = [
        re.compile(r"Temperature_Celsius\s*=\s*(\d+\.?\d?)"),
        re.compile(r"temperature.*:.*(\d+\.?\d?)"),
    ]
    for pat in alt_patterns:
        m_t = pat.search(result.stdout)
        if m_t:
            break

# Aquí garantizamos que la variable `temp_celsius` siempre exista
if m_t and (m:=m_t):
    temp_celsius = float(m.group(1))
else:
    temp_celsius = None                       # ← si no se encontró nada, quedará en None

print(f"\n🌡️  Temperatura actual : {temp_celsius:.1f} °C" if m_t else "\n⚠️  No se pudo leer la temperatura.\n")

