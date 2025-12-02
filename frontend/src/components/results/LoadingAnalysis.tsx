import { motion } from "framer-motion";
import { Loader2, FileSearch, Brain, ChartBar } from "lucide-react";
import { Card } from "@/components/ui/card";
import { useEffect, useState } from "react";

const steps = [
  { icon: FileSearch, text: "Lecture du CV...", delay: 0 },
  { icon: Brain, text: "Analyse sémantique en cours...", delay: 3000 },
  { icon: ChartBar, text: "Calcul du matching...", delay: 6000 },
];

export const LoadingAnalysis = () => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const timers = steps.map((step, index) => 
      setTimeout(() => setCurrentStep(index), step.delay)
    );
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex items-center justify-center min-h-[400px]"
    >
      <Card className="p-8 max-w-md w-full">
        <div className="flex flex-col items-center gap-6">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          >
            <Loader2 className="w-16 h-16 text-primary" />
          </motion.div>

          <div className="space-y-4 w-full">
            {steps.map((step, index) => {
              const Icon = step.icon;
              const isActive = index === currentStep;
              const isCompleted = index < currentStep;

              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ 
                    opacity: isActive || isCompleted ? 1 : 0.4,
                    x: 0 
                  }}
                  className="flex items-center gap-3"
                >
                  <div className={`
                    p-2 rounded-lg transition-colors
                    ${isActive ? "bg-primary/10" : isCompleted ? "bg-success/10" : "bg-muted"}
                  `}>
                    <Icon className={`
                      w-5 h-5
                      ${isActive ? "text-primary" : isCompleted ? "text-success" : "text-muted-foreground"}
                    `} />
                  </div>
                  <p className={`
                    text-sm font-medium transition-colors
                    ${isActive ? "text-foreground" : "text-muted-foreground"}
                  `}>
                    {step.text}
                  </p>
                </motion.div>
              );
            })}
          </div>

          <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
            <motion.div
              initial={{ width: "0%" }}
              animate={{ width: "100%" }}
              transition={{ duration: 9, ease: "linear" }}
              className="h-full bg-primary"
            />
          </div>

          <p className="text-sm text-muted-foreground text-center">
            L'analyse peut prendre jusqu'à 20 secondes. <br/>
            <span className="text-xs opacity-75">
              Note : Une latence &gt; 20s peut survenir lors du premier appel (démarrage serveur) ou si le CV chargé est très volumineux (limite API Mistral).
            </span>
          </p>
        </div>
      </Card>
    </motion.div>
  );
};
