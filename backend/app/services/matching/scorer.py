from typing import List, Dict, Tuple, Optional
import numpy as np
import logging
from langchain_mistralai import MistralAIEmbeddings
from app.core.config import settings

logger = logging.getLogger(__name__)

class MatchingService:
    """
    Service de matching intelligent entre CV et offres d'emploi.
    Utilise Mistral Embeddings pour la similarité sémantique.
    """
    
    # Poids de pondération pour le score global 
    WEIGHTS = {
        'technical_skills': 0.40,       # 40% - Compétences techniques
        'soft_skills': 0.20,            # 20% - Compétences comportementales
        'experience': 0.20,             # 20% - Niveau d'expérience
        'technologies': 0.20            # 20% - Technologies et outils
    }

    # Seuils de recommandation
    RECOMMENDATION_THRESHOLDS = {
        'strongly_recommended': 80,     # Fortement recommandé
        'consider': 50,                 # À considérer (entretien conseillé)
        # < 50: Non recommandé
    }
    
    # Niveaux de séniorité
    SENIORITY_LEVELS = {
        'junior': 1,
        'intermédiaire': 2,
        'confirmé': 2,
        'senior': 3,
        'expert': 4
    }

    def __init__(self):
        """
        Initialise le service avec Mistral Embeddings.
        """
        try:
            self.embeddings = MistralAIEmbeddings(
                mistral_api_key=settings.MISTRAL_API_KEY,
                model="mistral-embed"
            )
            logger.info("Client Mistral Embeddings initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de Mistral Embeddings: {e}")
            raise

    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calcule la similarité cosinus entre deux vecteurs."""
        if vec1 is None or vec2 is None:
            return 0.0
        
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return float(np.dot(vec1, vec2) / (norm1 * norm2))

    async def _get_embeddings_batch(self, texts: List[str]) -> Dict[str, np.ndarray]:
        """Récupère les embeddings pour une liste de textes en un seul appel."""
        # Filtrer les textes vides et dédoublonner
        unique_texts = list(set(t for t in texts if t and t.strip()))
        if not unique_texts:
            return {}

        try:
            embeddings = await self.embeddings.aembed_documents(unique_texts)
            return {text: np.array(emb) for text, emb in zip(unique_texts, embeddings)}
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des embeddings: {e}")
            return {}

    def _extract_list(self, data: dict, *keys) -> List[str]:
        """Extrait une liste depuis un dictionnaire imbriqué."""
        try:
            value = data
            for key in keys:
                value = value.get(key, {})
            return value if isinstance(value, list) else []
        except (AttributeError, TypeError):
            return []

    def _extract_value(self, data: dict, *keys, default=''):
        """Extrait une valeur depuis un dictionnaire imbriqué."""
        try:
            value = data
            for key in keys:
                value = value.get(key, default)
            return value if value else default
        except (AttributeError, TypeError):
            return default

    def _calculate_experience_match(self, cv_level: str, job_level: str) -> float:
        """
        Compare les niveaux d'expérience.
        """
        cv_level = cv_level.lower().strip() if cv_level else 'junior'
        job_level = job_level.lower().strip() if job_level else 'junior'
        
        cv_val = self.SENIORITY_LEVELS.get(cv_level, 1)
        job_val = self.SENIORITY_LEVELS.get(job_level, 1)
        
        diff = cv_val - job_val
        
        if diff >= 0:
            return 100.0    # Surqualifié ou parfait
        elif diff == -1:
            return 75.0     # Un niveau en dessous
        elif diff == -2:
            return 50.0     # Deux niveaux en dessous
        else:
            return 25.0     # Trop junior

    def _identify_matched_and_missing_skills(
        self, 
        cv_skills: List[str], 
        job_skills: List[str],
        embedding_map: Dict[str, np.ndarray]
    ) -> Tuple[List[str], List[str]]:
        """
        Identifie les compétences correspondantes et manquantes en utilisant la map d'embeddings.
        """
        if not cv_skills or not job_skills:
            return ([], job_skills if job_skills else [])
        
        cv_skills_norm = [s.lower().strip() for s in cv_skills if s]
        job_skills_norm = [s.lower().strip() for s in job_skills if s]
        
        matched = []
        missing = []
        
        for job_skill in job_skills_norm:
            # Match exact
            if job_skill in cv_skills_norm:
                matched.append(job_skill)
                continue
            
            # Match sémantique
            is_match = False
            job_vec = embedding_map.get(job_skill)
            
            if job_vec is not None:
                for cv_skill in cv_skills_norm:
                    cv_vec = embedding_map.get(cv_skill)
                    if cv_vec is not None:
                        sim = self._cosine_similarity(job_vec, cv_vec)
                        if sim > 0.85:
                            matched.append(job_skill)
                            is_match = True
                            break
            
            if not is_match:
                missing.append(job_skill)
        
        return (matched, missing)

    async def calculate_score(self, cv_data: dict, job_data: dict) -> dict:
        """
        Calcule le score de correspondance CV ↔ offre.
        """
        try:            
            # Extraction des informations clés du CV
            cv_technical = self._extract_list(cv_data, 'cv_analysis', 'technical_skills')
            cv_soft = self._extract_list(cv_data, 'cv_analysis', 'soft_skills')
            cv_technologies = self._extract_list(cv_data, 'cv_analysis', 'technologies')

            cv_seniority = self._extract_value(cv_data, 'cv_analysis', 'seniority', default='Junior')
            cv_experiences = self._extract_list(cv_data, 'cv_analysis', 'experiences')
            
            # Extraction des informations clés de l'offre
            job_technical = self._extract_list(job_data, 'required_technical_skills')
            job_soft = self._extract_list(job_data, 'required_soft_skills')
            job_technologies = self._extract_list(job_data, 'required_technologies')

            job_experience = self._extract_value(job_data, 'required_experience_level', default='Junior')
            
            # Préparation des textes pour embedding
            cv_tech_str = " ".join(cv_technical) if cv_technical else ""
            job_tech_str = " ".join(job_technical) if job_technical else ""
            
            cv_soft_str = " ".join(cv_soft) if cv_soft else ""
            job_soft_str = " ".join(job_soft) if job_soft else ""
            
            cv_tools_str = " ".join(cv_technologies) if cv_technologies else cv_tech_str
            job_tools_str = " ".join(job_technologies) if job_technologies else job_tech_str
            
            # Collecte de tous les textes uniques à vectoriser
            texts_to_embed = [
                cv_tech_str, job_tech_str,
                cv_soft_str, job_soft_str,
                cv_tools_str, job_tools_str
            ]
            
            # Ajout des compétences individuelles pour le matching détaillé
            cv_skills_all = [s.lower().strip() for s in cv_technical + cv_soft if s]
            job_skills_all = [s.lower().strip() for s in job_technical + job_soft if s]
            texts_to_embed.extend(cv_skills_all)
            texts_to_embed.extend(job_skills_all)
            
            # Récupération des embeddings en batch
            embedding_map = await self._get_embeddings_batch(texts_to_embed)

            # ========== CALCUL DES SCORES  ==========
            # 1. Score Compétences Techniques
            technical_score = self._cosine_similarity(
                embedding_map.get(cv_tech_str), 
                embedding_map.get(job_tech_str)
            ) * 100 if job_tech_str else 100.0
            
            # 2. Score Compétences Comportementales
            soft_score = self._cosine_similarity(
                embedding_map.get(cv_soft_str), 
                embedding_map.get(job_soft_str)
            ) * 100 if job_soft_str else 100.0
            
            # 3. Score Expérience
            experience_score = self._calculate_experience_match(cv_seniority, job_experience)
            
            # 4. Score Technologies/Outils
            technology_score = self._cosine_similarity(
                embedding_map.get(cv_tools_str), 
                embedding_map.get(job_tools_str)
            ) * 100 if job_tools_str else 100.0
            
            # Score Global avec pondération
            overall_score = (
                (technical_score * self.WEIGHTS['technical_skills']) +
                (soft_score * self.WEIGHTS['soft_skills']) +
                (experience_score * self.WEIGHTS['experience']) +
                (technology_score * self.WEIGHTS['technologies'])
            )
            
            # ========== IDENTIFICATION DES ÉCARTS  ==========
            matched_technical, missing_technical = self._identify_matched_and_missing_skills(
                cv_technical, job_technical, embedding_map
            )
            matched_soft, missing_soft = self._identify_matched_and_missing_skills(
                cv_soft, job_soft, embedding_map
            )
            
            # Combinaison pour le rapport
            matched_skills = matched_technical + matched_soft
            missing_skills = missing_technical + missing_soft
            
            # ========== RECOMMANDATION FINALE  ==========
            if overall_score >= self.RECOMMENDATION_THRESHOLDS['strongly_recommended']:
                recommendation = 'strongly_recommended'
            elif overall_score >= self.RECOMMENDATION_THRESHOLDS['consider']:
                recommendation = 'consider'
            else:
                recommendation = 'not_recommended'
            

            # ========== GÉNÉRATION DES POINTS FORTS  ==========
            strengths = []
            if technical_score >= 80:
                strengths.append(f"Excellente maîtrise des compétences techniques requises ({len(matched_technical)}/{len(job_technical)} compétences)")

            if experience_score >= 75:
                strengths.append(f"Niveau d'expérience ({cv_seniority}) aligné avec les attentes ({job_experience})")

            if soft_score >= 80:
                strengths.append(f"Compétences comportementales bien développées ({len(matched_soft)}/{len(job_soft)} soft skills)")

            if cv_experiences and len(cv_experiences) >= 3:
                strengths.append(f"Expériences professionnelles significatives ({len(cv_experiences)} postes)")

            if technology_score >= 85:
                strengths.append("Maîtrise avancée des technologies et outils requis")
            
            if not strengths:
                strengths.append("Profil avec des bases solides à développer")
            
            # ========== POINTS D'ATTENTION ==========
            concerns = []
            if missing_technical:
                concerns.append(f"Compétences techniques manquantes: {', '.join(missing_technical[:5])}")

            if experience_score < 75:
                concerns.append(f"Niveau d'expérience insuffisant (candidat: {cv_seniority}, requis: {job_experience})")

            if missing_soft:
                concerns.append(f"Soft skills à développer: {', '.join(missing_soft[:3])}")

            if technical_score < 60:
                concerns.append("Écart important entre compétences techniques du candidat et exigences du poste")
            
            if not concerns:
                concerns.append("Aucun point d'attention majeur identifié")
            
            
            # ========== STRUCTURE FINALE DU RAPPORT  ==========
            return {
                'overall_score': round(overall_score, 1),
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'recommendation': recommendation if recommendation != 'consider' else 'recommended',
                'details': {
                    'skills_score': round(technical_score, 1),
                    'soft_skills_score': round(soft_score, 1),
                    'experience_score': round(experience_score, 1),
                    'technologies_score': round(technology_score, 1)
                }
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul du score: {e}")
            return {
                'overall_score': 0.0,
                'matched_skills': [],
                'missing_skills': [],
                'recommendation': 'not_recommended',
                'details': {
                    'skills_score': 0.0,
                    'soft_skills_score': 0.0,
                    'experience_score': 0.0,
                    'technologies_score': 0.0
                }
            }
