# EduConnect - Project Structure

```
educonnect/
├── 📁 backend/                          # Django Backend
│   ├── 📁 educonnect_backend/           # Main Django project
│   │   ├── __init__.py                  # Celery app initialization
│   │   ├── settings.py                  # Django settings with all configurations
│   │   ├── urls.py                      # Main URL configuration
│   │   ├── wsgi.py                      # WSGI application
│   │   └── celery.py                    # Celery configuration
│   │
│   ├── 📁 users/                        # User management app
│   │   ├── models.py                    # User, EmailVerification, PasswordReset models
│   │   ├── serializers.py               # DRF serializers for user operations
│   │   ├── views.py                     # Authentication views and user management
│   │   ├── urls.py                      # User-related URL patterns
│   │   ├── admin.py                     # Django admin configuration
│   │   └── 📁 management/commands/      # Custom Django commands
│   │       └── load_sample_data.py      # Sample data loading command
│   │
│   ├── 📁 courses/                      # Course and university management
│   │   ├── models.py                    # University, Course, SavedCourse, Reviews models
│   │   ├── serializers.py               # Course and university serializers
│   │   ├── views.py                     # Course CRUD, search, comparison views
│   │   ├── urls.py                      # Course-related URL patterns
│   │   └── admin.py                     # Course admin interface
│   │
│   ├── 📁 scraper/                      # Web scraping module
│   │   ├── models.py                    # ScrapingJob, ScrapingRule, ScrapedData models
│   │   ├── scraper_engine.py            # Main scraping logic with BeautifulSoup/Selenium
│   │   ├── tasks.py                     # Celery tasks for background scraping
│   │   └── admin.py                     # Scraping admin interface
│   │
│   ├── 📁 ai_assistant/                 # AI features
│   │   ├── models.py                    # ChatSession, ChatMessage, Recommendations models
│   │   ├── views.py                     # Chat and recommendation views
│   │   ├── api_views.py                 # AI API endpoints
│   │   ├── ai_utils.py                  # OpenAI integration and AI utilities
│   │   ├── serializers.py               # AI-related serializers
│   │   └── urls.py                      # AI endpoint URL patterns
│   │
│   ├── 📁 media/                        # User uploaded files
│   ├── 📁 static/                       # Static files
│   ├── 📁 venv/                         # Python virtual environment
│   ├── requirements.txt                 # Python dependencies
│   ├── .env                            # Environment variables
│   ├── .env.example                    # Environment template
│   ├── manage.py                       # Django management script
│   ├── load_sample_data.py             # Standalone sample data loader
│   └── Dockerfile                      # Backend Docker configuration
│
├── 📁 frontend/                         # React Frontend
│   ├── 📁 public/                       # Public assets
│   ├── 📁 src/
│   │   ├── 📁 components/               # Reusable React components
│   │   │   ├── 📁 Layout/               # Layout components
│   │   │   │   ├── Header.tsx           # Navigation header with search
│   │   │   │   ├── Footer.tsx           # Footer with links and info
│   │   │   │   └── Layout.tsx           # Main layout wrapper
│   │   │   └── 📁 common/               # Common UI components
│   │   │       ├── LoadingSpinner.tsx   # Loading indicator
│   │   │       └── ProtectedRoute.tsx   # Route protection component
│   │   │
│   │   ├── 📁 pages/                    # Page components
│   │   │   ├── HomePage.tsx             # Landing page with hero and features
│   │   │   ├── LoginPage.tsx            # User login form
│   │   │   ├── RegisterPage.tsx         # User registration form
│   │   │   └── CoursesPage.tsx          # Course listing with filters
│   │   │
│   │   ├── 📁 context/                  # React Context providers
│   │   │   ├── AuthContext.tsx          # Authentication state management
│   │   │   └── ThemeContext.tsx         # Dark/light theme management
│   │   │
│   │   ├── 📁 services/                 # API integration
│   │   │   └── api.ts                   # Axios configuration and API calls
│   │   │
│   │   ├── 📁 hooks/                    # Custom React hooks
│   │   │   └── useApi.ts                # API call hooks and utilities
│   │   │
│   │   ├── 📁 types/                    # TypeScript type definitions
│   │   │   └── index.ts                 # All TypeScript interfaces
│   │   │
│   │   ├── App.tsx                      # Main React application
│   │   ├── index.tsx                    # React entry point
│   │   └── index.css                    # Global styles with Tailwind
│   │
│   ├── package.json                     # Node.js dependencies
│   ├── tailwind.config.js               # Tailwind CSS configuration
│   ├── postcss.config.js                # PostCSS configuration
│   ├── .env                            # Frontend environment variables
│   └── Dockerfile                      # Frontend Docker configuration
│
├── 📁 docs/                            # Documentation (placeholder)
├── 📁 scripts/                         # Utility scripts (placeholder)
│
├── docker-compose.yml                  # Multi-service Docker configuration
├── .env.example                       # Environment variables template
├── start.sh                           # Platform startup script
├── test_setup.py                      # Setup verification script
├── README.md                          # Main project documentation
├── DEPLOYMENT.md                      # Deployment guide
├── API_DOCUMENTATION.md               # Complete API documentation
├── PROJECT_SUMMARY.md                 # Project overview and status
└── STRUCTURE.md                       # This file - project structure
```

## 🔧 Key Configuration Files

### Docker Configuration
- `docker-compose.yml` - Multi-service orchestration
- `backend/Dockerfile` - Django backend container
- `frontend/Dockerfile` - React frontend container

### Backend Configuration
- `settings.py` - Django settings with all integrations
- `requirements.txt` - Python dependencies
- `celery.py` - Background task configuration

### Frontend Configuration
- `package.json` - Node.js dependencies and scripts
- `tailwind.config.js` - UI styling configuration
- `tsconfig.json` - TypeScript compiler settings

### Environment Files
- `.env.example` - Template for environment variables
- `backend/.env` - Backend environment configuration
- `frontend/.env` - Frontend environment configuration

## 📊 Database Schema Overview

### User Management
```sql
users (
  id, email, username, first_name, last_name,
  profile_picture, country, preferred_study_level,
  budget_min, budget_max, is_email_verified
)

email_verification_tokens (user_id, token, expires_at, is_used)
password_reset_tokens (user_id, token, expires_at, is_used)
```

### Academic Data
```sql
universities (
  id, name, country, city, website, logo, description,
  ranking_global, student_population, acceptance_rate
)

courses (
  id, title, university_id, level, field_of_study,
  duration_value, duration_unit, tuition_fee, currency,
  admission_requirements, gpa_requirement, popularity_score
)

saved_courses (user_id, course_id, notes, created_at)
course_reviews (user_id, course_id, rating, title, content)
```

### AI & Analytics
```sql
chat_sessions (id, user_id, session_id, title)
chat_messages (session_id, message_type, content, timestamp)
user_recommendations (user_id, type, title, confidence_score)
search_logs (user_id, query, filters_applied, results_count)
```

### Web Scraping
```sql
scraping_jobs (university_id, status, courses_found, error_message)
scraping_rules (university_id, base_url, selectors, use_selenium)
scraped_data (scraping_job_id, raw_data, processed, course_id)
```

## 🚀 Getting Started

### 1. Quick Setup (Docker)
```bash
./start.sh
```

### 2. Manual Setup
```bash
# Backend
cd backend && source venv/bin/activate
python manage.py migrate && python manage.py load_sample_data
python manage.py runserver

# Frontend
cd frontend && npm install && npm start
```

### 3. Verify Setup
```bash
python test_setup.py
```

## 🎯 Development Guidelines

### Backend Development
- Follow Django best practices
- Use DRF for all API endpoints
- Implement proper error handling
- Add comprehensive logging
- Write unit tests for models and views

### Frontend Development
- Use TypeScript for type safety
- Follow React best practices
- Implement responsive design
- Use React Query for data fetching
- Add proper error boundaries

### Code Organization
- Keep components small and focused
- Use custom hooks for reusable logic
- Implement proper prop types
- Follow consistent naming conventions
- Add comprehensive comments

This structure provides a solid foundation for a scalable, maintainable international education platform.