#!/usr/bin/env python3

import os
import json
from datetime import datetime

from text_extractor import TextExtractor
from text_preprocessor import TextPreprocessor
from similarity_engine import SimilarityEngine


def create_sample_files():
    resume_text = """
JOHN DOE
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567
Location: San Francisco, CA

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years of experience in full-stack web development.
Passionate about creating scalable applications using modern technologies.

EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2020 - Present
• Developed and maintained web applications using Python, Django, and React
• Implemented RESTful APIs serving 1M+ requests daily
• Led a team of 4 developers in agile development practices
• Improved application performance by 40% through code optimization

Software Developer | StartupXYZ | 2018 - 2020
• Built responsive web applications using JavaScript, HTML5, and CSS3
• Worked with PostgreSQL and MongoDB databases
• Implemented CI/CD pipelines using Jenkins and Docker
• Collaborated with cross-functional teams using Scrum methodology

TECHNICAL SKILLS
Programming Languages: Python, JavaScript, TypeScript, Java, SQL
Frameworks: Django, React, Node.js, Express.js, Flask
Databases: PostgreSQL, MongoDB, Redis, MySQL
Tools & Technologies: Git, Docker, Kubernetes, AWS, Jenkins, Linux
Methodologies: Agile, Scrum, TDD, CI/CD

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2014 - 2018
GPA: 3.7/4.0

CERTIFICATIONS
• AWS Certified Solutions Architect
• Certified Scrum Master (CSM)

PROJECTS
E-commerce Platform (2021)
• Developed a full-stack e-commerce application using Django and React
• Integrated payment processing with Stripe API
• Deployed on AWS with auto-scaling capabilities

Task Management System (2020)
• Created a collaborative task management tool using Node.js and MongoDB
• Implemented real-time updates using WebSocket technology
• Used by 500+ users across multiple teams
"""

    job_description = """
Senior Software Engineer - Full Stack

Company: InnovateTech Solutions
Location: San Francisco, CA (Remote options available)
Experience Level: 4-7 years

ABOUT THE ROLE
We are seeking a talented Senior Software Engineer to join our growing engineering team. 
You will be responsible for designing, developing, and maintaining scalable web applications 
that serve millions of users worldwide.

KEY RESPONSIBILITIES
• Design and develop robust, scalable web applications
• Write clean, maintainable, and well-tested code
• Collaborate with product managers and designers to implement new features
• Mentor junior developers and contribute to technical decision-making
• Optimize application performance and ensure security best practices
• Participate in code reviews and maintain high code quality standards

REQUIRED QUALIFICATIONS
• Bachelor's degree in Computer Science or related field
• 4+ years of experience in software development
• Strong proficiency in Python and JavaScript
• Experience with modern web frameworks (Django, React, or similar)
• Solid understanding of database design (PostgreSQL, MongoDB)
• Experience with RESTful API design and development
• Proficiency with Git version control
• Experience with cloud platforms (AWS, GCP, or Azure)
• Strong problem-solving and analytical skills
• Excellent communication and teamwork abilities

PREFERRED QUALIFICATIONS
• Experience with microservices architecture
• Knowledge of containerization technologies (Docker, Kubernetes)
• Experience with CI/CD pipelines
• Familiarity with agile development methodologies
• Previous experience in a leadership or mentoring role
• Contributions to open-source projects

TECHNICAL STACK
• Backend: Python, Django, PostgreSQL, Redis
• Frontend: React, TypeScript, HTML5, CSS3
• Infrastructure: AWS, Docker, Kubernetes, Jenkins
• Monitoring: Prometheus, Grafana, ELK Stack

WHAT WE OFFER
• Competitive salary: $120,000 - $160,000
• Equity package
• Comprehensive health benefits
• Flexible working arrangements
• Professional development budget
• Modern tech stack and tools
• Collaborative and inclusive work environment

TO APPLY
Please submit your resume and a brief cover letter explaining why you're interested 
in this position and how your experience aligns with our requirements.
"""

    os.makedirs("examples", exist_ok=True)

    with open("examples/sample_resume.txt", "w", encoding="utf-8") as f:
        f.write(resume_text)

    with open("examples/sample_job_description.txt", "w", encoding="utf-8") as f:
        f.write(job_description)

    print("✅ Sample files created:")
    print("   - examples/sample_resume.txt")
    print("   - examples/sample_job_description.txt")

    return "examples/sample_resume.txt", "examples/sample_job_description.txt"


def example_basic_analysis():
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Resume-Job Matching Analysis")
    print("=" * 60)

    resume_file, job_file = create_sample_files()

    print("Initializing ResuMatch components...")
    extractor = TextExtractor()
    preprocessor = TextPreprocessor()
    similarity_engine = SimilarityEngine()

    print("\n1. Extracting text from resume...")
    extraction_result = extractor.extract_text(resume_file)

    if extraction_result["success"]:
        print(f"✅ Text extracted successfully using: {extraction_result['extraction_method']}")
        resume_text = extraction_result["text"]
    else:
        print(f"❌ Text extraction failed: {extraction_result.get('error')}")
        return

    print("\n2. Loading job description...")
    with open(job_file, "r", encoding="utf-8") as f:
        job_text = f.read()
    print("✅ Job description loaded")

    print("\n3. Preprocessing texts...")
    resume_processed = preprocessor.preprocess_text(resume_text)
    job_processed = preprocessor.preprocess_text(job_text)

    print(f"✅ Resume preprocessing completed:")
    print(f"   - Word count: {resume_processed['statistics']['word_count']}")
    print(f"   - Skills found: {resume_processed['statistics']['skills_found']}")
    print(f"   - Entities found: {resume_processed['statistics']['entities_found']}")

    print(f"✅ Job description preprocessing completed:")
    print(f"   - Word count: {job_processed['statistics']['word_count']}")
    print(f"   - Skills found: {job_processed['statistics']['skills_found']}")

    print("\n4. Extracting features...")
    resume_features = preprocessor.get_feature_vector(resume_processed)
    job_features = preprocessor.get_feature_vector(job_processed)
    print("✅ Feature extraction completed")

    print("\n5. Calculating similarity...")
    similarity_result = similarity_engine.calculate_similarity(resume_features, job_features)

    print("\n6. Analysis Results:")
    print("-" * 40)
    print(f"Overall Match Score: {similarity_result['overall_score']:.1f}%")
    print(f"Assessment: {similarity_result['detailed_analysis']['overall_assessment']}")

    print("\nComponent Scores:")
    for component, score in similarity_result["component_scores"].items():
        print(f"  {component.replace('_', ' ').title()}: {score*100:.1f}%")

    print(f"\nMatched Skills ({len(similarity_result['matched_skills'])}):")
    for skill in similarity_result["matched_skills"][:10]:  # Show first 10
        print(f"  ✅ {skill}")

    print(f"\nMissing Skills ({len(similarity_result['missing_skills'])}):")
    for skill in similarity_result["missing_skills"][:10]:  # Show first 10
        print(f"  ❌ {skill}")

    print("\nRecommendations:")
    for rec in similarity_result["recommendations"]:
        print(f"  💡 {rec}")

    detailed_results = {
        "timestamp": datetime.now().isoformat(),
        "resume_analysis": resume_processed,
        "job_analysis": job_processed,
        "similarity_analysis": similarity_result,
        "extraction_info": extraction_result,
    }

    os.makedirs("examples/results", exist_ok=True)
    with open("examples/results/detailed_analysis.json", "w", encoding="utf-8") as f:
        json.dump(detailed_results, f, indent=2, default=str, ensure_ascii=False)

    print(f"\n✅ Detailed results saved to: examples/results/detailed_analysis.json")


def example_text_extraction():
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Text Extraction")
    print("=" * 60)

    extractor = TextExtractor()

    resume_file, _ = create_sample_files()

    print(f"Extracting text from: {resume_file}")
    result = extractor.extract_text(resume_file)

    if result["success"]:
        print(f"✅ Extraction successful!")
        print(f"   Method: {result['extraction_method']}")
        print(f"   File type: {result['file_type']}")
        print(f"   Text length: {len(result['text'])} characters")
        print(f"   Metadata: {result.get('metadata', {})}")

        preview = result["text"][:200] + "..." if len(result["text"]) > 200 else result["text"]
        print(f"\nText preview:\n{preview}")

        os.makedirs("examples/results", exist_ok=True)
        with open("examples/results/extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"\n✅ Full extracted text saved to: examples/results/extracted_text.txt")
    else:
        print(f"❌ Extraction failed: {result.get('error')}")


def example_text_preprocessing():
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Text Preprocessing Analysis")
    print("=" * 60)

    preprocessor = TextPreprocessor()

    resume_file, _ = create_sample_files()
    with open(resume_file, "r", encoding="utf-8") as f:
        text = f.read()

    print("Performing comprehensive text preprocessing...")
    result = preprocessor.preprocess_text(text)

    print(f"\n✅ Preprocessing completed!")

    stats = result["statistics"]
    print(f"\nText Statistics:")
    print(f"  Character count: {stats['character_count']:,}")
    print(f"  Word count: {stats['word_count']:,}")
    print(f"  Sentence count: {stats['sentence_count']}")
    print(f"  Unique tokens: {stats['unique_tokens']}")
    print(f"  Lexical diversity: {stats['lexical_diversity']:.3f}")

    entities = result["entities"]
    print(f"\nExtracted Entities:")
    for entity_type, entity_list in entities.items():
        if entity_list:
            print(f"  {entity_type.title()}: {entity_list}")

    skills = result["skills"]
    print(f"\nExtracted Skills:")
    for skill_category, skill_list in skills.items():
        if isinstance(skill_list, list) and skill_list:
            print(f"  {skill_category.replace('_', ' ').title()}: {skill_list}")
        elif isinstance(skill_list, list):
            continue
        else:
            print(f"  {skill_category.replace('_', ' ').title()}: {skill_list}")

    sections = result["sections"]
    print(f"\nIdentified Sections:")
    for section_name, section_content in sections.items():
        if section_content:
            preview = section_content[:100] + "..." if len(section_content) > 100 else section_content
            print(f"  {section_name.title()}: {preview}")

    quality_scores = preprocessor._calculate_text_quality_score(text, result)
    print(f"\nQuality Assessment:")
    for metric, score in quality_scores.items():
        percentage = score * 100
        print(f"  {metric.replace('_', ' ').title()}: {percentage:.1f}%")

    os.makedirs("examples/results", exist_ok=True)
    with open("examples/results/preprocessing_analysis.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str, ensure_ascii=False)

    print(f"\n✅ Preprocessing results saved to: examples/results/preprocessing_analysis.json")


def example_similarity_calculation():
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Similarity Calculation with Custom Weights")
    print("=" * 60)

    default_engine = SimilarityEngine()

    skill_focused_engine = SimilarityEngine()
    skill_focused_weights = {
        "semantic_similarity": 0.20,
        "skill_match": 0.50,
        "experience_match": 0.15,
        "education_match": 0.05,
        "keyword_match": 0.10,
    }
    skill_focused_engine.update_weights(skill_focused_weights)

    preprocessor = TextPreprocessor()
    resume_file, job_file = create_sample_files()

    with open(resume_file, "r", encoding="utf-8") as f:
        resume_text = f.read()
    with open(job_file, "r", encoding="utf-8") as f:
        job_text = f.read()

    resume_processed = preprocessor.preprocess_text(resume_text)
    job_processed = preprocessor.preprocess_text(job_text)

    resume_features = preprocessor.get_feature_vector(resume_processed)
    job_features = preprocessor.get_feature_vector(job_processed)

    print("Calculating similarity with different weight configurations...")

    default_result = default_engine.calculate_similarity(resume_features, job_features)
    skill_focused_result = skill_focused_engine.calculate_similarity(resume_features, job_features)

    print(f"\nResults Comparison:")
    print("-" * 50)
    print(f"{'Metric':<25} {'Default':<10} {'Skill-Focused':<15}")
    print("-" * 50)
    print(f"{'Overall Score':<25} {default_result['overall_score']:<10.1f} {skill_focused_result['overall_score']:<15.1f}")

    for component in default_result["component_scores"]:
        default_score = default_result["component_scores"][component] * 100
        skill_focused_score = skill_focused_result["component_scores"][component] * 100
        component_name = component.replace("_", " ").title()
        print(f"{component_name:<25} {default_score:<10.1f} {skill_focused_score:<15.1f}")

    print(f"\nWeight Configurations:")
    print("Default weights:", default_engine.weights)
    print("Skill-focused weights:", skill_focused_engine.weights)


def main():
    print("🎯 ResuMatch Usage Examples")
    print("This script demonstrates how to use ResuMatch components programmatically")

    try:
        example_basic_analysis()
        example_text_extraction()
        example_text_preprocessing()
        example_similarity_calculation()

        print("\n" + "=" * 60)
        print("🎉 ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nGenerated files:")
        print("- examples/sample_resume.txt")
        print("- examples/sample_job_description.txt")
        print("- examples/results/detailed_analysis.json")
        print("- examples/results/extracted_text.txt")
        print("- examples/results/preprocessing_analysis.json")

        print("\nNext steps:")
        print("1. Explore the generated files to understand the data structures")
        print("2. Modify the examples to work with your own data")
        print("3. Try the web interface: python main.py")
        print("4. Use the REST API endpoints for programmatic access")

    except Exception as e:
        print(f"\n❌ Example execution failed: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
