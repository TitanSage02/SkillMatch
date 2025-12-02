import { useRef } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Copy, FileText, Download } from "lucide-react";
import { toast } from "sonner";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";

interface ReportViewProps {
  report: string;
}

export const ReportView = ({ report }: ReportViewProps) => {
  const reportRef = useRef<HTMLDivElement>(null);

  const handleCopy = () => {
    navigator.clipboard.writeText(report);
    toast.success("Rapport copié dans le presse-papiers");
  };

  const handleDownloadPDF = async () => {
    if (!reportRef.current) return;

    toast.info("Génération du PDF en cours...");

    try {
      const canvas = await html2canvas(reportRef.current, {
        scale: 2,
        useCORS: true,
        backgroundColor: "#ffffff",
      });

      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("p", "mm", "a4");

      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = pdfWidth - 20;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;

      let heightLeft = imgHeight;
      let position = 10;

      // First page
      pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
      heightLeft -= pdfHeight - 20;

      // Additional pages if needed
      while (heightLeft > 0) {
        position = heightLeft - imgHeight + 10;
        pdf.addPage();
        pdf.addImage(imgData, "PNG", 10, position, imgWidth, imgHeight);
        heightLeft -= pdfHeight - 20;
      }

      pdf.save("rapport-analyse-hr.pdf");
      toast.success("Rapport téléchargé en PDF");
    } catch (error) {
      console.error("PDF generation error:", error);
      toast.error("Erreur lors de la génération du PDF");
    }
  };

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">Rapport Détaillé</h3>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleDownloadPDF}>
            <Download className="w-4 h-4 mr-2" />
            PDF
          </Button>
          <Button variant="outline" size="sm" onClick={handleCopy}>
            <Copy className="w-4 h-4 mr-2" />
            Copier
          </Button>
        </div>
      </div>

      <div 
        ref={reportRef} 
        className="report-content bg-white dark:bg-card rounded-lg p-6 border border-border w-full"
      >
        <ReactMarkdown 
          remarkPlugins={[remarkGfm]}
          components={{
            h1: ({node, ...props}) => <h1 className="text-2xl font-bold mb-4 mt-6 text-primary" {...props} />,
            h2: ({node, ...props}) => <h2 className="text-xl font-semibold mb-3 mt-5 text-foreground border-b pb-2" {...props} />,
            h3: ({node, ...props}) => <h3 className="text-lg font-medium mb-2 mt-4 text-foreground" {...props} />,
            p: ({node, ...props}) => <p className="mb-4 text-base leading-7 text-muted-foreground text-left break-words whitespace-pre-wrap" {...props} />,
            ul: ({node, ...props}) => <ul className="list-disc pl-5 mb-4 space-y-1 text-left" {...props} />,
            li: ({node, ...props}) => (
              <li className="text-muted-foreground pl-1 marker:text-primary">
                <span className="block">{props.children}</span>
              </li>
            ),
            strong: ({node, ...props}) => <strong className="font-semibold text-foreground" {...props} />,
            blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-primary/50 pl-4 italic my-4 text-muted-foreground" {...props} />,
          }}
        >
          {report}
        </ReactMarkdown>
      </div>
    </Card>
  );
};
