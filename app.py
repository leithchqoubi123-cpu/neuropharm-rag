# ========================================
# NEUROPHARM AI - Version Production
# ========================================

import streamlit as st
from google.cloud import discoveryengine_v1beta as discoveryengine
import logging

# --- CONFIGURATION SÉCURISÉE ---
# Le code va chercher les clés dans les secrets de Streamlit (.streamlit/secrets.toml)
try:
    PROJECT_ID = st.secrets["GCP_PROJECT_ID"]
    DATA_STORE_ID = st.secrets["GCP_DATA_STORE_ID"]
    LOCATION = "global" # Souvent global, mais peut être mis en secret aussi
except FileNotFoundError:
    st.error("❌ Erreur : Le fichier de secrets est introuvable.")
    st.stop()
except KeyError as e:
    st.error(f"❌ Erreur : La clé {e} est manquante dans les secrets.")
    st.stop()

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CLIENT CACHÉ (Performance) ---
@st.cache_resource
def get_search_client():
    """Crée le client Vertex AI UNE SEULE FOIS"""
    try:
        client = discoveryengine.SearchServiceClient()
        logger.info("✅ Client Vertex AI créé")
        return client
    except Exception as e:
        logger.error(f"❌ Erreur création client : {e}")
        return None

# --- FONCTION RAG ---
def search_rag(question):
    """Interroge Vertex AI Search"""
    client = get_search_client()

    if client is None:
        return "❌ Impossible de se connecter à Vertex AI. Vérifie ton authentification.", []

    try:
        serving_config = client.serving_config_path(
            project=PROJECT_ID,
            location=LOCATION,
            data_store=DATA_STORE_ID,
            serving_config="default_config",
        )

        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=question,
            page_size=3,
            content_search_spec={
                "snippet_spec": {"return_snippet": True},
                "summary_spec": {
                    "summary_result_count": 3,
                    "include_citations": True
                }
            }
        )

        logger.info(f"📤 Envoi requête : {question[:50]}...")
        response = client.search(request)

        summary = getattr(response.summary, 'summary_text', 'Aucune réponse générée.')
        results = list(response.results) if hasattr(response, 'results') else []

        logger.info(f"📥 Réponse reçue : {len(results)} sources")
        return summary, results

    except Exception as e:
        logger.error(f"❌ Erreur RAG : {type(e).__name__} - {str(e)}")
        return f"⚠️ Erreur technique : {type(e).__name__}", []

# --- INTERFACE STREAMLIT ---
st.set_page_config(
    page_title="NeuroPharm AI",
    page_icon="🧠",
    layout="centered"
)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=100)
    st.title("NeuroPharm 🧠")
    st.info("💊 Assistant RAG médical basé sur sources officielles (HAS, SFEMC)")

    st.divider()

    # Statistiques
    if "messages" in st.session_state:
        nb_questions = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("Questions posées", nb_questions)

    # Bouton reset
    if st.button("🔄 Nouvelle conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    # Disclaimer
    with st.expander("⚠️ Avertissement médical"):
        st.caption("""
        Cet outil est un assistant documentaire.
        Il ne remplace PAS l'avis d'un professionnel de santé.
        Consultez toujours un médecin pour un diagnostic.
        """)

# --- INTERFACE PRINCIPALE ---
st.title("🧠 Assistant Migraine Expert")
st.caption("Pose tes questions sur la prise en charge de la migraine")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Affiche les sources si présentes
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📚 Sources consultées"):
                for src in message["sources"]:
                    st.caption(f"- {src}")

# ===== CHAT INPUT (Zone critique) =====
if prompt := st.chat_input("Ex: Quels sont les traitements de crise de la migraine ?"):

    # Validation
    prompt_clean = prompt.strip()
    if len(prompt_clean) < 10:
        st.warning("⚠️ Question trop courte (minimum 10 caractères)")
        st.stop()

    if len(prompt_clean) > 500:
        st.error("❌ Question trop longue (maximum 500 caractères)")
        st.stop()

    # Affiche la question
    st.session_state.messages.append({"role": "user", "content": prompt_clean})
    with st.chat_message("user"):
        st.markdown(prompt_clean)

    # Génère la réponse
    with st.chat_message("assistant"):
        with st.spinner("🔍 Analyse des documents officiels en cours..."):
            reponse_texte, sources = search_rag(prompt_clean)
            st.markdown(reponse_texte)

            # Extraction des titres de sources
            source_titles = []
            if sources:
                st.markdown("---")
                st.caption("📚 **Sources utilisées :**")
                for doc in sources:
                    try:
                        data = doc.document.derived_struct_data
                        titre = data.get('title', data.get('link', 'Document PDF'))
                        st.caption(f"- {titre}")
                        source_titles.append(titre)
                    except Exception as e:
                        logger.warning(f"Erreur extraction source : {e}")
                        continue

    # Sauvegarde dans l'historique avec sources
    st.session_state.messages.append({
        "role": "assistant",
        "content": reponse_texte,
        "sources": source_titles
    })

# --- FOOTER ---
st.divider()
st.caption("🔬 Propulsé par Google Vertex AI Search | 🔒 Sources conformes HAS/SFEMC")
