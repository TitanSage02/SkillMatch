import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface JobClassification {
  job_title: string;
  confidence: number;
  alternative_jobs: string[];
}

export interface Experience {
  title: string;
  company: string;
  duration?: string;
  description?: string;
}

export interface Education {
  degree: string;
  school: string;
  year?: string;
}

export interface CVAnalysis {
  technical_skills: string[];
  soft_skills: string[];
  experiences: Experience[];
  educations: Education[];
  seniority: string;
  languages: string[];
}

export interface MatchingDetails {
  skills_score: number;
  experience_score: number;
  technologies_score: number;
  soft_skills_score: number;
}

export interface MatchingResult {
  overall_score: number;
  recommendation: "strongly_recommended" | "recommended" | "not_recommended";
  matched_skills: string[];
  missing_skills: string[];
  details: MatchingDetails;
}

export interface AnalysisResponse {
  job_classification: JobClassification;
  cv_analysis: CVAnalysis;
  matching: MatchingResult;
  report: string;
}

export const api = {
  analyze: async (cvFile: File, jobDescription: string): Promise<AnalysisResponse> => {
    const formData = new FormData();
    formData.append('cv', cvFile);
    formData.append('job_description', jobDescription);

    const response = await axios.post<AnalysisResponse>(`${API_URL}/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};
