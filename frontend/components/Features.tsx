import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Target, Brain, Users } from 'lucide-react';

const features = [
	{
		icon: Brain,
		title: 'AI-Powered Analysis',
		description:
			'Advanced natural language processing algorithms analyze text content and extract meaningful insights from resumes.',
		color: 'from-blue-500 to-cyan-500',
	},
	{
		icon: Target,
		title: 'Precise Matching',
		description:
			'Sophisticated similarity calculation with detailed component scoring across skills, experience, and education.',
		color: 'from-purple-500 to-pink-500',
	},
	{
		icon: Zap,
		title: 'Multi-Format Support',
		description:
			'Supports PDF, DOC, DOCX, TXT, and image files with text extraction capabilities.',
		color: 'from-green-500 to-emerald-500',
	},
	{
		icon: Users,
		title: 'Batch Processing',
		description:
			'Process multiple resumes against a single job description for comparison analysis.',
		color: 'from-orange-500 to-red-500',
	},
];

const containerVariants = {
	hidden: { opacity: 0 },
	visible: {
		opacity: 1,
		transition: {
			staggerChildren: 0.2,
		},
	},
};

const itemVariants = {
	hidden: { opacity: 0, y: 50 },
	visible: {
		opacity: 1,
		y: 0,
		transition: {
			duration: 0.6,
			ease: 'easeOut',
		},
	},
};

export default function Features() {
	return (
		<section className="py-16 md:py-20 lg:py-24 bg-white">
			<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
				<motion.div
					initial="hidden"
					whileInView="visible"
					viewport={{ once: true, margin: '-100px' }}
					variants={containerVariants}
					className="text-center mb-12 md:mb-16 lg:mb-20"
				>
					<motion.h2
						variants={itemVariants}
						className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 md:mb-6"
					>
						Advanced Features for
						<span className="gradient-text block mt-2">
							Smart Recruitment
						</span>
					</motion.h2>
					<motion.p
						variants={itemVariants}
						className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto px-4"
					>
						This demo showcases how AI technology can be used to analyze and
						match resume content with job requirements using advanced NLP
						techniques.
					</motion.p>
				</motion.div>

				<motion.div
					initial="hidden"
					whileInView="visible"
					viewport={{ once: true, margin: '-100px' }}
					variants={containerVariants}
					className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8"
				>
					{features.map((feature, index) => (
						<motion.div
							key={feature.title}
							variants={itemVariants}
							className="group relative"
						>
							<div className="card p-6 md:p-8 h-full group-hover:scale-105 transition-all duration-300">
								<div
									className={`w-14 h-14 md:w-16 md:h-16 rounded-2xl bg-gradient-to-r ${feature.color} p-3 md:p-4 mb-4 md:mb-6 group-hover:scale-110 transition-transform duration-300`}
								>
									<feature.icon className="w-8 h-8 text-white" />
								</div>

								<h3 className="text-lg md:text-xl font-semibold text-gray-900 mb-3 md:mb-4 group-hover:text-primary-600 transition-colors duration-300">
									{feature.title}
								</h3>

								<p className="text-gray-600 leading-relaxed text-sm md:text-base">
									{feature.description}
								</p>

								<div
									className={`absolute inset-0 rounded-xl bg-gradient-to-r ${feature.color} opacity-0 group-hover:opacity-5 transition-opacity duration-300`}
								/>
							</div>
						</motion.div>
					))}
				</motion.div>
			</div>
		</section>
	);
}
