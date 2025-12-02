import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { CVUploader } from "@/components/forms/CVUploader";
import { JobDescriptionForm } from "@/components/forms/JobDescriptionForm";
import { LoadingAnalysis } from "@/components/results/LoadingAnalysis";
import { OverallScore } from "@/components/results/OverallScore";
import { ScoreCard } from "@/components/results/ScoreCard";
import { SkillsRadarChart } from "@/components/results/SkillsRadarChart";
import { GapAnalysis } from "@/components/results/GapAnalysis";
import { ReportView } from "@/components/results/ReportView";
import { Code, Briefcase, Users, Cpu, RotateCcw } from "lucide-react";
import { toast } from "sonner";
import { api, AnalysisResponse } from "@/lib/api";

const Index = () => {
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);

  const handleAnalyze = async () => {
    if (!cvFile || !jobDescription.trim()) {
      toast.error("Veuillez fournir un CV et une description de poste");
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const result = await api.analyze(cvFile, jobDescription);
      setAnalysisResult(result);
      toast.success("Analyse terminée avec succès");
    } catch (error) {
      console.error(error);
      toast.error("Une erreur est survenue lors de l'analyse. Vérifiez que le backend est lancé.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setCvFile(null);
    setJobDescription("");
    setAnalysisResult(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/20 flex flex-col">
      <Header />
      
      <main className="container mx-auto px-6 py-8 flex-1 pb-24">
        {!analysisResult && !isAnalyzing && (
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-foreground mb-4">
                Analysez vos Candidatures en QUELQUES SECONDES !
              </h2>
              <p className="text-lg text-muted-foreground">
                Notre IA analyse automatiquement les CV et calcule leur pertinence par rapport à vos offres d'emploi
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6 mb-8">
              <CVUploader onFileSelect={setCvFile} selectedFile={cvFile} />
              <JobDescriptionForm value={jobDescription} onChange={setJobDescription} />
            </div>

            <div className="flex justify-center">
              <Button
                size="lg"
                onClick={handleAnalyze}
                disabled={!cvFile || !jobDescription.trim()}
                className="px-8"
              >
                Lancer l'Analyse
              </Button>
            </div>
          </div>
        )}

        {isAnalyzing && <LoadingAnalysis />}

        {analysisResult && !isAnalyzing && (
          <div className="max-w-6xl mx-auto space-y-8">
            <div className="flex justify-end gap-3">
              <Button variant="outline" onClick={handleReset}>
                <RotateCcw className="w-4 h-4 mr-2" />
                Nouvelle Analyse
              </Button>
            </div>

            <OverallScore
              score={analysisResult.matching.overall_score}
              jobTitle={analysisResult.job_classification.job_title}
              recommendation={analysisResult.matching.recommendation}
            />

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              <ScoreCard
                title="Compétences Techniques"
                score={analysisResult.matching.details.skills_score}
                icon={<Code className="w-5 h-5 text-primary" />}
                delay={0.1}
              />
              <ScoreCard
                title="Expérience"
                score={analysisResult.matching.details.experience_score}
                icon={<Briefcase className="w-5 h-5 text-primary" />}
                delay={0.2}
              />
              <ScoreCard
                title="Soft Skills"
                score={analysisResult.matching.details.soft_skills_score}
                icon={<Users className="w-5 h-5 text-primary" />}
                delay={0.3}
              />
              <ScoreCard
                title="Technologies"
                score={analysisResult.matching.details.technologies_score}
                icon={<Cpu className="w-5 h-5 text-primary" />}
                delay={0.4}
              />
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
              <SkillsRadarChart data={analysisResult.matching.details} />
              <GapAnalysis
                matchedSkills={analysisResult.matching.matched_skills}
                missingSkills={analysisResult.matching.missing_skills}
              />
            </div>

            <ReportView report={analysisResult.report} />
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default Index;
