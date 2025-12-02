from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import settings
from app.schemas.analysis import CVExtractionResult, JobDescriptionAnalysis

AUTHORIZED_JOBS = """
A. Tech – Général:
Développeur web, Développeur front-end, Développeur back-end, Développeur full-stack, 
Développeur mobile, Développeur cloud, Data scientist, Data analyst, Data engineer, 
Machine learning engineer, Deep learning engineer, Software engineer, DevOps engineer, 
Tech lead

B. Développement – Back-end:
Développeur Python, Développeur Django, Développeur Flask, Développeur Laravel, 
Développeur PHP, Développeur Java, Développeur Node.js, Développeur Ruby on Rails, 
Développeur Symfony, Développeur Go, Développeur Rust, Développeur C++, Développeur .NET, 
Développeur Kotlin, Développeur Swift, Développeur Android, Développeur Salesforce, 
Développeur Blockchain

C. Développement – Front-end:
Développeur React, Développeur Next.js, Développeur Vue.js, Développeur Angular, 
Développeur Svelte, Développeur Flutter, Développeur Webflow, Développeur WordPress, 
Développeur HTML/CSS

D. Développement – Spécialités:
Développeur Web3, Développeur IA, Développeur AR/VR, Développeur jeux vidéo, 
Développeur no-code, Développeur RPA

E. IA & Data:
AI engineer, NLP engineer, Computer vision engineer, Data warehouse developer, 
Business intelligence analyst, Chief data officer (CDO), Data quality analyst, Big data engineer

F. Design & Audiovisuel
UX designer, UI designer, Product designer, Designer graphique, Motion designer, Directeur
artistique, Illustrateur, Animateur 2D/3D, Vidéaste, Monteur vidéo, Coloriste, Ingénieur du
son

G. Marketing & Communication digitale
Social media manager, Community manager, Consultant SEO, Rédacteur SEO, Content
manager, Copywriter, Email marketing specialist, PPC expert, CRM manager, Meta Ads
manager, Google Ads manager, Growth hacker, Affiliate marketing manager, Product
marketer
"""

class LLMService:
    def __init__(self):
        self.llm = ChatMistralAI(
            mistral_api_key=settings.MISTRAL_API_KEY,
            model=settings.MISTRAL_MODEL,
            temperature=0.3 # moderate for a good balance between creativity and accuracy
        )

    async def analyze_cv(self, cv_text: str) -> dict:
        """
        Extract structured data from CV text using Mistral with structured output.
        Returns a dict matching CVExtractionResult schema.
        """
        structured_llm = self.llm.with_structured_output(CVExtractionResult)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Tu es un expert RH et un assistant IA spécialisé dans l'analyse de CV."
                       "Ta tâche est d'extraire les informations clés d'un CV et de les structurer."
                       "Sois précis et exhaustif."
                       "Pour le 'job_title', tu DOIS OBLIGATOIREMENT choisir le métier le plus proche parmi la liste officielle suivante."
                       "Si aucun métier ne correspond exactement, choisis le plus pertinent dans la liste."
                       "\n\nLISTE OFFICIELLE DES MÉTIERS :\n{authorized_jobs}\n\n"
                       "Pour 'seniority', choisis parmi: Junior, Confirmé, Senior, Expert."),
            ("user", "Voici le contenu du CV :\n\n{cv_text}")
        ])

        chain = prompt | structured_llm

        try:
            result = await chain.ainvoke({
                "cv_text": cv_text,
                "authorized_jobs": AUTHORIZED_JOBS
            })
           
            # Convert Pydantic model to dict for compatibility with the rest of the app
            return result.model_dump()
        
        except Exception as e:
            print(f"Error in analyze_cv: {e}")
            raise e

    async def analyze_job_description(self, job_text: str) -> dict:
        """
        Extract key requirements from Job Description using structured output.
        """
        structured_llm = self.llm.with_structured_output(JobDescriptionAnalysis)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Tu es un expert RH. Analyse cette offre d'emploi et extrais les compétences et critères requis."),
            ("user", "Offre d'emploi :\n\n{job_text}")
        ])
        
        chain = prompt | structured_llm

        try:
            result = await chain.ainvoke({
                "job_text": job_text
            })

            return result.model_dump()
        except Exception as e:
            print(f"Error in analyze_job: {e}")
            raise e

    async def generate_report(self, cv_data: dict, job_data: dict, matching_score: float) -> str:
        """
        Generate a human-readable report in Markdown.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Tu es un consultant RH senior expert. 
             Rédige un rapport d'évaluation professionnel et structuré pour un recruteur.

Tu DOIS utiliser le format Markdown suivant EXACTEMENT :

## Synthèse Globale
[Paragraphe de synthèse]

## Points Forts
- Point fort 1
- Point fort 2
- Point fort 3

## Points de Vigilance
- Point d'attention 1
- Point d'attention 2

## Conclusion
[Conclusion]
             
## RECOMMANDATION FINALE
[Recommandation finale]
    

Utilise des **mots en gras** pour les éléments importants."""),
            ("user", """
Informations du Candidat :
- Poste identifié : {job_title}
- Niveau d'expérience : {seniority}
- Compétences techniques : {cv_skills}
- Soft skills : {cv_soft_skills}
- Technologies maîtrisées : {cv_technologies}

Exigences du Poste :
- Compétences requises : {job_skills}
- Soft skills requis : {job_soft_skills}
- Technologies requises : {job_technologies}
- Niveau d'expérience requis : {job_experience}

Score de compatibilité calculé : **{score}/100**

Rédige maintenant le rapport d'évaluation en Markdown.
Utilise un ton professionnel, concret et objectif.""")
        ])
        
        chain = prompt | self.llm
        
        # Extraction des données pour le prompt
        cv_analysis = cv_data.get('cv_analysis', {})
        job_classification = cv_data.get('job_classification', {})
        
        response = await chain.ainvoke({
            "job_title": job_classification.get('job_title', 'Non identifié'),
            "seniority": cv_analysis.get('seniority', 'Non précisé'),
            "cv_skills": ', '.join(cv_analysis.get('technical_skills', [])[:10]) or 'Non précisées',
            "cv_soft_skills": ', '.join(cv_analysis.get('soft_skills', [])[:5]) or 'Non précisées',
            "cv_technologies": ', '.join(cv_analysis.get('technologies', [])[:8]) or 'Non précisées',
            "job_skills": ', '.join(job_data.get('required_technical_skills', [])[:10]) or 'Non précisées',
            "job_soft_skills": ', '.join(job_data.get('required_soft_skills', [])[:5]) or 'Non précisées',
            "job_technologies": ', '.join(job_data.get('required_technologies', [])[:8]) or 'Non précisées',
            "job_experience": job_data.get('required_experience_level', 'Non précisé'),
            "score": matching_score
        })
        
        return response.content
