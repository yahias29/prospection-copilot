#!/usr/bin/env python3
# Script de configuration rapide Vertex AI
# =======================================

import os
import sys
import json
import subprocess
from pathlib import Path

def setup_vertex_ai():
    """Configuration rapide Vertex AI"""
    print("🚀 Configuration Co-pilote Prospection IA - Vertex AI Edition")
    print()

    # Vérification Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis. Version actuelle:", sys.version)
        sys.exit(1)
    print("✅ Python version OK:", sys.version.split()[0])

    # Installation dépendances
    print("📦 Installation des dépendances Vertex AI...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_vertex.txt"], 
                      check=True, capture_output=True)
        print("✅ Dépendances installées")
    except subprocess.CalledProcessError:
        print("❌ Erreur installation. Vérifiez requirements_vertex.txt")
        sys.exit(1)

    # Configuration Google Cloud
    print("⚙️ Configuration Google Cloud...")

    project_id = input("🔑 ID de votre projet Google Cloud: ").strip()
    if not project_id:
        print("❌ ID projet obligatoire")
        sys.exit(1)

    # Vérification service account
    service_account_file = "service-account.json"
    if not Path(service_account_file).exists():
        print(f"❌ Fichier {service_account_file} manquant")
        print("📋 Étapes à suivre:")
        print("1. Console Google Cloud > IAM > Comptes de service")
        print("2. Créer un compte de service avec rôle 'Vertex AI User'")
        print("3. Générer une clé JSON")
        print("4. Renommer le fichier en 'service-account.json'")
        print("5. Placer le fichier dans ce dossier")
        sys.exit(1)

    # Création .env
    env_content = f"""# Configuration Vertex AI
GOOGLE_CLOUD_PROJECT={project_id}
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
GOOGLE_CLOUD_LOCATION=us-central1
"""

    with open(".env", "w") as f:
        f.write(env_content)
    print("✅ Fichier .env créé")

    # Test configuration
    print("🧪 Test de la configuration...")
    try:
        import vertexai
        vertexai.init(project=project_id, location="us-central1")
        print("✅ Vertex AI configuré correctement")
    except Exception as e:
        print(f"❌ Erreur Vertex AI: {e}")
        print("Vérifiez votre configuration Google Cloud")
        sys.exit(1)

    # Test DuckDuckGo
    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS()
        print("✅ DuckDuckGo prêt (gratuit)")
    except:
        print("⚠️ DuckDuckGo non disponible (optionnel)")

    print()
    print("🎉 Configuration terminée avec succès !")
    print()
    print("📋 Prochaines étapes:")
    print("1. Testez l'app: streamlit run prospection_copilot_vertex.py")
    print("2. Analysez quelques prospects")
    print("3. Déployez sur Streamlit Cloud")
    print("4. Contactez Made In Tracker !")

if __name__ == "__main__":
    setup_vertex_ai()
