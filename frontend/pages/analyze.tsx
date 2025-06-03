import React, { useState } from 'react';
import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import FileUpload from '@/components/FileUpload';
import AnalysisResults from '@/components/AnalysisResults';
import { useAnalysis } from '@/hooks/useAnalysis';
import { ArrowRight, FileText, Briefcase, Zap, Users } from 'lucide-react';

interface AnalysisState {
  resume: File | null;
  jobDescription: string;
  mode: 'single' | 'batch';
  batchFiles: File[];
}

export default function Analyze() {
  const [state, setState] = useState<AnalysisState>({
    resume: null,
    jobDescription: '',
    mode: 'single',
    batchFiles: [],
  });

  const { 
    isLoading, 
    results, 
    batchResults, 
    error, 
    analyzeSingleResume, 
    analyzeBatchResumes, 
    reset 
  } = useAnalysis();

  const handleFileSelect = (file: File) => {
    if (state.mode === 'single') {
      setState(prev => ({ ...prev, resume: file }));
    } else {
      setState(prev => ({ 
        ...prev, 
        batchFiles: [...prev.batchFiles, file] 
      }));
    }
  };

  const handleRemoveBatchFile = (index: number) => {
    setState(prev => ({
      ...prev,
      batchFiles: prev.batchFiles.filter((_, i) => i !== index)
    }));
  };

  const handleAnalyze = async () => {
    if (!state.jobDescription.trim()) {
      toast.error('Please enter a job description');
      return;
    }

    if (state.mode === 'single') {
      if (!state.resume) {
        toast.error('Please upload a resume');
        return;
      }
      await analyzeSingleResume(state.resume, state.jobDescription);
    } else {
      if (state.batchFiles.length === 0) {
        toast.error('Please upload at least one resume for batch analysis');
        return;
      }
      await analyzeBatchResumes(state.batchFiles, state.jobDescription);
    }

    setTimeout(() => {
      const resultsElement = document.getElementById('results');
      if (resultsElement) {
        resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  };

  const resetAnalysis = () => {
    setState({
      resume: null,
      jobDescription: '',
      mode: 'single',
      batchFiles: [],
    });
    reset();
  };

  const toggleMode = (mode: 'single' | 'batch') => {
    setState(prev => ({
      ...prev,
      mode,
      resume: null,
      batchFiles: [],
    }));
    reset();
  };

  return (
    <>
      <Head>
        <title>Analyze Resume Match - ResuMatch</title>
        <meta 
          name="description" 
          content="Upload your resume and job description to get AI-powered compatibility analysis with detailed scoring and recommendations." 
        />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <Header />
        
        <main className="pt-20 md:pt-24 pb-12 md:pb-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-8 md:mb-12"
            >
              <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-3 md:mb-4">
                AI-Powered Resume
                <span className="gradient-text block">Analysis</span>
              </h1>
              <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto px-4">
                Upload your resume and job description to get instant compatibility analysis 
                with detailed scoring, skill matching, and personalized recommendations.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="mb-8 md:mb-12"
            >
              <div className="flex flex-col md:flex-row items-center justify-center space-y-4 md:space-y-0 md:space-x-6 lg:space-x-8">
                {[
                  { 
                    icon: FileText, 
                    label: 'Upload Resume', 
                    completed: state.mode === 'single' ? !!state.resume : state.batchFiles.length > 0 
                  },
                  { icon: Briefcase, label: 'Job Description', completed: !!state.jobDescription.trim() },
                  { icon: Zap, label: 'AI Analysis', completed: !!(results || batchResults) },
                ].map((step, index) => (
                  <div key={step.label} className="flex items-center">
                    <div className={`
                      w-10 h-10 md:w-12 md:h-12 rounded-xl flex items-center justify-center transition-all duration-300
                      ${step.completed 
                        ? 'bg-primary-600 text-white scale-110' 
                        : 'bg-gray-200 text-gray-600'
                      }
                    `}>
                      <step.icon className="w-5 h-5 md:w-6 md:h-6" />
                    </div>
                    <span className={`
                      ml-2 md:ml-3 font-medium transition-colors duration-300 text-sm md:text-base
                      ${step.completed ? 'text-primary-600' : 'text-gray-600'}
                    `}>
                      {step.label}
                    </span>
                    {index < 2 && (
                      <ArrowRight className="hidden md:block w-5 h-5 text-gray-400 ml-6 lg:ml-8" />
                    )}
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.25 }}
              className="mb-6 md:mb-8"
            >
              <div className="flex justify-center">
                <div className="bg-white p-1 rounded-xl shadow-sm border">
                  <button
                    onClick={() => toggleMode('single')}
                    className={`
                      px-4 md:px-6 py-2 md:py-3 rounded-lg font-medium transition-all duration-200 text-sm md:text-base
                      ${state.mode === 'single'
                        ? 'bg-primary-600 text-white shadow-md'
                        : 'text-gray-600 hover:text-gray-900'
                      }
                    `}
                  >
                    <FileText className="w-4 h-4 md:w-5 md:h-5 inline mr-2" />
                    Single Resume
                  </button>
                  <button
                    onClick={() => toggleMode('batch')}
                    className={`
                      px-4 md:px-6 py-2 md:py-3 rounded-lg font-medium transition-all duration-200 text-sm md:text-base
                      ${state.mode === 'batch'
                        ? 'bg-primary-600 text-white shadow-md'
                        : 'text-gray-600 hover:text-gray-900'
                      }
                    `}
                  >
                    <Users className="w-4 h-4 md:w-5 md:h-5 inline mr-2" />
                    Batch Analysis
                  </button>
                </div>
              </div>
            </motion.div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8 mb-8 md:mb-12 min-h-[400px] md:min-h-[450px]">
              <motion.div
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <h2 className="text-xl md:text-2xl font-semibold text-gray-900 mb-3 md:mb-4">
                  {state.mode === 'single' ? 'Upload Resume' : 'Upload Resumes (Batch)'}
                </h2>
                
                {state.mode === 'single' ? (
                  <FileUpload
                    onFileSelect={handleFileSelect}
                    acceptedTypes={[
                      'application/pdf',
                      'application/msword',
                      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                      'text/plain',
                      'image/jpeg',
                      'image/png',
                    ]}
                    maxSize={10 * 1024 * 1024} // 10MB
                    title="Drop your resume here"
                    description="Drag & drop your resume or click to browse"
                  />
                ) : (
                  <div>
                    <FileUpload
                      onFileSelect={handleFileSelect}
                      acceptedTypes={[
                        'application/pdf',
                        'application/msword',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'text/plain',
                        'image/jpeg',
                        'image/png',
                      ]}
                      maxSize={10 * 1024 * 1024} // 10MB
                      title="Drop resumes here"
                      description="Add multiple resumes for batch analysis"
                    />
                    
                    {state.batchFiles.length > 0 && (
                      <div className="mt-4 space-y-2">
                        <h3 className="font-medium text-gray-900">
                          Selected Files ({state.batchFiles.length})
                        </h3>
                        <div className="max-h-32 overflow-y-auto space-y-1">
                          {state.batchFiles.map((file, index) => (
                            <div
                              key={index}
                              className="flex items-center justify-between bg-gray-50 p-2 rounded"
                            >
                              <span className="text-sm text-gray-700 truncate">
                                {file.name}
                              </span>
                              <button
                                onClick={() => handleRemoveBatchFile(index)}
                                className="text-red-500 hover:text-red-700 text-sm"
                              >
                                Remove
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                className="flex flex-col"
              >
                <h2 className="text-xl md:text-2xl font-semibold text-gray-900 mb-3 md:mb-4">Job Description</h2>
                <div className="card p-4 md:p-6 flex-1">
                  <textarea
                    value={state.jobDescription}
                    onChange={(e) => setState(prev => ({ ...prev, jobDescription: e.target.value }))}
                    placeholder="Paste the job description here..."
                    rows={10}
                    className="w-full h-64 md:h-80 resize-none border-0 focus:ring-0 focus:outline-none text-gray-900 placeholder-gray-500"
                  />
                  <div className="mt-3 md:mt-4 flex justify-between items-center text-sm text-gray-500">
                    <span>{state.jobDescription.length} characters</span>
                    <span>Minimum 100 characters recommended</span>
                  </div>
                </div>
              </motion.div>
            </div>

            <div className="h-4 md:h-6"></div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="flex flex-col items-center justify-center mb-8 md:mb-12 mt-6 md:mt-8 pt-4 md:pt-6"
            >
              <motion.button
                onClick={handleAnalyze}
                disabled={
                  isLoading || 
                  !state.jobDescription.trim() || 
                  (state.mode === 'single' ? !state.resume : state.batchFiles.length === 0)
                }
                whileHover={{ scale: isLoading ? 1 : 1.05 }}
                whileTap={{ scale: isLoading ? 1 : 0.95 }}
                className={`
                  inline-flex items-center justify-center px-8 md:px-12 py-3 md:py-4 text-base md:text-lg font-medium rounded-xl md:rounded-2xl shadow-lg transition-all duration-300 min-w-[200px] md:min-w-[250px]
                  ${isLoading || 
                    !state.jobDescription.trim() || 
                    (state.mode === 'single' ? !state.resume : state.batchFiles.length === 0)
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-primary-600 to-purple-600 text-white hover:from-primary-700 hover:to-purple-700 hover:shadow-xl'
                  }
                `}
              >
                {isLoading ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      className="w-6 h-6 border-2 border-white border-t-transparent rounded-full mr-3"
                    />
                    {state.mode === 'single' ? 'Analyzing...' : 'Processing Batch...'}
                  </>
                ) : (
                  <>
                    <Zap className="w-6 h-6 mr-3" />
                    {state.mode === 'single' ? 'Analyze Match' : `Analyze ${state.batchFiles.length} Resumes`}
                  </>
                )}
              </motion.button>
              
              {(results || batchResults) && (
                <motion.button
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.3 }}
                  onClick={resetAnalysis}
                  className="mt-3 md:mt-4 btn-secondary px-6 md:px-8 py-2 md:py-3 text-sm md:text-base"
                >
                  New Analysis
                </motion.button>
              )}
            </motion.div>

            <AnimatePresence>
              {(results || batchResults) && (
                <motion.div
                  id="results"
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -50 }}
                  transition={{ duration: 0.8, ease: 'easeOut' }}
                >
                  {results && <AnalysisResults result={results} />}
                  {batchResults && (
                    <div className="space-y-6">
                      <h2 className="text-2xl font-bold text-gray-900">
                        Batch Analysis Results
                      </h2>
                      <div className="bg-white p-6 rounded-lg shadow-sm">
                        <div className="flex items-center justify-between mb-4">
                          <span className="text-lg font-medium">Status: {batchResults.status}</span>
                          <span className="text-sm text-gray-500">
                            Job ID: {batchResults.job_id}
                          </span>
                        </div>
                        {batchResults.results && (
                          <div className="space-y-4">
                            {batchResults.results.map((result, index) => (
                              <div key={index} className="border-t pt-4">
                                <h3 className="font-medium mb-2">Resume {index + 1}</h3>
                                <AnalysisResults result={result} />
                              </div>
                            ))}
                          </div>
                        )}
                        {batchResults.error && (
                          <div className="text-red-600 p-4 bg-red-50 rounded-lg">
                            Error: {batchResults.error}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
