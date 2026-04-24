import { useState, useCallback } from 'react';
import { generateProposal, downloadProposalPdf, triggerDownload } from '../services/api';

const INITIAL_FORM = {
  description: '',
  project_type: '',
  industry: '',
  timeline: '',
  budget: '',
  client_name: '',
  extra_requirements: '',
};

// Ordered steps shown in the loading screen — mirrors pipeline.py
const GENERATION_STEPS = [
  'Analysing project requirements…',
  'Drafting Purpose of Document…',
  'Outlining Key Deliverables…',
  'Writing Objectives…',
  'Defining Features & Functionality…',
  'Building Technical Approach…',
  'Selecting Technology Stack…',
  'Exploring Future Scope…',
  'Estimating Time & Budget…',
  'Assembling final proposal…',
];

export function useProposal() {
  const [form, setForm]               = useState(INITIAL_FORM);
  const [proposalText, setProposalText] = useState('');
  const [status, setStatus]           = useState('idle'); // idle | generating | done | error
  const [error, setError]             = useState('');
  const [stepIndex, setStepIndex]     = useState(0);
  const [pdfLoading, setPdfLoading]   = useState(false);

  const updateField = useCallback((field, value) => {
    setForm(f => ({ ...f, [field]: value }));
  }, []);

  const resetForm = useCallback(() => {
    setForm(INITIAL_FORM);
    setProposalText('');
    setStatus('idle');
    setError('');
    setStepIndex(0);
  }, []);

  const generate = useCallback(async () => {
    if (!form.description.trim()) {
      setError('Project description is required.');
      return;
    }

    setStatus('generating');
    setError('');
    setStepIndex(0);

    // Simulate step progress while the LLM generates
    const totalSteps = GENERATION_STEPS.length;
    let current = 0;
    const interval = setInterval(() => {
      current += 1;
      if (current < totalSteps - 1) {
        setStepIndex(current);
      }
    }, 3200); // ~32s total for 10 steps, rough average for 8 LLM calls

    try {
      const text = await generateProposal(form);
      clearInterval(interval);
      setStepIndex(totalSteps - 1);
      await new Promise(r => setTimeout(r, 600)); // show last step briefly
      setProposalText(text);
      setStatus('done');
    } catch (e) {
      clearInterval(interval);
      setError(e.message || 'Something went wrong. Please try again.');
      setStatus('error');
    }
  }, [form]);

  const downloadPdf = useCallback(async () => {
    if (!proposalText) return;
    setPdfLoading(true);
    try {
      const blob = await downloadProposalPdf(proposalText);
      const clientSlug = form.client_name
        ? form.client_name.replace(/\s+/g, '_').toLowerCase()
        : 'proposal';
      triggerDownload(blob, `${clientSlug}_proposal.pdf`);
    } catch (e) {
      setError(e.message || 'PDF download failed.');
    } finally {
      setPdfLoading(false);
    }
  }, [proposalText, form.client_name]);

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
