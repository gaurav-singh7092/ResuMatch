import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 429) {
      throw new Error('Too many requests. Please try again later.');
    }
    if (error.response?.status === 500) {
      throw new Error('Server error. Please try again later.');
    }
    if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. Please try again.');
    }
    return Promise.reject(error);
  }
);

export interface AnalysisRequest {
  job_description: string;
}

export interface AnalysisResult {
  overall_score: number;
  component_scores: {
    semantic_similarity: number;
    skill_match: number;
    experience_match: number;
    education_match: number;
    keyword_match: number;
  };
  matched_skills: string[];
  missing_skills: string[];
  recommendations: string[];
  detailed_analysis: {
    overall_assessment: string;
    strengths: string[];
    areas_for_improvement: string[];
  };
}

export interface BatchAnalysisResult {
  job_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  results?: AnalysisResult[];
  error?: string;
  created_at: string;
  completed_at?: string;
}

export const analyzeResume = async (
  resumeFile: File,
  jobDescription: string
): Promise<AnalysisResult> => {
  const formData = new FormData();
  formData.append('resume', resumeFile);
  formData.append('job_description', jobDescription);

  const response = await api.post('/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  const { similarity_analysis } = response.data;
  return similarity_analysis;
};

export const analyzeBatchResumes = async (
  resumeFiles: File[],
  jobDescription: string
): Promise<{ job_id: string }> => {
  const formData = new FormData();
  resumeFiles.forEach((file, index) => {
    formData.append(`resumes`, file);
  });
  formData.append('job_description', jobDescription);

  const response = await api.post('/analyze/batch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const getBatchAnalysisStatus = async (
  jobId: string
): Promise<BatchAnalysisResult> => {
  const response = await api.get(`/analyze/batch/${jobId}`);
  return response.data;
};

export const healthCheck = async (): Promise<{ status: string; message: string }> => {
  const response = await api.get('/health');
  return response.data;
};

export const getSupportedFileTypes = async (): Promise<{ supported_types: string[] }> => {
  const response = await api.get('/supported-types');
  return response.data;
};

export default api;
