from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.analysis import AnalysisResponse
from app.services.parsers.extractor import TextExtractor
from app.services.llm.mistral_client import LLMService
from app.services.matching.scorer import MatchingService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Instanciation des services
llm_service = LLMService()
matching_service = MatchingService()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_application(
    cv: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Endpoint principal pour analyser une candidature.
    1. Extrait le texte du CV.
    2. Analyse le CV avec le LLM.
    3. Analyse l'offre d'emploi avec le LLM.
    4. Calcule le matching via Embeddings.
    5. Génère un rapport final.
    """
    try:
        # 1. Parsing du CV
        logger.info(f"Processing file: {cv.filename}")
        content = await cv.read()
        cv_text = TextExtractor.extract(cv.filename, content)
        
        if not cv_text:
            raise HTTPException(status_code=400, detail="Impossible d'extraire du texte du fichier.")

        # 2. Analyse IA (Parallélisable en théorie, ici séquentiel pour simplicité)
        logger.info("Analyzing CV with LLM...")
        cv_data = await llm_service.analyze_cv(cv_text)
        
        logger.info("Analyzing Job Description with LLM...")
        job_data = await llm_service.analyze_job_description(job_description)

        # 3. Matching
        logger.info("Calculating matching score...")
        matching_result = await matching_service.calculate_score(cv_data, job_data) ### ANALYSE POINTUE A VENIR A CE NIVEAU

        # 4. Génération de rapport
        logger.info("Generating report...")
        report = await llm_service.generate_report(
            cv_data, 
            job_data, 
            matching_result['overall_score']
        )

        # Construction de la réponse
        return AnalysisResponse(
            job_classification=cv_data.get('job_classification'),
            cv_analysis=cv_data.get('cv_analysis'),
            matching=matching_result,
            report=report
        )

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Internal error: {e}")
        raise HTTPException(status_code=500, detail=f"Une erreur interne est survenue: {str(e)}")
