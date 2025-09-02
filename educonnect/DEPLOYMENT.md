# EduConnect Deployment Guide

This guide covers deploying EduConnect in various environments.

## 🐳 Docker Deployment (Recommended)

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 20GB+ disk space

### Quick Start
```bash
# Clone repository
git clone <repository-url>
cd educonnect

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start all services
./start.sh
```

### Manual Docker Commands
```bash
# Build and start
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v
```

## 🔧 Local Development

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL must be running)
python manage.py migrate
python manage.py load_sample_data

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Additional Services
```bash
# Start Celery worker (in separate terminal)
cd backend
source venv/bin/activate
celery -A educonnect_backend worker --loglevel=info

# Start Celery beat (in separate terminal)
celery -A educonnect_backend beat --loglevel=info
```

## 🌐 Production Deployment

### Environment Configuration

#### Backend (.env)
```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
DATABASE_HOST=your-db-host
DATABASE_NAME=educonnect_prod
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-secure-password
REDIS_URL=redis://your-redis-host:6379/0
OPENAI_API_KEY=your-openai-api-key
EMAIL_HOST_USER=your-production-email
EMAIL_HOST_PASSWORD=your-email-app-password
FRONTEND_URL=https://your-domain.com
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

#### Frontend (.env.production)
```env
REACT_APP_API_URL=https://api.your-domain.com/api
```

### AWS Deployment

#### Using AWS ECS with Fargate
```bash
# Build and push images to ECR
aws ecr create-repository --repository-name educonnect-backend
aws ecr create-repository --repository-name educonnect-frontend

# Tag and push images
docker build -t educonnect-backend ./backend
docker tag educonnect-backend:latest <account-id>.dkr.ecr.region.amazonaws.com/educonnect-backend:latest
docker push <account-id>.dkr.ecr.region.amazonaws.com/educonnect-backend:latest

docker build -t educonnect-frontend ./frontend
docker tag educonnect-frontend:latest <account-id>.dkr.ecr.region.amazonaws.com/educonnect-frontend:latest
docker push <account-id>.dkr.ecr.region.amazonaws.com/educonnect-frontend:latest
```

#### RDS PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE educonnect_prod;
CREATE USER educonnect_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE educonnect_prod TO educonnect_user;
```

#### ElastiCache Redis Setup
- Create Redis cluster
- Note the endpoint URL
- Update REDIS_URL in environment variables

### Google Cloud Platform Deployment

#### Using Cloud Run
```bash
# Build and deploy backend
gcloud builds submit --tag gcr.io/PROJECT_ID/educonnect-backend ./backend
gcloud run deploy educonnect-backend --image gcr.io/PROJECT_ID/educonnect-backend --platform managed

# Build and deploy frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/educonnect-frontend ./frontend
gcloud run deploy educonnect-frontend --image gcr.io/PROJECT_ID/educonnect-frontend --platform managed
```

### Heroku Deployment

#### Backend (Django)
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create educonnect-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set OPENAI_API_KEY=your-openai-key

# Deploy
git subtree push --prefix=backend heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py load_sample_data
```

#### Frontend (React)
```bash
# Create frontend app
heroku create educonnect-frontend

# Set buildpack
heroku buildpacks:set mars/create-react-app

# Set environment variables
heroku config:set REACT_APP_API_URL=https://educonnect-backend.herokuapp.com/api

# Deploy
git subtree push --prefix=frontend heroku main
```

## 🔒 Security Checklist

### Production Security
- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable database encryption
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Enable rate limiting
- [ ] Set up security headers

### Environment Variables Security
```bash
# Use environment-specific .env files
.env.development
.env.staging
.env.production

# Never commit .env files to version control
echo ".env*" >> .gitignore
```

## 📊 Monitoring & Logging

### Application Monitoring
```python
# Add to Django settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'educonnect.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Database Monitoring
- Set up PostgreSQL monitoring
- Monitor query performance
- Set up automated backups
- Monitor disk usage

### Celery Monitoring
```bash
# Install Flower for Celery monitoring
pip install flower

# Start Flower
celery -A educonnect_backend flower
```

## 🚀 Performance Optimization

### Database Optimization
```python
# Add database indexes
class Course(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['level', 'field_of_study']),
            models.Index(fields=['tuition_fee']),
            models.Index(fields=['university', 'level']),
        ]
```

### Caching Strategy
```python
# Add Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Frontend Optimization
```javascript
// Code splitting
const CoursesPage = lazy(() => import('./pages/CoursesPage'));

// Image optimization
const optimizedImageUrl = `${imageUrl}?w=400&h=300&fit=crop&auto=format`;
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy EduConnect

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt
          python manage.py test
      - name: Test Frontend
        run: |
          cd frontend
          npm install
          npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Your deployment commands here
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (nginx, AWS ALB, GCP Load Balancer)
- Multiple Django instances
- Separate Celery workers
- Database read replicas

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Use connection pooling
- Implement caching layers

## 🆘 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check PostgreSQL status
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up db
```

#### Celery Issues
```bash
# Check Redis connection
docker-compose logs redis

# Restart Celery workers
docker-compose restart celery celery-beat
```

#### Frontend Build Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Log Locations
- Django logs: `backend/educonnect.log`
- Docker logs: `docker-compose logs [service]`
- Celery logs: `docker-compose logs celery`

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review log files
3. Create an issue on GitHub
4. Contact support team

## 🔄 Updates

### Updating the Platform
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d

# Run new migrations if any
docker-compose exec backend python manage.py migrate
```

### Database Migrations
```bash
# Create new migrations
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# Backup before major migrations
docker-compose exec db pg_dump -U postgres educonnect_db > backup.sql
```