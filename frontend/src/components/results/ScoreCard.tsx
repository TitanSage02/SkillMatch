import { Card } from "@/components/ui/card";
import { motion } from "framer-motion";

interface ScoreCardProps {
  title: string;
  score: number;
  icon: React.ReactNode;
  delay?: number;
}

export const ScoreCard = ({ title, score, icon, delay = 0 }: ScoreCardProps) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-success";
    if (score >= 50) return "text-warning";
    return "text-destructive";
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return "bg-success-light border-success/20";
    if (score >= 50) return "bg-warning-light border-warning/20";
    return "bg-destructive-light border-destructive/20";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
    >
      <Card className="p-6 hover:shadow-lg transition-shadow">
        <div className="flex items-start justify-between mb-4">
          <div className={`p-2.5 rounded-lg ${getScoreBg(score)}`}>
            {icon}
          </div>
          <span className={`text-3xl font-bold ${getScoreColor(score)}`}>
            {score}
            <span className="text-lg text-muted-foreground">/100</span>
          </span>
        </div>
        <h4 className="text-sm font-medium text-muted-foreground">{title}</h4>
        <div className="mt-3 h-2 bg-muted rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${score}%` }}
            transition={{ delay: delay + 0.2, duration: 0.6 }}
            className={`h-full ${score >= 80 ? "bg-success" : score >= 50 ? "bg-warning" : "bg-destructive"}`}
          />
        </div>
      </Card>
    </motion.div>
  );
};
