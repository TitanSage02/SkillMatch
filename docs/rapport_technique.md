# Rapport Technique - Agent IA RH

## 1. Introduction
Ce document présente les choix techniques, l'architecture et les défis relevés lors du développement de l'Agent IA RH. L'objectif était de créer une solution robuste, évolutive et performante pour l'analyse automatisée de candidatures.

## 2. Choix Technologiques

### 2.1 Backend : FastAPI & Python
Nous avons choisi **FastAPI** pour plusieurs raisons :
- **Performance** : L'un des frameworks Python les plus rapides grâce à Starlette et Pydantic.
- **Asynchrone** : Support natif de `async/await`, indispensable pour gérer efficacement les appels I/O bound vers les API LLM (Mistral).
- **Typage fort** : Utilisation de Pydantic pour la validation des données, réduisant les bugs à l'exécution.

### 2.2 Frontend : React & Vite
- **React** : Standard de l'industrie, écosystème riche.
- **Vite** : Build tool ultra-rapide, améliorant l'expérience développeur.
- **Tailwind CSS** : Permet un développement UI rapide et cohérent.
- **Shadcn/ui** : Composants accessibles et personnalisables, basés sur Radix UI.

### 2.3 Intelligence Artificielle : Mistral AI
Le choix de **Mistral AI** (via LangChain) s'est imposé pour :
- **Performance/Coût** : Excellent rapport qualité/prix par rapport à GPT-4.
- **Capacités** : Très bon suivi des instructions (instruction following) pour l'extraction JSON structurée.

### 2.4 Matching : Embeddings Vectoriels
Plutôt qu'une simple recherche par mots-clés (keyword matching), nous avons opté pour une approche sémantique :
1. **Vectorisation** : Les compétences du CV et de l'offre sont transformées en vecteurs (embeddings) via `mistral-embed`.
2. **Similarité Cosinus** : Calcul de la distance angulaire entre les vecteurs.
Cela permet de comprendre que "React" et "React.js" sont identiques, ou que "Python" et "Django" sont liés, ce qu'une approche par mots-clés rate souvent.

## 3. Architecture

L'architecture suit le pattern **Client-Serveur** classique, découplé via une API REST.

### Flux de traitement
1. **Upload** : Le fichier est envoyé au backend.
2. **Extraction** : 
   - `pypdf` extrait le texte des PDF natifs.
   - `OCR (Tesseract)` prend le relais pour les scans (images).
3. **Analyse** : Le LLM extrait les entités nommées (Compétences, Expériences) en format JSON strict.
4. **Scoring** : Le moteur de matching compare les vecteurs et génère un score pondéré.
5. **Rapport** : Le LLM rédige une synthèse en langage naturel basée sur les données structurées.

## 4. Défis et Solutions

### 4.1 Hallucinations du LLM
**Problème** : Le LLM inventait parfois des compétences non présentes.
**Solution** : Utilisation stricte de `structured_output` (Function Calling) avec Pydantic pour forcer le modèle à ne sortir que ce qui est présent dans le texte.

### 4.2 Parsing de PDF complexes
**Problème** : Les CVs avec des mises en page complexes (colonnes) étaient mal lus.
**Solution** : Intégration d'une stratégie de fallback avec OCR pour les documents où l'extraction texte échoue.

## 5. Améliorations Futures
- **Cache** : Mettre en cache les embeddings des offres d'emploi fréquentes pour économiser des tokens.
- **Feedback Loop** : Permettre au recruteur de corriger le parsing pour affiner le modèle (Fine-tuning).
- **Support Multi-langues** : Étendre explicitement le support à d'autres langues.

## 6. Conclusion
L'application délivrée est fonctionnelle, testée et documentée. Elle respecte les meilleures pratiques de développement moderne et offre une base solide pour une industrialisation future.
