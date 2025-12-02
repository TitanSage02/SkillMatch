import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { FileText, X } from "lucide-react";
import { useRef } from "react";
import { toast } from "sonner";

interface JobDescriptionFormProps {
  value: string;
  onChange: (value: string) => void;
}

export const JobDescriptionForm = ({ value, onChange }: JobDescriptionFormProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type !== "text/plain") {
      toast.error("Veuillez sélectionner un fichier .txt");
      return;
    }

    try {
      const text = await file.text();
      onChange(text);
      toast.success("Fichier chargé avec succès");
    } catch (error) {
      toast.error("Erreur lors de la lecture du fichier");
    }
  };

  const handleClear = () => {
    onChange("");
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-foreground">Description du Poste</h3>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => fileInputRef.current?.click()}
            className="gap-2"
          >
            <FileText className="w-4 h-4" />
            Importer .txt
          </Button>
          {value && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleClear}
              className="gap-2"
            >
              <X className="w-4 h-4" />
            </Button>
          )}
        </div>
      </div>
      <input
        ref={fileInputRef}
        type="file"
        accept=".txt"
        onChange={handleFileSelect}
        className="hidden"
      />
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Collez ici la description complète de l'offre d'emploi ou importez un fichier .txt..."
        className="min-h-[240px] resize-none text-foreground"
      />
      <p className="text-xs text-muted-foreground mt-3">
        Plus la description est détaillée, plus l'analyse sera précise.
      </p>
    </Card>
  );
};
