try:
    from flask import Flask
    print("✅ Flask importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro importando Flask: {e}")

try:
    import requests
    print("✅ Requests importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro importando requests: {e}")

try:
    import os
    print("✅ OS importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro importando OS: {e}")

print("\nTentando instalar bibliotecas faltantes...")
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    install("flask")
    install("requests")
    print("✅ Bibliotecas instaladas com sucesso!")
except Exception as e:
    print(f"❌ Erro na instalação: {e}")