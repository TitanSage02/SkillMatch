import { useState, useCallback } from "react";
import { Upload, File, X } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface CVUploaderProps {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
}

export const CVUploader = ({ onFileSelect, selectedFile }: CVUploaderProps) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);

      const files = Array.from(e.dataTransfer.files);
      const validFile = files.find((file) =>
        ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"].includes(file.type)
      );

      if (validFile && validFile.size <= 5 * 1024 * 1024) {
        onFileSelect(validFile);
      }
    },
    [onFileSelect]
  );

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4 text-foreground">CV du Candidat</h3>
      
      {!selectedFile ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            border-2 border-dashed rounded-xl p-8 text-center transition-all
            ${isDragging 
              ? "border-primary bg-primary/5 scale-[1.02]" 
              : "border-border hover:border-primary/50 hover:bg-muted/30"
            }
          `}
        >
          <div className="flex flex-col items-center gap-4">
            <div className="bg-primary/10 rounded-full p-4">
              <Upload className="w-8 h-8 text-primary" />
            </div>
            <div>
              <p className="text-foreground font-medium mb-1">
                Glissez-déposez votre CV ici
              </p>
              <p className="text-sm text-muted-foreground">
                ou cliquez pour sélectionner un fichier
              </p>
            </div>
            <label htmlFor="cv-upload">
              <Button type="button" variant="outline" size="sm" asChild>
                <span className="cursor-pointer">Choisir un fichier</span>
              </Button>
            </label>
            <input
              id="cv-upload"
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileInput}
              className="hidden"
            />
            <p className="text-xs text-muted-foreground">
              PDF, DOCX ou TXT • Max 5MB
            </p>
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-between bg-success-light border border-success/20 rounded-xl p-4">
          <div className="flex items-center gap-3">
            <div className="bg-success/10 rounded-lg p-2">
              <File className="w-5 h-5 text-success" />
            </div>
            <div>
              <p className="text-sm font-medium text-foreground">{selectedFile.name}</p>
              <p className="text-xs text-muted-foreground">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
          </div>
          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => onFileSelect(null)}
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      )}
    </Card>
  );
};
