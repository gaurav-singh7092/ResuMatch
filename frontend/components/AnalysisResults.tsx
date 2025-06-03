import React from 'react';
import { motion } from 'framer-motion';
import { 
  CheckCircle, 
  XCircle, 
  TrendingUp, 
  User, 
  GraduationCap, 
  Briefcase, 
  Code,
  Target,
  Lightbulb
} from 'lucide-react';

interface AnalysisResult {
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

interface AnalysisResultsProps {
  result: AnalysisResult;
  className?: string;
}

const componentIcons = {
  semantic_similarity: TrendingUp,
  skill_match: Code,
  experience_match: Briefcase,
  education_match: GraduationCap,
  keyword_match: Target,
};

const componentNames = {
  semantic_similarity: 'Semantic Match',
  skill_match: 'Skills Match',
  experience_match: 'Experience Match',
  education_match: 'Education Match',
  keyword_match: 'Keywords Match',
};

export default function AnalysisResults({ result, className = '' }: AnalysisResultsProps) {
  const getScoreColor = (score: number) => {
    if (score >= 75) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreColorRing = (score: number) => {
    if (score >= 75) return 'stroke-green-500';
    if (score >= 60) return 'stroke-yellow-500';
    return 'stroke-red-500';
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: 'easeOut',
      },
    },
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className={`w-full space-y-8 ${className}`}
    >
      <motion.div variants={itemVariants} className="card p-8 text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Match Analysis Results</h2>
        
        <div className="relative inline-flex items-center justify-center">
          <svg className="w-32 h-32 transform -rotate-90">
            <circle
              cx="64"
              cy="64"
              r="56"
              stroke="currentColor"
              strokeWidth="8"
              fill="none"
              className="text-gray-200"
            />
            <circle
              cx="64"
              cy="64"
              r="56"
              stroke="currentColor"
              strokeWidth="8"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={`${2 * Math.PI * 56}`}
              strokeDashoffset={`${2 * Math.PI * 56 * (1 - (result.overall_score || 0) / 100)}`}
              className={getScoreColorRing(result.overall_score || 0)}
              style={{
                transition: 'stroke-dashoffset 1s ease-in-out',
              }}
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className={`text-3xl font-bold ${getScoreColor(result.overall_score || 0).split(' ')[0]}`}>
                {(result.overall_score || 0).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600">Overall Match</div>
            </div>
          </div>
        </div>
        
        <p className="text-lg text-gray-600 mt-6">{result.detailed_analysis?.overall_assessment || 'No assessment available'}</p>
      </motion.div>

      <motion.div variants={itemVariants} className="card p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">Detailed Analysis</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(result.component_scores || {}).map(([key, score]) => {
            const Icon = componentIcons[key as keyof typeof componentIcons];
            const name = componentNames[key as keyof typeof componentNames];
            const percentage = Math.round((score || 0) * 100);
            
            return (
              <motion.div
                key={key}
                variants={itemVariants}
                className="bg-gray-50 rounded-xl p-4 hover:bg-gray-100 transition-colors duration-200"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${getScoreColor(percentage)}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="font-medium text-gray-900">{name}</span>
                  </div>
                  <span className={`text-lg font-bold ${getScoreColor(percentage).split(' ')[0]}`}>
                    {percentage}%
                  </span>
                </div>
                
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${percentage}%` }}
                    transition={{ duration: 1, delay: 0.5 }}
                    className={`h-2 rounded-full ${
                      percentage >= 75 ? 'bg-green-500' : 
                      percentage >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                  />
                </div>
              </motion.div>
            );
          })}
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <motion.div variants={itemVariants} className="card p-6">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">
              Matched Skills ({(result.matched_skills || []).length})
            </h3>
          </div>
          
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {(result.matched_skills || []).slice(0, 20).map((skill, index) => (
              <motion.div
                key={skill}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-center space-x-3 py-2 px-3 bg-green-50 rounded-lg"
              >
                <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0" />
                <span className="text-gray-900">{skill}</span>
              </motion.div>
            ))}
            {(result.matched_skills || []).length > 20 && (
              <p className="text-sm text-gray-500 text-center py-2">
                +{(result.matched_skills || []).length - 20} more skills
              </p>
            )}
          </div>
        </motion.div>

        <motion.div variants={itemVariants} className="card p-6">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <XCircle className="w-6 h-6 text-red-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">
              Missing Skills ({(result.missing_skills || []).length})
            </h3>
          </div>
          
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {(result.missing_skills || []).slice(0, 20).map((skill, index) => (
              <motion.div
                key={skill}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-center space-x-3 py-2 px-3 bg-red-50 rounded-lg"
              >
                <XCircle className="w-4 h-4 text-red-600 flex-shrink-0" />
                <span className="text-gray-900">{skill}</span>
              </motion.div>
            ))}
            {(result.missing_skills || []).length > 20 && (
              <p className="text-sm text-gray-500 text-center py-2">
                +{(result.missing_skills || []).length - 20} more skills
              </p>
            )}
          </div>
        </motion.div>
      </div>

      {(result.recommendations || []).length > 0 && (
        <motion.div variants={itemVariants} className="card p-6">
          <div className="flex items-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <Lightbulb className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900">Recommendations</h3>
          </div>
          
          <div className="space-y-4">
            {(result.recommendations || []).map((recommendation, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-start space-x-3 p-4 bg-blue-50 rounded-lg"
              >
                <div className="w-6 h-6 bg-blue-200 rounded-full flex items-center justify-center text-blue-700 font-semibold text-sm flex-shrink-0 mt-0.5">
                  {index + 1}
                </div>
                <p className="text-gray-900 leading-relaxed">{recommendation}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {(result.detailed_analysis?.strengths || []).length > 0 && (
          <motion.div variants={itemVariants} className="card p-6">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Strengths</h3>
            </div>
            
            <div className="space-y-3">
              {(result.detailed_analysis?.strengths || []).map((strength, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-start space-x-3"
                >
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-900">{strength}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {(result.detailed_analysis?.areas_for_improvement || []).length > 0 && (
          <motion.div variants={itemVariants} className="card p-6">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-yellow-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Areas for Improvement</h3>
            </div>
            
            <div className="space-y-3">
              {(result.detailed_analysis?.areas_for_improvement || []).map((area, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-start space-x-3"
                >
                  <Target className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-900">{area}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
