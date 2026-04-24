import { useState, useCallback } from "react";
import {
  generateProposal,
  downloadProposalPdf,
  triggerDownload,
} from "../services/api";

const INITIAL_FORM = {
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

// Ordered steps shown in the loading screen
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
  const [status, setStatus] = useState("idle"); // idle | generating | done | error
  const [error, setError] = useState("");
  const [stepIndex, setStepIndex] = useState(0);
  const [pdfLoading, setPdfLoading] = useState(false);

  const updateField = useCallback((field, value) => {
    setForm((f) => ({ ...f, [field]: value }));
  }, []);

  const resetForm = useCallback(() => {
    setForm(INITIAL_FORM);
    setProposalText("");
    setStatus("idle");
    setError("");
    setStepIndex(0);
  }, []);

  const generate = useCallback(async () => {
    if (!form.description.trim()) {
      setError("Project description is required.");
      return;
    }

    setStatus("generating");
    setError("");
    setStepIndex(0);

    const totalSteps = GENERATION_STEPS.length;
    let current = 0;

    const interval = setInterval(() => {
      current += 1;
      if (current < totalSteps - 1) {
        setStepIndex(current);
      }
    }, 3200);

    try {
      const text = await generateProposal(form);

      clearInterval(interval);

      if (!text || typeof text !== "string") {
        throw new Error("Invalid response from proposal generator");
      }

      setStepIndex(totalSteps - 1);
      await new Promise((r) => setTimeout(r, 600));

      setProposalText(text);
      setStatus("done");
    } catch (e) {
      clearInterval(interval);

      console.error("GENERATION ERROR:", e);

      setError(
        e?.response?.data?.message ||
          e.message ||
          "Something went wrong. Please try again.",
      );
      setStatus("error");
    }
  }, [form]);

  const downloadPdf = useCallback(async () => {
    if (pdfLoading) return;

    if (!proposalText) {
      setError("No proposal available to download.");
      return;
    }

    setPdfLoading(true);
    setError("");

    try {
      const blob = await downloadProposalPdf(proposalText);

      if (!blob || !(blob instanceof Blob)) {
        throw new Error("Invalid PDF response from server");
      }

      const clientSlug = form.client_name
        ? form.client_name.replace(/\s+/g, "_").toLowerCase()
        : "proposal";

      triggerDownload(blob, `${clientSlug}_proposal.pdf`);
    } catch (e) {
      console.error("PDF ERROR:", e);

      setError(
        e?.response?.data?.message ||
          e.message ||
          "PDF download failed. Please try again.",
      );
    } finally {
      setPdfLoading(false);
    }
  }, [proposalText, form.client_name, pdfLoading]);

  return {
    form,
    updateField,
    resetForm,
    proposalText,
    setProposalText,
    status,
    error,
    stepIndex,
    steps: GENERATION_STEPS,
    generate,
    downloadPdf,
    pdfLoading,
  };
}
