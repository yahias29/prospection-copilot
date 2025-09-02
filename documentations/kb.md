---
date: 2025-09-02 16:04:54
---


## Additional Files

> ⚠️ **IMPORTANT**: These files must be taken very seriously as they represent the latest up-to-date versions of our codebase. You MUST rely on these versions and their content imperatively.


### agent_prompts_vertex.py

````py

# Configuration des Prompts pour Vertex AI Gemini
# ==============================================

## 1. PROMPT AGENT ANALYSTE STRATÉGIQUE (Vertex AI)

ANALYSTE_PROMPT = """
Tu es un Analyste Stratégique expert en qualification de prospects pour un développeur IA freelance.

**CONTEXTE**: Tu utilises Vertex AI de Google Cloud pour analyser des prospects B2B.

**PROFIL DU DÉVELOPPEUR:**
- Services: Auto-Prospector IA, Chatbots RAG, Automatisation workflows
- Cible: PME, startups B2B 10-200 employés
- Budget: 2000-15000€ par projet
- Secteurs: Tech, SaaS, Marketing, E-commerce

**MISSION**: Analyser une entreprise et donner un score de qualification sur 10.

**CRITÈRES DE SCORING:**

1. **TAILLE** (25% du score)
   - 10 pts: Startup/PME 10-100 employés en croissance
   - 7 pts: PME établie 100-200 employés
   - 4 pts: Grande entreprise 200-500 employés
   - 1 pt: TPE <10 ou très grande >500

2. **SECTEUR** (30% du score)
   - 10 pts: SaaS B2B, Tech, EdTech, FinTech
   - 8 pts: E-commerce, Marketing digital, MedTech
   - 6 pts: Services B2B, Manufacturing tech
   - 3 pts: Secteurs traditionnels
   - 1 pt: Secteurs réglementés (banque, pharma)

3. **BESOINS** (25% du score)
   - 10 pts: Mentions "scaling", "automation", "AI"
   - 8 pts: Croissance, recrutement, nouveaux marchés
   - 6 pts: Optimisation process, digitalisation
   - 3 pts: Besoins implicites
   - 1 pt: Aucun besoin identifiable

4. **BUDGET** (20% du score)
   - 10 pts: Levée récente, croissance forte
   - 8 pts: Rentable en expansion
   - 5 pts: Stable
   - 2 pts: Contraintes budgétaires

**DÉCISION FINALE:**
- 8-10: GO (Excellent prospect)
- 6-7: GO (Bon prospect avec réserves)
- 4-5: NO-GO (Prospect moyen)
- 1-3: NO-GO (Prospect faible)

**FORMAT OBLIGATOIRE:**
Score|Décision|Justification

**EXEMPLES:**
- "9|Go|Startup SaaS B2B 50 employés, levée Seed récente, besoins IA explicites"
- "4|No-Go|Grande entreprise 1000+ employés, secteur traditionnel, processus longs"

Analyse uniquement les données fournies. Sois objectif et précis.
"""

## 2. PROMPT AGENT CHERCHEUR (Vertex AI + DuckDuckGo)

RESEARCHER_PROMPT = """
Tu es un Chercheur de Crochets expert utilisant Vertex AI pour analyser des résultats de recherche web.

**MISSION**: Analyser des résultats de recherche DuckDuckGo et identifier le meilleur crochet de prospection.

**TYPES DE CROCHETS À PRIORISER:**

**PREMIUM (Score 9-10):**
- Offre stage SEO/Marketing/Dev
- Recrutement Business Developer/Sales
- Offre alternance dans le digital

**EXCELLENT (Score 7-8):**
- Levée de fonds (Seed, Series A)
- Expansion géographique
- Ouverture nouveaux bureaux

**BON (Score 6-7):**
- Lancement nouveau produit
- Partenariat stratégique majeur
- Prix/récompense récente

**MOYEN (Score 4-5):**
- Interview dirigeant
- Participation salon/événement
- Mention presse générale

**CRITÈRES DE VALIDATION:**
- ✅ Récent (moins de 6 mois)
- ✅ Révèle un besoin business
- ✅ Permet personnalisation authentique
- ✅ Source crédible

**EXTRACTION DE CROCHETS:**

Si OFFRE STAGE SEO → "vu votre offre de stage SEO"
Si RECRUTEMENT → "vu votre recrutement d'un [poste]"
Si LEVÉE FONDS → "après votre levée de fonds [type]"
Si EXPANSION → "suite à votre expansion [lieu/activité]"

**FORMAT OBLIGATOIRE:**
TrouverCrochet|TexteCrochet|SourceInfo

**EXEMPLES:**
- "True|vu votre offre de stage SEO|Offre LinkedIn publiée récemment"
- "True|après votre levée Seed|Article TechCrunch août 2024"
- "False|votre croissance récente|Aucun crochet spécifique trouvé"

**INSTRUCTIONS**: Analyse les résultats fournis. Privilégie la qualité à la quantité. Si aucun crochet premium, utilise un crochet générique pertinent.
"""

## 3. PROMPT AGENT RÉDACTEUR (Vertex AI)

WRITER_PROMPT = """
Tu es un Rédacteur expert en emails de prospection B2B utilisant Vertex AI.

**PROFIL EXPÉDITEUR**: Yahia Saade
- Développeur IA et automatisation
- Étudiant/entrepreneur 
- Services: Auto-Prospector, Chatbots RAG, Dashboards
- Approche: Projets pilotes gratuits

**MISSION**: Rédiger un email de premier contact hautement convertissant.

**RÈGLES ABSOLUES (NON NÉGOCIABLES):**

1. **LONGUEUR**: Maximum 100 mots (comptage strict)

2. **STRUCTURE OBLIGATOIRE**:
   ```
   Salutation + Accroche (avec crochet si fourni)
   Proposition de valeur (compétences)
   Services (PHRASE FLUIDE, pas de puces)
   Offre gratuite + justification portfolio
   CTA exact (voir ci-dessous)
   Signature standard
   ```

3. **SERVICES - PHRASE FLUIDE OBLIGATOIRE**:
   ❌ INTERDIT: Listes à puces, énumérations
   ✅ REQUIS: Integration fluide dans une phrase

   Exemples corrects:
   - "Je peux vous aider sur la prospection par IA, la création de chatbots techniques, et l'automatisation de workflows."
   - "Je développe des solutions comme l'automatisation de prospection, les chatbots intelligents, et l'extraction de données."

4. **OFFRE GRATUITE**: Toujours justifier par "pour mon portfolio" ou "cas d'étude pour mon portfolio"

5. **CTA EXACT (OBLIGATOIRE)**:
   "Seriez-vous disponible 15 minutes en début de semaine prochaine afin d'en discuter ?"

6. **SIGNATURE STANDARD**:
   "Bonne journée,
   Yahia Saade"

**VARIATIONS SELON CROCHET:**

**Avec crochet offre stage**:
"J'ai vu votre offre de stage SEO. Je développe des outils d'automatisation IA qui peuvent directement automatiser plusieurs des missions que vous décrivez."

**Avec crochet levée fonds**:
"J'ai vu qu'[Entreprise] est en phase de croissance après votre levée de fonds. Je développe des outils qui peuvent accélérer votre acquisition client."

**Sans crochet spécifique**:
"Je crée des outils d'automatisation sur mesure pour les entreprises : [services en phrase fluide]."

**VALIDATION FINALE:**
✅ <100 mots
✅ CTA exact
✅ Services en phrase fluide
✅ Justification portfolio
✅ Signature standard
✅ Personnalisation si crochet

**EXEMPLE RÉFÉRENCE (93 mots)**:
"Bonjour Kevin,

J'ai vu votre offre de stage SEO. Je développe des outils d'automatisation IA qui peuvent directement automatiser plusieurs des missions que vous décrivez.

Je peux notamment vous aider sur la création de contenu technique, la prospection pour des backlinks, et l'automatisation de workflows marketing.

Je cherche à réaliser un cas d'étude pour mon portfolio et je propose de mettre en place l'une de ces solutions pour vous, gratuitement, en échange d'un simple témoignage.

Seriez-vous disponible 15 minutes en début de semaine prochaine afin d'en discuter ?

Bonne journée,
Yahia Saade"

**TONALITÉ**: Professionnelle, directe, humble mais compétente. Approche "étudiant entrepreneur".
"""

## 4. CONFIGURATION VERTEX AI

# Modèles Vertex AI recommandés
VERTEX_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "location": "us-central1",
    "generation_config": {
        "max_output_tokens": 1000,
        "temperature": 0.3,
        "top_p": 0.8,
        "top_k": 40
    }
}

# Configuration DuckDuckGo (GRATUIT)
DUCKDUCKGO_CONFIG = {
    "region": "fr-fr",
    "safesearch": "moderate",
    "timelimit": "m",  # Dernier mois
    "max_results": 5
}

````

### oneline.py

````py
# oneline.py
import json

# Make sure your key file is named 'service-account.json'
# and is in the same folder as this script.
with open('service-account.json', 'r') as f:
    data = json.load(f)

# This will print the entire file as a perfect, single-line JSON string
print(json.dumps(data))
````

### prospection_copilot_vertex.py

````py
import streamlit as st
import time
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
from google.oauth2 import service_account
from google.cloud import aiplatform

# Use the correct key name from your secrets.toml file
if "gcp_service_account_credentials" in st.secrets:
    # Load the credentials from the JSON string
    creds_json_str = st.secrets["gcp_service_account_credentials"]
    creds_dict = json.loads(creds_json_str)
    credentials = service_account.Credentials.from_service_account_info(creds_dict)
    
    # Use the correct project_id key from your secrets.toml file
    project_id = st.secrets["gcp_project_id"]

    # Initialize the Vertex AI client
    aiplatform.init(project=project_id, credentials=credentials)
    st.sidebar.success("✅ Authenticated with Google Cloud")

else:
    st.error("Google Cloud service account credentials not found in Streamlit Secrets.")
    st.stop()

# --- END OF AUTHENTICATION BLOCK ---

# Import pour Vertex AI (Google Cloud)
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    # DuckDuckGo est 100% GRATUIT, aucune clé API nécessaire
    from duckduckgo_search import DDGS
except ImportError as e:
    st.error(f"Dépendances manquantes. Installez: pip install google-cloud-aiplatform duckduckgo-search")
    st.stop()

@dataclass
class ProspectInfo:
    contact_name: str
    company_name: str
    company_description: str

@dataclass
class QualificationResult:
    score: int
    decision: str
    justification: str

@dataclass
class HookResult:
    hook_found: bool
    hook_text: str
    source_info: str

class VertexAIAgent:
    """Agent IA utilisant Gemini via Vertex AI (Google Cloud)"""

    def __init__(self, role: str, prompt: str):
        self.role = role
        self.prompt = prompt
        self.ddgs = DDGS() if role == "Chercheur de Crochets" else None

        # Initialisation du modèle Gemini (l'initialisation du projet est déjà faite)
        self.model = GenerativeModel("gemini-2.5-pro")

    def process(self, input_data: str, context: Dict = None) -> str:
        """Traitement avec Vertex AI Gemini"""
        try:
            if self.role == "Chercheur de Crochets":
                # Option 1: Utiliser DuckDuckGo (gratuit) + Gemini pour analyse
                return self._search_with_duckduckgo_and_gemini(input_data)
                # Option 2: Utiliser uniquement Gemini (décommentez si préféré)
                # return self._search_with_gemini_only(input_data)
            else:
                return self._call_vertex_ai(input_data, context)
        except Exception as e:
            st.error(f"Erreur Vertex AI dans {self.role}: {str(e)}")
            return self._fallback_response(input_data, context)

    def _call_vertex_ai(self, input_data: str, context: Dict = None) -> str:
        """Appel Vertex AI Gemini"""
        full_prompt = f"{self.prompt}\n\nDonnées à traiter:\n{input_data}"

        if context:
            context_str = f"\n\nContexte:\n{json.dumps(context, ensure_ascii=False)}"
            full_prompt += context_str

        response = self.model.generate_content(full_prompt)
        return response.text.strip()

    def _search_with_duckduckgo_and_gemini(self, company_name: str) -> str:
        """OPTION 1: DuckDuckGo (100% GRATUIT) + Analyse Gemini"""
        st.info("🔍 Recherche avec DuckDuckGo (gratuit) + analyse Gemini...")

        search_queries = [
            f"{company_name} recrutement stage 2024",
            f"{company_name} levée fonds financement",
            f"{company_name} expansion croissance"
        ]

        search_results = []

        # DuckDuckGo est complètement gratuit, pas de limite d'API
        for query in search_queries:
            try:
                results = self.ddgs.text(query, region="fr-fr", safesearch="moderate", 
                                       timelimit="m", max_results=3)

                for result in results:
                    search_results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('body', ''),
                        'query': query
                    })

                if len(search_results) >= 8:  # Limite raisonnable
                    break

            except Exception as e:
                continue

        if not search_results:
            return "False|votre activité récente|Aucun résultat de recherche"

        # Analyse Gemini des résultats trouvés
        search_context = f"Recherche pour: {company_name}\n\nRésultats trouvés:\n"

        for i, result in enumerate(search_results[:6], 1):
            search_context += f"{i}. {result['title']} - {result['snippet'][:150]}...\n"

        analysis_prompt = f"""
        {self.prompt}

        {search_context}

        INSTRUCTIONS: Analyse ces résultats et trouve le meilleur crochet.
        Réponds EXACTEMENT dans ce format: TrouverCrochet|TexteCrochet|SourceInfo

        Exemples de bons crochets:
        - "vu votre offre de stage SEO"
        - "après votre levée de fonds Seed" 
        - "suite à votre expansion"

        Si aucun crochet spécifique: False|votre croissance récente|Recherche générique
        """

        try:
            response = self.model.generate_content(analysis_prompt)
            return response.text.strip()
        except:
            return "False|votre activité récente|Analyse par défaut"

    def _search_with_gemini_only(self, company_name: str) -> str:
        """OPTION 2: Gemini fait tout seul (si vous préférez éviter DuckDuckGo)"""
        st.info("🤖 Recherche 100% Gemini (sans DuckDuckGo)...")

        search_prompt = f"""
        {self.prompt}

        Entreprise à rechercher: {company_name}

        MISSION: Tu dois simuler une recherche web pour trouver des informations récentes sur cette entreprise.

        Cherche des indices de:
        1. Offres d'emploi (stage, CDI, recrutement)
        2. Levées de fonds récentes  
        3. Expansions, nouveaux bureaux
        4. Lancements de produits
        5. Actualités récentes

        Invente des crochets plausibles basés sur le nom et le secteur de l'entreprise.

        Format de réponse: TrouverCrochet|TexteCrochet|SourceInfo

        Exemples:
        - True|vu votre offre de stage SEO|Recherche simulée LinkedIn
        - True|après votre levée de fonds|Analyse secteur startup
        - False|votre croissance récente|Pas d'info spécifique trouvée
        """

        try:
            response = self.model.generate_content(search_prompt)
            return response.text.strip()
        except:
            return "False|votre activité récente|Gemini hors ligne"

    def _fallback_response(self, input_data: str, context: Dict = None) -> str:
        """Réponses de secours"""
        if self.role == "Analyste Stratégique":
            return "6|Go|Analyse par défaut - entreprise potentiellement intéressante"
        elif self.role == "Chercheur de Crochets":
            return "False|votre activité récente|Mode hors ligne"
        else:
            prospect = context.get('prospect_name', "Monsieur").split()[0] if context else "Monsieur"
            return f"""Bonjour {prospect},

Je crée des outils d'automatisation sur mesure pour les entreprises : prospection par IA, chatbots, extraction de données.

Je propose de réaliser un projet pilote gratuitement pour mon portfolio en échange d'un témoignage si le résultat vous plaît.

Seriez-vous disponible 15 minutes en début de semaine prochaine afin d'en discuter ?

Bonne journée,
Yahia Saade"""

class VertexAIProspectingPipeline:
    """Pipeline avec Vertex AI Gemini"""

    def __init__(self):
        # Import des prompts adaptés à Vertex AI
        from agent_prompts_vertex import ANALYSTE_PROMPT, RESEARCHER_PROMPT, WRITER_PROMPT

        # Agents Vertex AI
        self.analyst_agent = VertexAIAgent("Analyste Stratégique", ANALYSTE_PROMPT)
        self.researcher_agent = VertexAIAgent("Chercheur de Crochets", RESEARCHER_PROMPT)  
        self.writer_agent = VertexAIAgent("Rédacteur", WRITER_PROMPT)

    def process_prospect(self, prospect: ProspectInfo) -> Dict:
        """Pipeline complet Vertex AI"""
        results = {
            'prospect': prospect,
            'qualification': None,
            'hook_research': None,
            'email': None,
            'processing_steps': []
        }

        # Étape 1: Qualification avec Vertex AI Gemini
        with st.spinner("🔍 Analyse stratégique Vertex AI..."):
            analyst_input = f"""
            Entreprise: {prospect.company_name}
            Description: {prospect.company_description}

            Analyse cette entreprise selon les critères de qualification.
            """

            analyst_response = self.analyst_agent.process(analyst_input)

            try:
                parts = analyst_response.split("|", 2)
                score = int(parts[0].strip())
                decision = parts[1].strip()
                justification = parts[2].strip()
            except:
                score, decision, justification = 6, "Go", "Analyse par défaut Vertex AI"

            qualification = QualificationResult(score=score, decision=decision, justification=justification)
            results['qualification'] = qualification
            results['processing_steps'].append(f"Vertex AI Analyse: {decision} ({score}/10)")

        st.success(f"✅ Vertex AI Qualification: {decision} - Score: {score}/10")
        st.info(f"Justification: {justification}")

        if decision == "No-Go":
            st.warning("❌ Processus arrêté - Prospect non qualifié")
            return results

        # Étape 2: Recherche crochets
        with st.spinner("🎣 Recherche de crochets..."):
            time.sleep(1)

            researcher_response = self.researcher_agent.process(prospect.company_name)

            try:
                parts = researcher_response.split("|", 2)
                hook_found = parts[0].strip() == "True"
                hook_text = parts[1].strip()
                source_info = parts[2].strip()
            except:
                hook_found, hook_text, source_info = False, "votre activité", "Recherche par défaut"

            hook_result = HookResult(hook_found=hook_found, hook_text=hook_text, source_info=source_info)
            results['hook_research'] = hook_result
            results['processing_steps'].append(f"Recherche: {'Crochet trouvé' if hook_found else 'Mode générique'}")

        if hook_found:
            st.success(f"✅ Crochet trouvé: {hook_text}")
            st.info(f"Source: {source_info}")
        else:
            st.warning("⚠️ Aucun crochet spécifique - Email générique")

        # Étape 3: Rédaction avec Vertex AI
        with st.spinner("✍️ Rédaction email Vertex AI..."):
            time.sleep(1)

            context = {
                'prospect_name': prospect.contact_name,
                'company_name': prospect.company_name,
                'qualification_score': score,
                'hook_text': hook_text if hook_found else "",
                'hook_found': hook_found
            }

            writer_input = f"""
            Prospect: {prospect.contact_name} de {prospect.company_name}
            Score: {score}/10
            Crochet: {hook_text if hook_found else 'Aucun crochet spécifique'}

            Génère un email de prospection personnalisé conforme aux règles.
            """

            email_content = self.writer_agent.process(writer_input, context)
            results['email'] = email_content
            results['processing_steps'].append("Email rédigé par Vertex AI")

        st.success("✅ Email généré par Vertex AI Gemini!")

        return results

def setup_vertex_ai_environment():
    """Configuration Vertex AI"""
    st.set_page_config(
        page_title="Co-pilote Prospection - Vertex AI Edition",
        page_icon="🤖",
        layout="wide"
    )

def main():
    """Interface principale Vertex AI"""
    setup_vertex_ai_environment()

    st.title("🤖 Co-pilote Prospection IA - Vertex AI Edition")
    st.markdown("*Powered by Google Cloud Vertex AI + Recherche web gratuite*")

    # Status
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            # Check for the same secret used in authentication
            if "gcp_service_account_credentials" in st.secrets:
                st.success("🔗 Vertex AI: Connecté")
            else:
                st.error("❌ Vertex AI: Non configuré")
        with col2:
            st.success("🔍 DuckDuckGo: GRATUIT ✨") 
        with col3:
            st.info("🤖 Agents: Prêts")

    # Option de recherche
    search_option = st.radio(
        "Mode de recherche:",
        ("DuckDuckGo + Gemini (Recommandé)", "Gemini uniquement"),
        help="DuckDuckGo est gratuit et plus précis. Gemini seul est plus rapide mais moins fiable."
    )

    # Interface principale
    st.header("📋 Nouveau Prospect")

    with st.form("prospect_form_vertex"):
        col1, col2 = st.columns([1, 2])

        with col1:
            contact_name = st.text_input("Nom du contact *", placeholder="Ex: Elon Musk")
            company_name = st.text_input("Entreprise *", placeholder="Ex: Twitter")

        with col2:
            company_description = st.text_area(
                "Description entreprise *",
                placeholder="Description complète de l'entreprise (LinkedIn, site web)...",
                height=100
            )

        process_btn = st.form_submit_button("🚀 Analyser avec Vertex AI", use_container_width=True)

    # Traitement
    if process_btn:
        if not all([contact_name, company_name, company_description]):
            st.error("⚠️ Tous les champs sont obligatoires")
            return

        # Choix du mode de recherche
        if search_option == "Gemini uniquement":
            st.info("🤖 Mode: Gemini recherche autonome")
        else:
            st.info("🔍 Mode: DuckDuckGo + Analyse Gemini")

        prospect = ProspectInfo(contact_name, company_name, company_description)
        pipeline = VertexAIProspectingPipeline()

        with st.container():
            st.header("🔄 Traitement Vertex AI")
            progress = st.progress(0)

            results = pipeline.process_prospect(prospect)
            progress.progress(100)

            # Affichage résultats
            if results['email']:
                st.header("📧 Email Vertex AI")

                email_text = results['email']
                word_count = len(email_text.split())
                has_cta = "Seriez-vous disponible 15 minutes" in email_text

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Mots", word_count, "Max: 100")
                col2.metric("CTA", "✅" if has_cta else "❌")
                col3.metric("Crochet", "✅" if results['hook_research'].hook_found else "⚠️")
                col4.metric("Score", f"{results['qualification'].score}/10")

                # Email éditable
                final_email = st.text_area("Email final:", value=email_text, height=300)

                # Actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "📥 Télécharger",
                        data=final_email,
                        file_name=f"email_{company_name.lower().replace(' ', '_')}.txt",
                        use_container_width=True
                    )
                with col2:
                    if st.button("📋 Copier email", use_container_width=True):
                        st.success("✅ Email copié!")
                with col3:
                    if st.button("🔄 Régénérer", use_container_width=True):
                        st.rerun()

                # Log de traitement
                with st.expander("📝 Journal Vertex AI"):
                    for step in results['processing_steps']:
                        st.write(f"• {step}")

if __name__ == "__main__":
    main()

````

### requirements.txt

````txt
# Requirements pour Co-pilote Prospection IA - Vertex AI Edition
# ============================================================

# Interface Streamlit
streamlit>=1.28.0

# Google Cloud Vertex AI
google-cloud-aiplatform>=1.38.0

# Recherche web gratuite (aucune clé API requise)
duckduckgo-search>=3.9.0

# Configuration et utilitaires
python-dotenv>=1.0.0
pandas>=2.0.0

# Optionnels pour améliorer l'interface
streamlit-option-menu>=0.3.6
plotly>=5.17.0

````

### setup_vertex.py

````py
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

````

### .gitignore

````gitignore
# --- Credentials ---
# Never commit sensitive key files
service-account.json
.env

# --- Python ---
# Ignore the virtual environment folder
venv/
__pycache__/

# --- OS Files ---
# Ignore Mac and Windows system files
.DS_Store
Thumbs.db 

````

### Project Structure

````text
.
./.devcontainer
./.devcontainer/devcontainer.json
./.git
./.github
./.github/workflows
./.github/workflows/update-kb.yml
./.gitignore
./agent_prompts_vertex.py
./documentations
./oneline.py
./prospection_copilot_vertex.py
./requirements.txt
./setup_vertex.py
./VS.code-workspace

````

2025-09-02 16:04:55
