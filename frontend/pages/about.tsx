import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { 
  Brain, 
  Target, 
  Zap, 
  Users, 
  Award, 
  TrendingUp,
  Shield,
  Clock
} from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'Text Processing',
    description: 'Natural language processing pipeline with entity recognition and skill extraction.',
  },
  {
    icon: Target,
    title: 'Similarity Analysis',
    description: 'Semantic similarity calculation using transformer-based sentence embeddings.',
  },
  {
    icon: Zap,
    title: 'Multi-Format Input',
    description: 'Text extraction from PDF, DOC, DOCX, TXT, and image files.',
  },
  {
    icon: Users,
    title: 'Batch Processing',
    description: 'API endpoints for processing multiple files programmatically.',
  },
  {
    icon: Award,
    title: 'Component Scoring',
    description: 'Detailed analysis across skills, experience, education, and keyword matching.',
  },
  {
    icon: TrendingUp,
    title: 'Scalable Solution',
    description: 'Built with modern architecture for growing recruitment needs.',
  },
];

const stats = [
  { number: 'AI', label: 'Powered Analysis' },
  { number: 'NLP', label: 'Text Processing' },
  { number: 'Open', label: 'Source Code' },
  { number: 'Python', label: 'Backend Tech' },
];

export default function About() {
  return (
    <>
      <Head>
        <title>About ResuMatch - AI Resume Analysis Platform</title>
        <meta 
          name="description" 
          content="Learn about ResuMatch's AI-powered resume analysis platform using natural language processing and machine learning algorithms for smart recruitment." 
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
              className="text-center mb-12 md:mb-16"
            >
              <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-4 md:mb-6">
                About
                <span className="gradient-text block">ResuMatch</span>
              </h1>
              <p className="text-lg md:text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed px-4">
                AI-powered resume analysis platform using natural language processing and machine 
                learning to intelligently match resume content with job descriptions.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="card p-8 md:p-12 mb-12 md:mb-16 text-center"
            >
              <div className="max-w-4xl mx-auto">
                <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4 md:mb-6">Our Mission</h2>
                <p className="text-base md:text-lg text-gray-600 leading-relaxed">
                  ResuMatch transforms the recruitment process by leveraging advanced natural language processing 
                  and machine learning techniques to analyze resumes and match them with job descriptions. 
                  Our platform helps organizations make data-driven hiring decisions by providing detailed 
                  insights into candidate compatibility and skill alignment.
                </p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="mb-16"
            >
              <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
                Platform Features
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {features.map((feature, index) => (
                  <motion.div
                    key={feature.title}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.4 + index * 0.1 }}
                    className="card p-8 text-center group hover:shadow-xl transition-all duration-300"
                  >
                    <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:from-primary-600 group-hover:to-purple-600 transition-all duration-300">
                      <feature.icon className="w-8 h-8 text-primary-600 group-hover:text-white transition-colors duration-300" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">{feature.title}</h3>
                    <p className="text-gray-600">{feature.description}</p>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="bg-gradient-to-r from-primary-600 to-purple-600 rounded-3xl p-12 mb-16"
            >
              <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-white mb-4">
                  Trusted by Organizations
                </h2>
                <p className="text-primary-100 text-lg">
                  Our platform delivers reliable AI-powered recruitment solutions
                </p>
              </div>
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
                {stats.map((stat, index) => (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
                    className="text-center"
                  >
                    <div className="text-4xl lg:text-5xl font-bold text-white mb-2">
                      {stat.number}
                    </div>
                    <div className="text-primary-100 font-medium">
                      {stat.label}
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="mb-16"
            >
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-6">
                    Advanced Technology Stack
                  </h2>
                  <p className="text-lg text-gray-600 mb-8">
                    ResuMatch is built using a modern technology stack to deliver professional-grade 
                    AI-powered recruitment solutions. Our platform utilizes advanced natural language 
                    processing techniques and machine learning approaches for intelligent resume analysis.
                  </p>
                  <div className="space-y-4">
                    <div className="flex items-center">
                      <Shield className="w-6 h-6 text-primary-600 mr-3" />
                      <span className="text-gray-700">Enterprise-ready data processing capabilities</span>
                    </div>
                    <div className="flex items-center">
                      <Clock className="w-6 h-6 text-primary-600 mr-3" />
                      <span className="text-gray-700">Real-time analysis and processing</span>
                    </div>
                    <div className="flex items-center">
                      <TrendingUp className="w-6 h-6 text-primary-600 mr-3" />
                      <span className="text-gray-700">Advanced AI/ML implementation for recruitment</span>
                    </div>
                  </div>
                </div>
                <div className="card p-8">
                  <h3 className="text-xl font-semibold text-gray-900 mb-6">Core Technologies</h3>
                  <div className="space-y-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900">Natural Language Processing</h4>
                      <p className="text-sm text-gray-600">Advanced NLP for content understanding</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900">Machine Learning</h4>
                      <p className="text-sm text-gray-600">Sophisticated matching algorithms</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900">FastAPI Backend</h4>
                      <p className="text-sm text-gray-600">High-performance Python API</p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900">React Frontend</h4>
                      <p className="text-sm text-gray-600">Modern, responsive user interface</p>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.7 }}
              className="text-center"
            >
              <div className="card p-12">
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Ready to Transform Your Hiring?
                </h2>
                <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
                  Experience the power of AI-driven resume analysis and see how our platform 
                  can streamline your recruitment process with intelligent candidate matching.
                </p>
                <motion.a
                  href="/analyze"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-primary inline-flex items-center"
                >
                  <Zap className="w-5 h-5 mr-2" />
                  Start Analysis
                </motion.a>
              </div>
            </motion.div>
          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
