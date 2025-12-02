from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Modèles partagés ---
class Skill(BaseModel):
    name: str
    category: Optional[str] = None # ex: Technical, Soft, Tool
    level: Optional[str] = None

class Experience(BaseModel):
    title: str = Field(description="Intitulé du poste")
    company: str = Field(description="Nom de l'entreprise")
    duration: Optional[str] = Field(None, description="Durée ou dates")
    description: Optional[str] = Field(None, description="Description des tâches")

class Education(BaseModel):
    degree: str = Field(description="Diplôme obtenu")
    school: str = Field(description="École ou université")
    year: Optional[str] = Field(None, description="Année d'obtention")


# --- Modèles de sortie ---
class JobClassification(BaseModel):
    job_title: str = Field(..., description="Le titre du métier identifié")
    confidence: float = Field(..., description="Score de confiance entre 0 et 1")
    alternative_jobs: List[str] = Field(default=[], description="Autres métiers possibles")

class CVAnalysis(BaseModel):
    technical_skills: List[str]
    soft_skills: List[str]
    experiences: List[Experience]
    educations: List[Education]
    seniority: str = Field(..., description="Junior, Confirmé, Senior, Expert")
    languages: List[str]

class CVExtractionResult(BaseModel):
    job_classification: JobClassification
    cv_analysis: CVAnalysis

class JobDescriptionAnalysis(BaseModel):
    required_technical_skills: List[str]
    required_soft_skills: List[str]
    required_experience_level: str
    required_languages: List[str]

class MatchingDetails(BaseModel):
    skills_score: float
    experience_score: float
    technologies_score: float
    soft_skills_score: float

class MatchingResult(BaseModel):
    overall_score: float
    recommendation: str = Field(..., description="strongly_recommended, recommended, not_recommended")
    matched_skills: List[str]
    missing_skills: List[str]
    details: MatchingDetails

class AnalysisResponse(BaseModel):
    job_classification: JobClassification
    cv_analysis: CVAnalysis
    matching: MatchingResult
    report: str = Field(..., description="Rapport complet au format Markdown")
