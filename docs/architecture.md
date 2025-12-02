# Architecture technique - Agent IA RH

## Vue d'ensemble

L'application est conçue selon une architecture moderne séparant le frontend (client) du backend (serveur), avec une intégration forte de services d'Intelligence Artificielle (LLM).

### Diagramme de flux de données

1. **Utilisateur** -> Upload CV + Description de poste (Frontend)
2. **Frontend** -> Envoi des fichiers via API REST (Backend)
3. **Backend** -> Extraction du texte (Parsers)
4. **Backend** -> Analyse sémantique et extraction d'entités (Mistral AI)
5. **Backend** -> Vectorisation et calcul de similarité (Mistral Embeddings)
6. **Backend** -> Génération du rapport (Mistral AI)
7. **Backend** -> Réponse JSON structurée (Frontend)
8. **Frontend** -> Affichage des résultats et graphiques

---

## Composants détaillés

### 1. Frontend (Client)
- **Framework** : React 18 avec Vite.
- **Langage** : TypeScript pour la robustesse du typage.
- **UI Library** : Shadcn/ui + Tailwind CSS pour un design moderne et responsive.
- **Gestion d'état** : React Query pour la gestion des requêtes API et du cache.
- **Visualisation** : Recharts pour les graphiques de compétences.

### 2. Backend (Serveur)
- **Framework** : FastAPI (Python) pour sa rapidité et sa gestion native de l'asynchrone.
- **Structure** :
    - `api/` : Routes et endpoints.
    - `core/` : Configuration et paramètres globaux.
    - `schemas/` : Modèles de données Pydantic (Validation).
    - `services/` : Logique métier (LLM, Parsing, Matching).
- **Parsing** :
    - `pypdf` pour les PDF natifs.
    - `python-docx` pour les fichiers Word.
    - `pytesseract` + `pdf2image` pour l'OCR (PDF scannés).

### 3. Intelligence Artificielle & Matching
- **LLM** : Mistral AI (via LangChain) pour :
    - L'extraction structurée d'informations (JSON output).
    - La classification des métiers.
    - La rédaction du rapport final.
- **Matching Engine** :
    - Utilisation de `MistralAIEmbeddings` pour transformer les compétences et descriptions en vecteurs mathématiques.
    - Calcul de la **Cosine Similarity** pour évaluer la proximité sémantique entre le CV et l'offre, au-delà des simples mots-clés.
    - Algorithme de scoring pondéré :
        - Compétences techniques : 40%
        - Soft Skills : 20%
        - Expérience : 20%
        - Technologies : 20%

### 4. Infrastructure & déploiement
- **Docker** : Containerisation de l'application backend incluant les dépendances système (OCR).
- **CI/CD** : Compatible avec les pipelines standards (GitHub Actions, Vercel, Render).

## Sécurité
- Gestion des clés API via variables d'environnement (`.env`).
- Validation stricte des entrées via Pydantic.
- CORS configuré pour restreindre l'accès aux origines autorisées.
