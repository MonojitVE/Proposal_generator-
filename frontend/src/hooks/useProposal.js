import { useState, useCallback } from "react";
import { generateProposal, triggerDownload } from "../services/api";
import { generateProposalPdf } from "../services/pdfGenerator";

const INITIAL_FORM = {
  project_name: "",
  description: "",
  project_type: "",
  industry: "",
  timeline: "",
  budget: "",
  phases: "",
  resources: "",
  client_name: "",
  extra_requirements: "",
};

const GENERATION_STEPS = [
  "Analysing project requirements…",
  "Drafting Purpose of Document…",
  "Outlining Key Deliverables…",
  "Writing Objectives…",
  "Defining Features & Functionality…",
  "Building Technical Approach…",
  "Selecting Technology Stack…",
  "Exploring Future Scope…",
  "Estimating Time & Budget…",
  "Assembling final proposal…",
];

export function useProposal() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [proposalText, setProposalText] = useState("");
  const [status, setStatus] = useState("idle");
  const [error, setError] = useState("");
  const [stepIndex, setStepIndex] = useState(0);
  const [pdfLoading, setPdfLoading] = useState(false);

  // ← Snapshot of form saved at generation time, survives page transitions
  const [savedMeta, setSavedMeta] = useState({ project_name: "", client_name: "" });

  const updateField = useCallback((field, value) => {
    setForm((f) => ({ ...f, [field]: value }));
  }, []);

  const resetForm = useCallback(() => {
    setForm(INITIAL_FORM);
    setProposalText("");
    setStatus("idle");
    setError("");
    setStepIndex(0);
    setSavedMeta({ project_name: "", client_name: "" });
  }, []);

  const generate = useCallback(async () => {
    if (!form.description.trim()) {
      setError("Project description is required.");
      return;
    }
    setStatus("generating");
    setError("");
    setStepIndex(0);

    // ← Save project_name and client_name NOW before any navigation/reset
    setSavedMeta({
      project_name: form.project_name.trim(),
      client_name: form.client_name.trim(),
    });

    const totalSteps = GENERATION_STEPS.length;
    let current = 0;
    const interval = setInterval(() => {
      current += 1;
      if (current < totalSteps - 1) setStepIndex(current);
    }, 3200);

    try {
      const text = await generateProposal(form);
      clearInterval(interval);
      if (!text || typeof text !== "string") throw new Error("Invalid response from proposal generator");
      setStepIndex(totalSteps - 1);
      await new Promise((r) => setTimeout(r, 600));
      setProposalText(text);
      setStatus("done");
    } catch (e) {
      clearInterval(interval);
      console.error("GENERATION ERROR:", e);
      setError(e?.response?.data?.message || e.message || "Something went wrong. Please try again.");
      setStatus("error");
    }
  }, [form]);

  const downloadPdf = useCallback(async () => {
    if (pdfLoading) return;
    if (!proposalText) { setError("No proposal available to download."); return; }
    setPdfLoading(true);
    setError("");

    try {
      const blob = await generateProposalPdf(proposalText, {
        projectTitle: savedMeta.project_name,   // ← uses saved snapshot, never empty
        preparedBy: "Virtual Employee Pvt. Ltd.",
        clientName: savedMeta.client_name || "",
        date: "",
      });

      if (!blob || !(blob instanceof Blob)) throw new Error("Invalid PDF response");

      const clientSlug = savedMeta.client_name
        ? savedMeta.client_name.replace(/\s+/g, "_").toLowerCase()
        : "proposal";
      triggerDownload(blob, `${clientSlug}_proposal.pdf`);
    } catch (e) {
      console.error("PDF ERROR:", e);
      setError(e?.response?.data?.message || e.message || "PDF download failed. Please try again.");
    } finally {
      setPdfLoading(false);
    }
  }, [proposalText, savedMeta, pdfLoading]);

  return {
    form, updateField, resetForm,
    proposalText, setProposalText,
    status, error, stepIndex,
    steps: GENERATION_STEPS,
    generate, downloadPdf, pdfLoading,
  };
}