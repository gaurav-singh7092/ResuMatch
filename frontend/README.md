# ResuMatch Frontend

A modern, responsive React/Next.js frontend for the ResuMatch AI-powered resume analysis demonstration platform.

**Note: This is an educational demonstration project, not intended for production use.**

## Features

- 🚀 **Modern Tech Stack**: Built with Next.js 14, TypeScript, and Tailwind CSS
- 🎨 **Beautiful UI**: Professional design with smooth animations using Framer Motion
- 📱 **Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- ⚡ **Fast Performance**: Optimized with Next.js features for excellent performance
- 🔒 **Type Safe**: Full TypeScript support for better development experience
- 🎯 **AI Integration**: Seamless integration with FastAPI backend for resume analysis
- 📊 **Rich Analytics**: Detailed scoring and visualization of analysis results
- 🔄 **Batch Processing**: Support for analyzing multiple resumes simultaneously
- 🛡️ **Error Handling**: Comprehensive error boundaries and user feedback
- 🌟 **Accessibility**: Built with accessibility best practices

## Tech Stack

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS with custom design system
- **Animations**: Framer Motion for smooth interactions
- **HTTP Client**: Axios for API communication
- **File Upload**: React Dropzone for drag-and-drop functionality
- **Notifications**: React Hot Toast for user feedback
- **Icons**: Lucide React for consistent iconography

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- ResuMatch FastAPI backend running on `http://localhost:8000`

### Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   ```
   
   Update `.env.local` with your configuration:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NODE_ENV=development
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

## Project Structure

```
frontend/
├── components/           # Reusable UI components
│   ├── AnalysisResults.tsx
│   ├── ErrorBoundary.tsx
│   ├── Features.tsx
│   ├── FileUpload.tsx
│   ├── Footer.tsx
│   ├── Header.tsx
│   ├── Hero.tsx
│   └── LoadingSpinner.tsx
├── hooks/               # Custom React hooks
│   └── useAnalysis.ts
├── pages/               # Next.js pages (routes)
│   ├── _app.tsx
│   ├── _document.tsx
│   ├── 404.tsx
│   ├── about.tsx
│   ├── analyze.tsx
│   ├── help.tsx
│   ├── index.tsx
│   └── status.tsx
├── services/            # API integration
│   └── api.ts
├── styles/              # Global styles
│   └── globals.css
└── config files         # TypeScript, Tailwind, etc.
```

## Features Overview

### 🏠 Homepage
- Hero section with animated gradients
- Feature showcase with hover effects
- Responsive design with mobile-first approach

### 📊 Analysis Page
- Single resume analysis
- Batch processing for multiple resumes
- Real-time progress tracking
- Detailed results visualization

### ℹ️ About Page
- Company information and mission
- Technology stack details
- Platform statistics and achievements

### ❓ Help & Support
- Comprehensive FAQ section
- Searchable help content
- Quick action links
- Contact information

### 📈 Status Page
- Real-time API health monitoring
- Supported file types display
- System status indicators

## API Integration

The frontend integrates with the ResuMatch FastAPI backend through:

- **Health Check**: Monitor API availability
- **Single Analysis**: Analyze individual resumes
- **Batch Analysis**: Process multiple resumes
- **File Support**: Check supported file formats

### Error Handling

- Comprehensive error boundaries
- User-friendly error messages
- Automatic retry mechanisms
- Graceful degradation

## Customization

### Design System

The application uses a custom design system built on Tailwind CSS:

- **Colors**: Primary blue palette with purple accents
- **Typography**: Inter font family with responsive scales
- **Spacing**: Consistent spacing using Tailwind's scale
- **Components**: Reusable component classes in `globals.css`

### Animation System

Framer Motion powers the smooth animations:

- Page transitions and component entrance effects
- Hover and interaction animations
- Loading states and progress indicators
- Responsive animation scaling

## Performance Optimizations

- **Next.js Optimizations**: Automatic code splitting and optimization
- **Image Optimization**: Next.js Image component for optimal loading
- **Bundle Analysis**: Webpack bundle analyzer for size monitoring
- **Caching**: Efficient API response caching
- **Lazy Loading**: Component-level lazy loading where appropriate

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript checks
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | FastAPI backend URL | `http://localhost:8000` |
| `NODE_ENV` | Environment mode | `development` |

## License

This project is an educational demonstration. Use for learning and educational purposes only.

## Support

For support and questions:
- Email: support@resumatch.ai
- Documentation: [ResuMatch Docs](https://docs.resumatch.ai)
- Issues: [GitHub Issues](https://github.com/resumatch/frontend/issues)
