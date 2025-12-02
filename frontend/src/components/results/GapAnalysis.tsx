import { Card } from "@/components/ui/card";
import { CheckCircle2, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";

interface GapAnalysisProps {
  matchedSkills: string[];
  missingSkills: string[];
}

export const GapAnalysis = ({ matchedSkills, missingSkills }: GapAnalysisProps) => {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-6 text-foreground">Analyse des Écarts</h3>
      
      <div className="space-y-6">
        {/* Matched Skills */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle2 className="w-5 h-5 text-success" />
            <h4 className="font-medium text-foreground">Compétences Validées</h4>
            <span className="text-sm text-muted-foreground">({matchedSkills.length})</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {matchedSkills.map((skill, index) => (
              <motion.span
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.05 }}
                className="px-3 py-1.5 bg-success-light border border-success/20 text-success text-sm rounded-lg"
              >
                {skill}
              </motion.span>
            ))}
          </div>
        </div>

        {/* Missing Skills */}
        {missingSkills.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <AlertCircle className="w-5 h-5 text-destructive" />
              <h4 className="font-medium text-foreground">Compétences Manquantes</h4>
              <span className="text-sm text-muted-foreground">({missingSkills.length})</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {missingSkills.map((skill, index) => (
                <motion.span
                  key={index}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.05 }}
                  className="px-3 py-1.5 bg-destructive-light border border-destructive/20 text-destructive text-sm rounded-lg"
                >
                  {skill}
                </motion.span>
              ))}
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};
