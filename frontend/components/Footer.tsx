import React from 'react';
import { motion } from 'framer-motion';
import { Target, Github, Twitter, Linkedin, Mail } from 'lucide-react';
import Link from 'next/link';

const footerLinks = {
  project: [
    { name: 'Source Code', href: 'https://github.com/gauravsingh07/ResuMatch' },
    { name: 'Documentation', href: '/help' },
    { name: 'About Project', href: '/about' },
  ],
  navigation: [
    { name: 'Home', href: '/' },
    { name: 'Analyze', href: '/analyze' },
    { name: 'About', href: '/about' },
    { name: 'Help', href: '/help' },
  ],
};

const socialLinks = [
  { name: 'GitHub', icon: Github, href: 'https://github.com/gauravsingh07/ResuMatch' },
  { name: 'Email', icon: Mail, href: 'mailto:gaurav91345@gmail.com' },
];

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-10">
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="mb-6"
            >
              <Link href="/" className="flex items-center space-x-3 mb-4 md:mb-6">
                <div className="w-10 h-10 bg-gradient-to-r from-primary-600 to-purple-600 rounded-xl flex items-center justify-center">
                  <Target className="w-6 h-6 text-white" />
                </div>
                <span className="text-2xl font-bold">ResuMatch</span>
              </Link>
              <p className="text-gray-400 leading-relaxed mb-4 md:mb-6 text-sm md:text-base">
                A demonstration project showcasing AI-powered resume analysis using natural language 
                processing and machine learning techniques. Built for educational and portfolio purposes.
              </p>
              <div className="flex space-x-3 md:space-x-4">
                {socialLinks.map((social) => (
                  <motion.a
                    key={social.name}
                    href={social.href}
                    whileHover={{ scale: 1.1, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-primary-600 transition-colors duration-200"
                  >
                    <social.icon className="w-5 h-5" />
                  </motion.a>
                ))}
              </div>
            </motion.div>
          </div>

          {Object.entries(footerLinks).map(([category, links], index) => (
            <motion.div
              key={category}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
            >
              <h3 className="text-lg font-semibold mb-3 md:mb-4 capitalize">{category}</h3>
              <ul className="space-y-2 md:space-y-3">
                {links.map((link) => (
                  <li key={link.name}>
                    <Link
                      href={link.href}
                      className="text-gray-400 hover:text-white transition-colors duration-200 text-sm md:text-base"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-12 md:mt-16 pt-6 md:pt-8 border-t border-gray-800"
        >
          <div className="max-w-md">
            <h3 className="text-lg font-semibold mb-3 md:mb-4">Get in Touch</h3>
            <p className="text-gray-400 mb-3 md:mb-4 text-sm md:text-base">
              Have questions about this project or want to connect? Feel free to reach out!
            </p>
            <motion.a
              href="mailto:gaurav91345@gmail.com"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary inline-flex items-center px-4 md:px-6 py-2 md:py-3 text-sm md:text-base"
            >
              <Mail className="w-4 h-4 mr-2" />
              Contact Developer
            </motion.a>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mt-12 md:mt-16 pt-6 md:pt-8 border-t border-gray-800 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0"
        >
          <p className="text-gray-400 text-sm md:text-base text-center md:text-left">
            © {new Date().getFullYear()} ResuMatch. Created by Gaurav Singh.
          </p>
          <div className="text-sm md:text-base text-gray-400 text-center md:text-right">
            Built with Next.js, TypeScript & Tailwind CSS
          </div>
        </motion.div>
      </div>
    </footer>
  );
}
