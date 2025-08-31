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

        # Configuration Vertex AI
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        if not project_id:
            st.error("""
            ⚠️ Configuration Google Cloud manquante. Définissez:
            - GOOGLE_CLOUD_PROJECT=your-project-id
            - GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
            """)
            st.stop()

        # Initialisation Vertex AI
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-1.5-flash")

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

    # Vérification Google Cloud
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not project_id or not credentials_path:
        st.error("""
        🔑 **Configuration Google Cloud requise:**

        1. **Projet Google Cloud**: Créez un projet sur [Google Cloud Console](https://console.cloud.google.com)
        2. **Activez Vertex AI API**: Dans votre projet GCP
        3. **Service Account**: Créez une clé de service avec rôle Vertex AI User
        4. **Variables d'environnement**:
           ```
           GOOGLE_CLOUD_PROJECT=your-project-id
           GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
           ```

        📌 **DuckDuckGo**: 100% GRATUIT, aucune configuration !
        """)
        st.stop()

def main():
    """Interface principale Vertex AI"""
    setup_vertex_ai_environment()

    st.title("🤖 Co-pilote Prospection IA - Vertex AI Edition")
    st.markdown("*Powered by Google Cloud Vertex AI + Recherche web gratuite*")

    # Status
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            if os.getenv("GOOGLE_CLOUD_PROJECT"):
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
            contact_name = st.text_input("Nom du contact *", placeholder="Ex: Kevin Martin")
            company_name = st.text_input("Entreprise *", placeholder="Ex: Made In Tracker")

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
