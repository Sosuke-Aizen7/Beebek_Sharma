# EduConnect API Documentation

Base URL: `http://localhost:8000/api`

## 🔐 Authentication

EduConnect uses JWT (JSON Web Tokens) for authentication.

### Register User
```http
POST /auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword",
  "password_confirm": "securepassword"
}
```

**Response:**
```json
{
  "message": "User created successfully. Please check your email for verification.",
  "user_id": 1
}
```

### Login
```http
POST /auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "profile_picture": null,
    "country": null,
    "preferred_study_level": null
  }
}
```

### Refresh Token
```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Get User Profile
```http
GET /auth/profile/
Authorization: Bearer <access_token>
```

### Update User Profile
```http
PATCH /auth/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith",
  "country": "USA",
  "preferred_study_level": "master",
  "budget_min": 10000,
  "budget_max": 50000
}
```

## 🏫 Universities

### List Universities
```http
GET /universities/
```

**Query Parameters:**
- `search`: Search by name, country, or city
- `country`: Filter by country
- `ordering`: Sort by `name`, `ranking_global`, `student_population`

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/universities/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Harvard University",
      "country": "USA",
      "city": "Cambridge",
      "logo": null,
      "ranking_global": 1,
      "courses_count": 25
    }
  ]
}
```

### University Details
```http
GET /universities/{id}/
```

### Featured Universities
```http
GET /featured-universities/
```

## 📚 Courses

### List Courses
```http
GET /courses/
```

**Query Parameters:**
- `search`: Search by title, field, university name, or description
- `level`: Filter by level (`bachelor`, `master`, `phd`, `diploma`, `certificate`)
- `field_of_study`: Filter by field of study
- `university__country`: Filter by university country
- `is_online`: Filter online courses (`true`/`false`)
- `is_part_time`: Filter part-time courses (`true`/`false`)
- `currency`: Filter by currency
- `min_fee`: Minimum tuition fee
- `max_fee`: Maximum tuition fee
- `countries`: Comma-separated list of countries
- `levels`: Comma-separated list of levels
- `fields`: Comma-separated list of fields
- `ordering`: Sort by `title`, `tuition_fee`, `duration_value`, `popularity_score`

**Response:**
```json
{
  "count": 500,
  "next": "http://localhost:8000/api/courses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Master of Science in Computer Science",
      "university_name": "Harvard University",
      "university_country": "USA",
      "level": "master",
      "field_of_study": "Computer Science",
      "duration_display": "2 years",
      "tuition_fee": 54880.00,
      "currency": "USD",
      "is_online": false,
      "is_part_time": false,
      "average_rating": 4.5,
      "is_saved": false
    }
  ]
}
```

### Course Details
```http
GET /courses/{id}/
```

**Response:**
```json
{
  "id": 1,
  "title": "Master of Science in Computer Science",
  "university": {
    "id": 1,
    "name": "Harvard University",
    "country": "USA",
    "city": "Cambridge",
    "logo": null,
    "ranking_global": 1
  },
  "level": "master",
  "field_of_study": "Computer Science",
  "description": "Advanced computer science program...",
  "duration_value": 2,
  "duration_unit": "years",
  "duration_display": "2 years",
  "tuition_fee": 54880.00,
  "currency": "USD",
  "application_fee": 100.00,
  "admission_requirements": "Bachelor's degree in CS...",
  "language_requirements": "TOEFL 100+ or IELTS 7.0+",
  "prerequisites": "Mathematics, Programming",
  "career_prospects": "Software Engineer, Data Scientist...",
  "course_url": "https://harvard.edu/cs-masters",
  "application_deadline": "2024-12-01",
  "start_date": "2024-09-01",
  "is_online": false,
  "is_part_time": false,
  "credits": 32,
  "gpa_requirement": 3.70,
  "popularity_score": 95,
  "average_rating": 4.5,
  "reviews_count": 25,
  "is_saved": false
}
```

### Popular Courses
```http
GET /popular/
```

### Course Comparison
```http
POST /compare/
Content-Type: application/json

{
  "course_ids": [1, 2, 3]
}
```

### Course Statistics
```http
GET /statistics/
```

**Response:**
```json
{
  "total_universities": 150,
  "total_courses": 1200,
  "countries_count": 25,
  "fields_of_study": 45,
  "average_tuition_fee": 25000.50,
  "level_distribution": {
    "bachelor": 400,
    "master": 600,
    "phd": 150,
    "diploma": 30,
    "certificate": 20
  },
  "top_countries": [
    {"country": "USA", "course_count": 300},
    {"country": "UK", "course_count": 200}
  ]
}
```

## 💾 Saved Courses

### List Saved Courses
```http
GET /saved-courses/
Authorization: Bearer <access_token>
```

### Save Course
```http
POST /saved-courses/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "course_id": 1,
  "notes": "Interesting program for my career goals"
}
```

### Update Saved Course
```http
PATCH /saved-courses/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "notes": "Updated notes about this course"
}
```

### Remove Saved Course
```http
DELETE /saved-courses/{id}/
Authorization: Bearer <access_token>
```

## 🤖 AI Assistant

### Chat Query
```http
POST /ai/chat/query/
Content-Type: application/json

{
  "message": "I'm looking for affordable computer science masters programs",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "session_id": "uuid-session-id",
  "response": "I can help you find affordable CS masters programs! Here are some great options...",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Smart Search
```http
POST /ai/search/smart/
Content-Type: application/json

{
  "query": "Show me affordable master's programs in computer science in Germany",
  "filters": {}
}
```

**Response:**
```json
{
  "query_id": 1,
  "processed_query": "affordable master's programs in computer science in Germany",
  "extracted_filters": {
    "level": "master",
    "field_of_study": "Computer Science",
    "country": "Germany",
    "max_fee": 20000
  },
  "suggested_courses": [...],
  "confidence": 0.85,
  "processing_time": 1.23
}
```

### Get Recommendations
```http
GET /ai/recommendations/
Authorization: Bearer <access_token>
```

### Generate New Recommendations
```http
POST /ai/recommendations/generate/
Authorization: Bearer <access_token>
```

### Dismiss Recommendation
```http
POST /ai/recommendations/{id}/dismiss/
Authorization: Bearer <access_token>
```

## 📝 Course Reviews

### List Course Reviews
```http
GET /courses/{course_id}/reviews/
```

### Add Course Review
```http
POST /courses/{course_id}/reviews/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rating": 5,
  "title": "Excellent program!",
  "content": "This course exceeded my expectations..."
}
```

## 🔍 Search & Filtering

### Advanced Search Examples

#### Search by Multiple Criteria
```http
GET /courses/?search=computer science&level=master&university__country=USA&min_fee=10000&max_fee=60000&ordering=-popularity_score
```

#### Filter by Multiple Countries
```http
GET /courses/?countries=USA,UK,Canada&level=bachelor,master
```

#### Online Courses Only
```http
GET /courses/?is_online=true&field_of_study=Business
```

## 📊 Error Handling

### Error Response Format
```json
{
  "error": "Error message",
  "details": "Detailed error information",
  "code": "ERROR_CODE"
}
```

### Common HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

### Authentication Errors
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

## 🚀 Rate Limiting

### Default Limits
- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour
- AI endpoints: 50 requests/hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 📱 API Versioning

Current API version: `v1`

Future versions will be accessible via:
- Header: `Accept: application/json; version=v2`
- URL: `/api/v2/courses/`

## 🔧 Development Tools

### API Testing with curl

#### Login and get token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@educonnect.com", "password": "admin123"}'
```

#### Use token for authenticated requests
```bash
curl -X GET http://localhost:8000/api/saved-courses/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Postman Collection
Import the provided Postman collection for easy API testing:
- [EduConnect API Collection](./postman_collection.json)

## 📊 Analytics & Metrics

### Search Analytics
Track user search behavior:
```http
GET /analytics/search-trends/
Authorization: Bearer <admin_token>
```

### Course Popularity
Track course views and saves:
```http
GET /analytics/course-popularity/
Authorization: Bearer <admin_token>
```

## 🔄 Webhooks (Future Feature)

### University Data Updates
```http
POST /webhooks/university-update/
Content-Type: application/json

{
  "university_id": 1,
  "event": "course_added",
  "data": {...}
}
```