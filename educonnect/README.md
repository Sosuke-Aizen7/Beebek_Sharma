# EduConnect - International University Course Aggregator

EduConnect is a comprehensive full-stack web platform that aggregates, manages, and displays academic course and fee information from international universities. The platform provides an AI-enhanced interface for students to search, compare, and explore higher education programs globally.

## 🚀 Features

- **Global Course Database**: Access thousands of courses from universities worldwide
- **AI-Powered Search**: Natural language search with intelligent filtering
- **Course Comparison**: Side-by-side comparison of programs, fees, and requirements
- **Personalized Recommendations**: AI-driven course and university suggestions
- **User Profiles**: Save courses, track preferences, and manage applications
- **Real-time Data**: Web scraping keeps course information up-to-date
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark Mode**: Modern UI with light/dark theme support

## 🛠️ Tech Stack

### Frontend
- **React.js** with TypeScript
- **React Router** for navigation
- **Tailwind CSS** for styling
- **React Query** for data fetching
- **React Hook Form** for form management
- **Axios** for API calls

### Backend
- **Django** with Django REST Framework
- **PostgreSQL** database
- **Celery** for background tasks
- **Redis** for caching and task queue
- **JWT** authentication

### AI & Scraping
- **OpenAI API** for AI features
- **BeautifulSoup & Scrapy** for web scraping
- **Selenium** for JavaScript-heavy sites

## 📦 Installation & Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.13+ (for local development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd educonnect
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/admin
   - Admin Login: admin@educonnect.com / admin123

### Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database (requires PostgreSQL running)
python manage.py migrate
python load_sample_data.py
python manage.py runserver
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/` - Update user profile

### Courses Endpoints
- `GET /api/courses/` - List courses with filtering
- `GET /api/courses/{id}/` - Course details
- `GET /api/popular/` - Popular courses
- `POST /api/compare/` - Compare courses
- `GET /api/statistics/` - Platform statistics

### Universities Endpoints
- `GET /api/universities/` - List universities
- `GET /api/universities/{id}/` - University details
- `GET /api/featured-universities/` - Featured universities

### AI Assistant Endpoints
- `POST /api/ai/chat/query/` - Chat with AI assistant
- `POST /api/ai/search/smart/` - Smart search with NLP
- `GET /api/ai/recommendations/` - Get personalized recommendations

### Saved Courses Endpoints
- `GET /api/saved-courses/` - User's saved courses
- `POST /api/saved-courses/` - Save a course
- `DELETE /api/saved-courses/{id}/` - Remove saved course

## 🎯 Key Features

### 1. Smart Search
Users can search using natural language:
- "Show me affordable master's programs in computer science in Germany"
- "Find online MBA courses under $50,000"
- "PhD programs in engineering with good rankings"

### 2. Course Comparison
Compare up to 5 courses side-by-side:
- Tuition fees and duration
- Admission requirements
- University rankings
- Course details

### 3. AI Chatbot
Integrated AI assistant helps users:
- Find relevant courses
- Answer questions about programs
- Provide study abroad guidance
- Suggest alternatives

### 4. Web Scraping
Automated data collection:
- Scheduled scraping jobs
- Real-time course updates
- Configurable scraping rules
- Data validation and processing

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_HOST=localhost
DATABASE_NAME=educonnect_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=your-openai-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Database Schema

The platform uses PostgreSQL with the following main tables:
- `users` - User accounts and preferences
- `universities` - University information
- `courses` - Course details and metadata
- `saved_courses` - User's saved courses
- `chat_sessions` & `chat_messages` - AI chat history
- `scraping_jobs` & `scraped_data` - Web scraping management

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Production Deployment
1. Set up production environment variables
2. Configure PostgreSQL and Redis servers
3. Set up SSL certificates
4. Use Docker Compose with production overrides:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

### Scaling Considerations
- Use multiple Celery workers for scraping tasks
- Implement database read replicas for heavy read workloads
- Add CDN for static files and images
- Use load balancer for multiple backend instances

## 🔒 Security Features

- JWT-based authentication
- CORS protection
- CSRF protection
- XSS prevention
- SQL injection protection
- Rate limiting on API endpoints
- Email verification
- Secure password policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Email: support@educonnect.com
- Documentation: [Link to docs]

## 🔮 Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced AI recommendations
- [ ] University application tracking
- [ ] Scholarship information integration
- [ ] Student reviews and ratings
- [ ] Virtual campus tours
- [ ] Multi-language support