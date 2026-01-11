#!/usr/bin/env python3
import subprocess
import re

def get_ssd_info():
    try:
        # Ejecutar smartctl para obtener datos SMART
        smart_result = subprocess.run(['sudo', 'smartctl', '-A', '/dev/disk0'], capture_output=True, text=True, check=True)
        
        # Ejecutar diskutil para obtener información detallada
        diskutil_result = subprocess.run(['diskutil', 'info', 'disk0'], capture_output=True, text=True, check=True)
        
        # Parsear datos SMART
        smart_output = smart_result.stdout
        diskutil_output = diskutil_result.stdout
        
        # Extraer información específica
        tbw = "No disponible"
        temperature = "No disponible"
        power_cycles = "No disponible"
        power_on_hours = "No disponible"
        percentage_used = "No disponible"
        data_units_written = "No disponible"
        data_units_read = "No disponible"
        
        # Extraer datos del output SMART
        for line in smart_output.split('\n'):
            if 'Temperature:' in line and 'Celsius' in line:
                parts = line.split()
                if len(parts) >= 2:
                    temperature = parts[1] + "°C"
            
            if 'Data Units Written:' in line:
                parts = line.split()
                if len(parts) >= 4:
                    data_units_written = parts[3] + " " + parts[4]
            
            if 'Data Units Read:' in line:
                parts = line.split()
                if len(parts) >= 4:
                    data_units_read = parts[3] + " " + parts[4]
            
            if 'Power Cycles:' in line:
                parts = line.split()
                if len(parts) >= 2:
                    power_cycles = parts[1]
            
            if 'Power On Hours:' in line:
                parts = line.split()
                if len(parts) >= 2:
                    power_on_hours = parts[1]
            
            if 'Percentage Used:' in line:
                parts = line.split()
                if len(parts) >= 2:
                    percentage_used = parts[1]
        
        # Extraer información del diskutil
        model = "No disponible"
        serial = "No disponible"
        capacity = "No disponible"
        disk_type = "No disponible"
        device_name = "No disponible"
        
        for line in diskutil_output.split('\n'):
            if 'Device / Media Name:' in line:
                parts = line.split(':', 1)
                if len(parts) >= 2:
                    device_name = parts[1].strip()
            elif 'Serial Number:' in line:
                parts = line.split(':', 1)
                if len(parts) >= 2:
                    serial = parts[1].strip()
            elif 'Disk Size:' in line:
                parts = line.split(':', 1)
                if len(parts) >= 2:
                    capacity = parts[1].strip()
            elif 'Protocol:' in line:
                parts = line.split(':', 1)
                if len(parts) >= 2:
                    disk_type = parts[1].strip()
        
        # Extraer modelo específico del nombre del dispositivo
        if device_name and "APPLE SSD" in device_name:
            model = device_name.split("APPLE SSD ")[1] if "APPLE SSD " in device_name else device_name
        
        # Mostrar reporte resumido en español
        print("=== REPORTE RESUMIDO DEL SSD ===")
        print(f"Tipo de disco: {disk_type}")
        print(f"Capacidad: {capacity}")
        print(f"Temperatura: {temperature}")

        print("\n=== REPORTE COMPLETO ===")
        print(smart_output)
        
        print("\n=== INFORMACIÓN DETALLADA DEL DISCO ===")
        print(diskutil_output)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    get_ssd_info()

