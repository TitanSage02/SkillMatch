from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API pour l'analyse automatisée de candidatures par SkillMatch, l'Agent IA spécialisé en Ressources Humaines.",
)

# Log des origines autorisées au démarrage
logger.info(f"CORS Allowed Origins: {settings.ALLOWED_ORIGINS}")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Configuration depuis settings
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de SkillMatch. Documentation sur /docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
