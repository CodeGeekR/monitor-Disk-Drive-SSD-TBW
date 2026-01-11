#!/usr/bin/env python3
import subprocess
import json

def get_nvme_smart():
    # Primero verificamos que smartctl esté instalado
    try:
        subprocess.run(["smartctl", "--version"], check=True, capture_output=True)
    except:
        print("Error: smartmontools no está instalado")
        print("Instálalo con: brew install smartmontools")
        return None

    # Buscamos el dispositivo NVMe
    try:
        result = subprocess.run(
            ["diskutil", "list"],
            capture_output=True,
            text=True,
            check=True
        )
    except:
        print("Error: No se pudo listar los discos")
        return None

    # Extraemos la ruta del NVMe de la salida de diskutil
    nvme_path = None
    for line in result.stdout.split('\n'):
        if 'Apple NVMe' in line or 'NVMe' in line:
            parts = line.split()
            if len(parts) > 1 and parts[0].isdigit():
                nvme_path = f"/dev/disk{parts[0]}"
                break

    if not nvme_path:
        print("Error: No se encontró un dispositivo NVMe")
        print("Prueba manualmente con: sudo smartctl -a /dev/nvme0")
        return None

    # Obtenemos la información SMART
    try:
        result = subprocess.run(
            ["sudo", "smartctl", "-j", "-a", nvme_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"Error al obtener SMART: {result.stderr}")
            return None

        data = json.loads(result.stdout)
        return {
            "model": data["smartctl"]["device"]["model_name"],
            "serial": data["smartctl"]["device"]["serial_number"],
            "temperature": data["smartctl"]["nvme_smart_health_information_log"]["basic"]["temperature"],
            "health": data["smartctl"]["nvme_smart_health_information_log"]["basic"]["percentage_used"],
            "power_cycles": data["smartctl"]["nvme_smart_health_information_log"]["basic"]["power_cycles"],
            "unsafe_shutdowns": data["smartctl"]["nvme_smart_health_information_log"]["basic"]["unsafe_shutdowns"]
        }

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

if __name__ == "__main__":
    print("Obteniendo información SMART del NVMe...")
    smart = get_nvme_smart()

    if smart:
        print("\n=== INFORMACIÓN DEL SSD ===")
        print(f"Modelo: {smart['model']}")
        print(f"Serial: {smart['serial']}")
        print(f"Temperatura: {smart['temperature']}°C")
        print(f"Salud: {smart['health']}% usado")
        print(f"Ciclos de encendido: {smart['power_cycles']}")
        print(f"Apagados no seguros: {smart['unsafe_shutdowns']}")
    else:
        print("\nNo se pudo obtener la información SMART")
        print("Verifica:")
        print("1. El dispositivo NVMe existe (diskutil list)")
        print("2. Los permisos (sudo)")
        print("3. La instalación (smartctl --version)")

