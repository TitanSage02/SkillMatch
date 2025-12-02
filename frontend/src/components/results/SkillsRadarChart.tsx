import { Card } from "@/components/ui/card";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from "recharts";

interface SkillsRadarChartProps {
  data: {
    skills_score: number;
    experience_score: number;
    soft_skills_score: number;
    technologies_score: number;
  };
}

export const SkillsRadarChart = ({ data }: SkillsRadarChartProps) => {
  const chartData = [
    { category: "Compétences", value: data.skills_score },
    { category: "Expérience", value: data.experience_score },
    { category: "Soft Skills", value: data.soft_skills_score },
    { category: "Technologies", value: data.technologies_score },
  ];

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-6 text-foreground">Analyse Comparative</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart data={chartData}>
          <PolarGrid stroke="hsl(var(--border))" />
          <PolarAngleAxis 
            dataKey="category" 
            tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tick={{ fill: "hsl(var(--muted-foreground))" }}
          />
          <Radar
            name="Score"
            dataKey="value"
            stroke="hsl(var(--primary))"
            fill="hsl(var(--primary))"
            fillOpacity={0.3}
          />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </Card>
  );
};
