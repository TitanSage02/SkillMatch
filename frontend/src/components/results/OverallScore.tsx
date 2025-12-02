import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";
import { TrendingUp, CheckCircle, AlertTriangle, XCircle } from "lucide-react";

interface OverallScoreProps {
  score: number;
  jobTitle: string;
  recommendation: "strongly_recommended" | "recommended" | "not_recommended";
}

export const OverallScore = ({ score, jobTitle, recommendation }: OverallScoreProps) => {
  const getRecommendationConfig = () => {
    switch (recommendation) {
      case "strongly_recommended":
        return {
          icon: <CheckCircle className="w-5 h-5" />,
          text: "Fortement Recommandé",
          variant: "default" as const,
          bgClass: "bg-success-light border-success/20",
          textClass: "text-success",
        };
      case "recommended":
        return {
          icon: <AlertTriangle className="w-5 h-5" />,
          text: "À Considérer",
          variant: "secondary" as const,
          bgClass: "bg-warning-light border-warning/20",
          textClass: "text-warning",
        };
      default:
        return {
          icon: <XCircle className="w-5 h-5" />,
          text: "Non Recommandé",
          variant: "destructive" as const,
          bgClass: "bg-destructive-light border-destructive/20",
          textClass: "text-destructive",
        };
    }
  };

  const config = getRecommendationConfig();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <Card className="p-8 bg-gradient-to-br from-primary/5 via-background to-background border-primary/20">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex-1 text-center md:text-left">
            <div className="flex items-center gap-2 mb-2 justify-center md:justify-start">
              <TrendingUp className="w-5 h-5 text-primary" />
              <span className="text-sm font-medium text-muted-foreground">Poste Identifié</span>
            </div>
            <h2 className="text-3xl font-bold text-foreground mb-4">{jobTitle}</h2>
            <Badge variant={config.variant} className="text-sm px-3 py-1">
              {config.icon}
              <span className="ml-2">{config.text}</span>
            </Badge>
          </div>

          <div className="flex flex-col items-center">
            <div className="relative w-32 h-32">
              <svg className="w-full h-full transform -rotate-90">
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="hsl(var(--muted))"
                  strokeWidth="8"
                  fill="none"
                />
                <motion.circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="hsl(var(--primary))"
                  strokeWidth="8"
                  fill="none"
                  strokeLinecap="round"
                  initial={{ strokeDasharray: "0 352" }}
                  animate={{ strokeDasharray: `${(score / 100) * 352} 352` }}
                  transition={{ duration: 1, ease: "easeOut" }}
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold text-foreground">{score}</span>
                <span className="text-sm text-muted-foreground">/ 100</span>
              </div>
            </div>
            <p className="text-sm text-muted-foreground mt-3">Score Global</p>
          </div>
        </div>
      </Card>
    </motion.div>
  );
};
