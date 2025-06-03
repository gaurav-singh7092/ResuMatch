import React, { useState } from 'react';
import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { 
  ChevronDown, 
  Search, 
  FileText, 
  Upload, 
  Zap, 
  Users,
  HelpCircle,
  Mail
} from 'lucide-react';

const faqs = [
  {
    category: 'Getting Started',
    questions: [
      {
        question: 'What file formats does ResuMatch support?',
        answer: 'ResuMatch supports PDF, DOC, DOCX, TXT, JPG, and PNG files. We recommend using PDF or DOCX formats for the best results.',
      },
      {
        question: 'How do I upload a resume for analysis?',
        answer: 'Simply drag and drop your resume file onto the upload area on the Analyze page, or click to browse and select your file. The file will be automatically processed once uploaded.',
      },
      {
        question: 'What information do I need to provide?',
        answer: 'You need to upload your resume and paste the job description you want to match against. Make sure the job description is detailed for better analysis results.',
      },
    ],
  },
  {
    category: 'Analysis & Results',
    questions: [
      {
        question: 'How accurate is the analysis?',
        answer: 'This is a demonstration project that showcases NLP and machine learning techniques for text analysis. The accuracy depends on the quality of input data and the complexity of the matching requirements.',
      },
      {
        question: 'What does the scoring system mean?',
        answer: 'Scores are given on a 0-100 scale across multiple dimensions: Skills Match, Experience Match, Education Match, and Keyword Match. The scoring system is designed to be generous - scores of 75%+ indicate excellent matches, 60-74% are good matches, 45-59% are fair matches, and below 45% indicates areas that need improvement.',
      },
      {
        question: 'How long does analysis take?',
        answer: 'Most analyses complete in under 5 seconds. Complex resumes or longer job descriptions may take slightly longer, but typically no more than 30 seconds.',
      },
      {
        question: 'Can I analyze multiple resumes at once?',
        answer: 'Yes! The system supports batch processing through the API interface, allowing you to process multiple resumes against a single job description.',
      },
    ],
  },
  {
    category: 'Privacy & Security',
    questions: [
      {
        question: 'Is my resume data secure?',
        answer: 'This is a demo application. In a production environment, uploaded files should be processed securely and deleted after analysis. For this demo, be mindful of the data you upload.',
      },
      {
        question: 'Do you share my information with third parties?',
        answer: 'This is an open-source demonstration project. No data is intentionally shared, but as with any demo application, avoid uploading sensitive personal information.',
      },
      {
        question: 'How long is my data retained?',
        answer: 'In this demo, files are processed temporarily. For production use, proper data retention policies should be implemented.',
      },
    ],
  },
  {
    category: 'Technical Support',
    questions: [
      {
        question: 'What browsers are supported?',
        answer: 'ResuMatch works on all modern browsers including Chrome, Firefox, Safari, and Edge. We recommend using the latest version for the best experience.',
      },
      {
        question: 'Why is my file upload failing?',
        answer: 'Check that your file is under 10MB and in a supported format. Also ensure you have a stable internet connection. Try refreshing the page and uploading again.',
      },
      {
        question: 'Can I use ResuMatch on mobile devices?',
        answer: 'Yes, ResuMatch is fully responsive and works on mobile devices. However, for the best experience, we recommend using a desktop or tablet.',
      },
    ],
  },
];

const quickActions = [
  {
    icon: Upload,
    title: 'Upload Resume',
    description: 'Start by uploading your resume',
    action: 'Go to Analyze',
    href: '/analyze',
  },
  {
    icon: FileText,
    title: 'Sample Job Description',
    description: 'Need a job description example?',
    action: 'View Examples',
    href: '#examples',
  },
  {
    icon: Zap,
    title: 'Quick Tutorial',
    description: 'Learn how to use ResuMatch',
    action: 'Watch Tutorial',
    href: '#tutorial',
  },
];

export default function Help() {
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const toggleExpanded = (id: string) => {
    setExpandedItems(prev => 
      prev.includes(id) 
        ? prev.filter(item => item !== id)
        : [...prev, id]
    );
  };

  const filteredFaqs = faqs.map(category => ({
    ...category,
    questions: category.questions.filter(
      q => 
        q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
        q.answer.toLowerCase().includes(searchTerm.toLowerCase())
    )
  })).filter(category => category.questions.length > 0);

  return (
    <>
      <Head>
        <title>Help & FAQ - ResuMatch</title>
        <meta 
          name="description" 
          content="Get help with ResuMatch. Find answers to frequently asked questions about resume analysis, file uploads, scoring, and more." 
        />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <Header />
        
        <main className="pt-20 md:pt-24 pb-12 md:pb-16">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-12 md:mb-16"
            >
              <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 md:mb-6">
                Help &
                <span className="gradient-text block">Support</span>
              </h1>
              <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto px-4">
                Find answers to common questions or get in touch with our support team
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="mb-8 md:mb-12"
            >
              <div className="relative max-w-2xl mx-auto">
                <Search className="absolute left-3 md:left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4 md:w-5 md:h-5" />
                <input
                  type="text"
                  placeholder="Search for help..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 md:pl-12 pr-4 py-3 md:py-4 rounded-xl md:rounded-2xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-base md:text-lg"
                />
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="mb-12 md:mb-16"
            >
              <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-4 md:mb-6 px-4 sm:px-0">Quick Actions</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
                {quickActions.map((action, index) => (
                  <motion.a
                    key={action.title}
                    href={action.href}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
                    whileHover={{ scale: 1.02 }}
                    className="card p-4 md:p-6 text-center group hover:shadow-lg transition-all duration-300"
                  >
                    <div className="w-10 h-10 md:w-12 md:h-12 bg-gradient-to-br from-primary-100 to-purple-100 rounded-xl flex items-center justify-center mx-auto mb-3 md:mb-4 group-hover:from-primary-600 group-hover:to-purple-600 transition-all duration-300">
                      <action.icon className="w-5 h-5 md:w-6 md:h-6 text-primary-600 group-hover:text-white transition-colors duration-300" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-2 text-sm md:text-base">{action.title}</h3>
                    <p className="text-gray-600 text-xs md:text-sm mb-3 md:mb-4 leading-relaxed">{action.description}</p>
                    <span className="text-primary-600 font-medium group-hover:text-primary-700 text-sm">
                      {action.action} →
                    </span>
                  </motion.a>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <h2 className="text-xl md:text-2xl font-bold text-gray-900 mb-6 md:mb-8 px-4 sm:px-0">Frequently Asked Questions</h2>
              
              {filteredFaqs.length === 0 && searchTerm && (
                <div className="text-center py-8 md:py-12">
                  <HelpCircle className="w-12 h-12 md:w-16 md:h-16 text-gray-300 mx-auto mb-3 md:mb-4" />
                  <p className="text-gray-500 text-sm md:text-base">No results found for "{searchTerm}"</p>
                </div>
              )}

              {filteredFaqs.map((category, categoryIndex) => (
                <motion.div
                  key={category.category}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.4 + categoryIndex * 0.1 }}
                  className="mb-6 md:mb-8"
                >
                  <h3 className="text-lg md:text-xl font-semibold text-gray-900 mb-3 md:mb-4 px-4 sm:px-0">
                    {category.category}
                  </h3>
                  <div className="space-y-2 md:space-y-3">
                    {category.questions.map((faq, index) => {
                      const itemId = `${category.category}-${index}`;
                      const isExpanded = expandedItems.includes(itemId);
                      
                      return (
                        <div key={index} className="card overflow-hidden">
                          <button
                            onClick={() => toggleExpanded(itemId)}
                            className="w-full p-4 md:p-6 text-left flex items-center justify-between hover:bg-gray-50 transition-colors duration-200"
                          >
                            <span className="font-medium text-gray-900 pr-3 md:pr-4 text-sm md:text-base leading-relaxed">
                              {faq.question}
                            </span>
                            <motion.div
                              animate={{ rotate: isExpanded ? 180 : 0 }}
                              transition={{ duration: 0.3 }}
                              className="flex-shrink-0"
                            >
                              <ChevronDown className="w-4 h-4 md:w-5 md:h-5 text-gray-400" />
                            </motion.div>
                          </button>
                          <AnimatePresence>
                            {isExpanded && (
                              <motion.div
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                transition={{ duration: 0.3 }}
                                className="overflow-hidden"
                              >
                                <div className="px-4 md:px-6 pb-4 md:pb-6 text-gray-600 leading-relaxed text-sm md:text-base">
                                  {faq.answer}
                                </div>
                              </motion.div>
                            )}
                          </AnimatePresence>
                        </div>
                      );
                    })}
                  </div>
                </motion.div>
              ))}
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="mt-12 md:mt-16"
            >
              <div className="card p-6 md:p-8 text-center">
                <h3 className="text-xl md:text-2xl font-bold text-gray-900 mb-3 md:mb-4">
                  Still Need Help?
                </h3>
                <p className="text-gray-600 mb-6 md:mb-8 max-w-2xl mx-auto text-sm md:text-base leading-relaxed px-4">
                  Can't find what you're looking for? Our support team is here to help 
                  you get the most out of ResuMatch.
                </p>
                <div className="flex flex-col sm:flex-row gap-3 md:gap-4 justify-center max-w-md mx-auto">
                  <motion.a
                    href="mailto:gaurav91345@gmail.com"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="btn-primary inline-flex items-center justify-center py-3 px-4 text-sm md:text-base"
                  >
                    <Mail className="w-4 h-4 md:w-5 md:h-5 mr-2" />
                    Email Support
                  </motion.a>
                </div>
              </div>
            </motion.div>
          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
