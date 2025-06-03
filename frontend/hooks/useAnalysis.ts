import { useState, useCallback } from 'react';
import { 
  analyzeResume, 
  analyzeBatchResumes as apiAnalyzeBatchResumes, 
  getBatchAnalysisStatus, 
  AnalysisResult, 
  BatchAnalysisResult 
} from '../services/api';
import toast from 'react-hot-toast';

interface UseAnalysisState {
  isLoading: boolean;
  results: AnalysisResult | null;
  batchResults: BatchAnalysisResult | null;
  error: string | null;
}

interface UseAnalysisActions {
  analyzeSingleResume: (file: File, jobDescription: string) => Promise<void>;
  analyzeBatchResumes: (files: File[], jobDescription: string) => Promise<void>;
  checkBatchStatus: (jobId: string) => Promise<void>;
  reset: () => void;
}

export const useAnalysis = (): UseAnalysisState & UseAnalysisActions => {
  const [state, setState] = useState<UseAnalysisState>({
    isLoading: false,
    results: null,
    batchResults: null,
    error: null,
  });

  const analyzeSingleResume = useCallback(async (file: File, jobDescription: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null, results: null }));
    
    try {
      const loadingToast = toast.loading('Analyzing resume...');
      const results = await analyzeResume(file, jobDescription);
      
      setState(prev => ({
        ...prev,
        isLoading: false,
        results,
      }));
      
      toast.dismiss(loadingToast);
      toast.success('Analysis completed successfully!');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An error occurred during analysis';
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      toast.error(errorMessage);
    }
  }, []);

  const analyzeBatchResumes = useCallback(async (files: File[], jobDescription: string) => {
    setState(prev => ({ ...prev, isLoading: true, error: null, batchResults: null }));
    
    try {
      const loadingToast = toast.loading(`Starting batch analysis for ${files.length} resumes...`);
      const { job_id } = await apiAnalyzeBatchResumes(files, jobDescription);
      
      const pollStatus = async () => {
        try {
          const batchResults = await getBatchStatus(job_id);
          setState(prev => ({ ...prev, batchResults }));
          
          if (batchResults.status === 'completed') {
            toast.dismiss(loadingToast);
            toast.success('Batch analysis completed!');
            setState(prev => ({ ...prev, isLoading: false }));
          } else if (batchResults.status === 'failed') {
            toast.dismiss(loadingToast);
            toast.error(batchResults.error || 'Batch analysis failed');
            setState(prev => ({ ...prev, isLoading: false, error: batchResults.error || 'Analysis failed' }));
          } else {
            setTimeout(pollStatus, 2000);
          }
        } catch (error) {
          toast.dismiss(loadingToast);
          const errorMessage = error instanceof Error ? error.message : 'Failed to check batch status';
          setState(prev => ({ ...prev, isLoading: false, error: errorMessage }));
          toast.error(errorMessage);
        }
      };
      
      pollStatus();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to start batch analysis';
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      toast.error(errorMessage);
    }
  }, []);

  const checkBatchStatus = useCallback(async (jobId: string) => {
    try {
      const batchResults = await getBatchAnalysisStatus(jobId);
      setState(prev => ({ ...prev, batchResults }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to check batch status';
      setState(prev => ({ ...prev, error: errorMessage }));
      toast.error(errorMessage);
    }
  }, []);

  const reset = useCallback(() => {
    setState({
      isLoading: false,
      results: null,
      batchResults: null,
      error: null,
    });
  }, []);

  return {
    ...state,
    analyzeSingleResume,
    analyzeBatchResumes,
    checkBatchStatus,
    reset,
  };
};

const getBatchStatus = getBatchAnalysisStatus;
