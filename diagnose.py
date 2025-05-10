#!/usr/bin/env python
"""Script para diagnosticar problemas de importación."""
import os
import sys
import importlib

def show_sys_path():
    """Muestra los directorios en sys.path."""
    print("Directorios en sys.path:")
    for path in sys.path:
        print(f"  - {path}")
    print()

def check_module_exists(module_name):
    """Comprueba si se puede importar un módulo."""
    try:
        importlib.import_module(module_name)
        print(f"✅ Se pudo importar '{module_name}' correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error al importar '{module_name}': {e}")
        return False

def main():
    """Función principal."""
    # Mostrar el directorio actual
    print(f"Directorio actual: {os.getcwd()}")
    
    # Mostrar sys.path
    show_sys_path()
    
    # Intentar importar módulos clave
    modules_to_check = [
        'backend',
        'backend.config',
        'backend.config.settings',
        'backend.tasks',
        'backend.users',
    ]
    
    for module in modules_to_check:
        check_module_exists(module)

if __name__ == '__main__':
    main()