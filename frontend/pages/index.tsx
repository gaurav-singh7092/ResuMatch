import React from 'react';
import Head from 'next/head';
import Header from '@/components/Header';
import Hero from '@/components/Hero';
import Features from '@/components/Features';
import Footer from '@/components/Footer';

export default function Home() {
  return (
    <>
      <Head>
        <title>ResuMatch - AI Resume Analysis</title>
        <meta 
          name="description" 
          content="AI-powered resume and job description matching using natural language processing and machine learning techniques." 
        />
        <meta name="keywords" content="resume analysis, AI matching, job compatibility, NLP, machine learning" />
        <meta property="og:title" content="ResuMatch - AI Resume Analysis" />
        <meta property="og:description" content="AI-powered resume and job description matching using NLP." />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
      </Head>

      <div className="min-h-screen">
        <Header />
        <main>
          <Hero />
          <Features />
        </main>
        <Footer />
      </div>
    </>
  );
}
