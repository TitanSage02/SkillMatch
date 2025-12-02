import { Github } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="border-t border-border bg-background/80 backdrop-blur-sm fixed bottom-0 left-0 right-0 z-50">
      <div className="container mx-auto px-6 py-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} SkillMatch. Tous droits réservés.
          </p>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <span>Réalisé par</span>
              <a
                href="https://github.com/TitanSage02"
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium text-foreground hover:text-primary transition-colors"
              >
                Espérance AYIWAHOUN
              </a>
            </div>
            <div className="h-4 w-px bg-border" />
            <a
              href="https://github.com/TitanSage02/SkillMatch"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 font-medium text-foreground hover:text-primary transition-colors"
            >
              <Github className="w-4 h-4" />
              <span>Code Source</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
