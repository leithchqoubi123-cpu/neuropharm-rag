# 🧠 NeuroPharm AI - Assistant RAG Migraine

**NeuroPharm AI** est un assistant intelligent spécialisé dans la prise en charge de la migraine. 

Contrairement à un ChatGPT classique, il utilise une architecture **RAG (Retrieval-Augmented Generation)** connectée à **Google Vertex AI Search**. Il ne répond qu'en se basant sur une base de connaissances fermée et vérifiée : les lois et recommandations officielles françaises (HAS, SFEMC).

## 🚀 Fonctionnalités Clés

* **🕵️‍♂️ Zéro Hallucination** : L'IA répond uniquement si l'information est dans les documents officiels.
* **📚 Citations Précises** : Chaque affirmation est sourcée avec un lien vers le document PDF d'origine.
* **🏥 Expert Médical** : Capable de répondre sur les traitements, les contre-indications (ex: Triptans) et le diagnostic.
* **🔒 Sécurité** : Gestion des accès via Google Cloud IAM et secrets sécurisés.

## 🛠️ Stack Technique

Ce projet démontre l'utilisation de technologies Cloud modernes :

* **Moteur IA & Indexation** : Google Cloud Vertex AI Search & Conversation
* **Interface Utilisateur** : Streamlit (Python)
* **Infrastructure** : Google Colab & Ngrok (Tunneling sécurisé)
* **Langage** : Python 3.10+

## ⚙️ Installation et Configuration

Pour tester ce projet localement :

1.  **Cloner le dépôt**
    ```bash
    git clone https://github.com/leithchqoubi123/neuropharm-rag.git
cd neuropharm-rag
    ```

2.  **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurer les Secrets (Indispensable)**
    Ce projet nécessite un accès à un projet Google Cloud avec Vertex AI activé.
    Créez un dossier `.streamlit` et un fichier `secrets.toml` à la racine :
    
    ```toml
    # .streamlit/secrets.toml
    GCP_PROJECT_ID = "votre-id-projet-google"
    GCP_DATA_STORE_ID = "votre-id-datastore-vertex"
    ```

4.  **Lancer l'application**
    ```bash
    streamlit run app.py
    ```

## ⚠️ Avertissement

Cet outil est une démonstration technique (POC) à visée éducative. Il ne remplace en aucun cas l'avis d'un professionnel de santé.

---
*Projet réalisé par [CHQOUBI Leith] - 2026*