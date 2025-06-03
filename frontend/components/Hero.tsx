import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Sparkles } from 'lucide-react';
import Link from 'next/link';

const floatingElements = [
	{ id: 1, x: '10%', y: '20%', delay: 0 },
	{ id: 2, x: '80%', y: '15%', delay: 0.5 },
	{ id: 3, x: '15%', y: '70%', delay: 1 },
	{ id: 4, x: '85%', y: '65%', delay: 1.5 },
	{ id: 5, x: '50%', y: '80%', delay: 2 },
];

export default function Hero() {
	return (
		<section className="relative min-h-screen flex items-center justify-center overflow-hidden gradient-bg pt-20 md:pt-24">
			<div className="absolute inset-0 overflow-hidden">
				{floatingElements.map((element) => (
					<motion.div
						key={element.id}
						className="absolute w-4 h-4 bg-primary-400 rounded-full opacity-20"
						style={{ left: element.x, top: element.y }}
						animate={{
							y: [0, -20, 0],
							scale: [1, 1.2, 1],
							opacity: [0.2, 0.5, 0.2],
						}}
						transition={{
							duration: 3,
							repeat: Infinity,
							delay: element.delay,
							ease: 'easeInOut',
						}}
					/>
				))}
			</div>

			<div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-primary-400 to-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float" />
			<div className="absolute top-3/4 right-1/4 w-96 h-96 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-float animation-delay-400" />

			<div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center py-12 md:py-16">
				<motion.div
					initial={{ opacity: 0, y: 30 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.8, ease: 'easeOut' }}
					className="mb-6 md:mb-8"
				>
					<motion.div
						initial={{ scale: 0 }}
						animate={{ scale: 1 }}
						transition={{ delay: 0.2, duration: 0.5, type: 'spring' }}
						className="inline-flex items-center px-4 py-2 rounded-full bg-white/80 backdrop-blur-sm border border-primary-200 text-primary-700 font-medium mb-6 md:mb-8"
					>
						<Sparkles className="w-4 h-4 mr-2" />
						AI-Powered Resume Matching
					</motion.div>

					<h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-4 md:mb-6 leading-tight">
						<motion.span
							initial={{ opacity: 0, x: -50 }}
							animate={{ opacity: 1, x: 0 }}
							transition={{ delay: 0.4, duration: 0.8 }}
						>
							Find the
						</motion.span>
						<motion.span
							initial={{ opacity: 0, scale: 0.5 }}
							animate={{ opacity: 1, scale: 1 }}
							transition={{ delay: 0.6, duration: 0.8 }}
							className="gradient-text block"
						>
							Perfect Match
						</motion.span>
						<motion.span
							initial={{ opacity: 0, x: 50 }}
							animate={{ opacity: 1, x: 0 }}
							transition={{ delay: 0.8, duration: 0.8 }}
						>
							Every Time
						</motion.span>
					</h1>
				</motion.div>

				<motion.p
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 1, duration: 0.8 }}
					className="text-lg md:text-xl lg:text-2xl text-gray-600 mb-8 md:mb-12 max-w-4xl mx-auto leading-relaxed px-4"
				>
					Leverage AI-powered resume analysis to make smarter hiring decisions.
					Get detailed compatibility scores, skill matching, and actionable insights
					for every candidate.
				</motion.p>

				<motion.div
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 1.2, duration: 0.8 }}
					className="flex items-center justify-center px-4"
				>
					<Link href="/analyze" className="relative group">
						<motion.div
							whileHover={{ scale: 1.05 }}
							whileTap={{ scale: 0.95 }}
							className="btn-primary text-lg px-8 md:px-12 py-4 md:py-5 group relative overflow-hidden"
						>
							<motion.div
								className="absolute inset-0 bg-gradient-to-r from-primary-600 via-purple-600 to-primary-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
								animate={{
									backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
								}}
								transition={{
									duration: 2,
									repeat: Infinity,
									ease: 'linear',
								}}
								style={{
									backgroundSize: '200% 100%',
								}}
							/>

							<span className="relative flex items-center justify-center">
								<motion.span
									className="mr-3"
									animate={{
										scale: [1, 1.1, 1],
									}}
									transition={{
										duration: 2,
										repeat: Infinity,
										ease: 'easeInOut',
									}}
								>
									✨
								</motion.span>
								Start Analyzing Now
								<motion.div
									className="ml-3"
									animate={{
										x: [0, 5, 0],
									}}
									transition={{
										duration: 1.5,
										repeat: Infinity,
										ease: 'easeInOut',
									}}
								>
									<ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
								</motion.div>
							</span>

							<motion.div
								className="absolute top-0 left-0 w-full h-full bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12"
								animate={{
									x: ['-100%', '100%'],
								}}
								transition={{
									duration: 3,
									repeat: Infinity,
									ease: 'easeInOut',
									repeatDelay: 2,
								}}
							/>
						</motion.div>
					</Link>
				</motion.div>

				<motion.div
					initial={{ opacity: 0, y: 30 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ delay: 1.4, duration: 0.8 }}
					className="mt-12 md:mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 max-w-4xl mx-auto px-4"
				>
					{[
						{ value: 'AI-Powered', label: 'Text Analysis' },
						{ value: 'Multi-Format', label: 'File Support' },
						{ value: 'Open Source', label: 'Application' },
					].map((stat, index) => (
						<motion.div
							key={stat.label}
							initial={{ opacity: 0, scale: 0.8 }}
							animate={{ opacity: 1, scale: 1 }}
							transition={{ delay: 1.6 + index * 0.1, duration: 0.5 }}
							className="glass-effect rounded-2xl p-4 md:p-6"
						>
							<div className="text-lg md:text-xl font-bold text-primary-600 mb-2">
								{stat.value}
							</div>
							<div className="text-gray-600 font-medium text-sm md:text-base">
								{stat.label}
							</div>
						</motion.div>
					))}
				</motion.div>
			</div>
		</section>
	);
}
