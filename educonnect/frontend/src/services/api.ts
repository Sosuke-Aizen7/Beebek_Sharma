import axios, { AxiosResponse } from 'axios';
import { 
  User, University, Course, CourseListItem, SavedCourse, CourseReview,
  SearchFilters, ChatSession, ChatMessage, UserRecommendation,
  SmartSearchResult, ApiResponse, AuthTokens, CourseStatistics
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          localStorage.setItem('accessToken', access);
          
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, redirect to login
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
        }
      } else {
        // No refresh token, redirect to login
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  register: (userData: {
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    password: string;
    password_confirm: string;
  }) => api.post('/auth/register/', userData),

  login: (credentials: { email: string; password: string }): Promise<AxiosResponse<AuthTokens>> =>
    api.post('/auth/login/', credentials),

  refreshToken: (refresh: string) => api.post('/auth/token/refresh/', { refresh }),

  verifyEmail: (token: string) => api.post(`/auth/verify-email/${token}/`),

  requestPasswordReset: (email: string) => api.post('/auth/reset-password/', { email }),

  confirmPasswordReset: (token: string, password: string, passwordConfirm: string) =>
    api.post(`/auth/reset-password/${token}/`, {
      new_password: password,
      new_password_confirm: passwordConfirm,
    }),

  changePassword: (currentPassword: string, newPassword: string, newPasswordConfirm: string) =>
    api.post('/auth/change-password/', {
      current_password: currentPassword,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    }),

  getProfile: (): Promise<AxiosResponse<User>> => api.get('/auth/profile/'),

  updateProfile: (userData: Partial<User>) => api.patch('/auth/profile/', userData),
};

// Universities API
export const universitiesApi = {
  getList: (params?: any): Promise<AxiosResponse<ApiResponse<University>>> =>
    api.get('/universities/', { params }),

  getDetail: (id: number): Promise<AxiosResponse<University>> =>
    api.get(`/universities/${id}/`),

  getFeatured: (): Promise<AxiosResponse<University[]>> =>
    api.get('/featured-universities/'),
};

// Courses API
export const coursesApi = {
  getList: (filters?: SearchFilters): Promise<AxiosResponse<ApiResponse<CourseListItem>>> =>
    api.get('/courses/', { params: filters }),

  getDetail: (id: number): Promise<AxiosResponse<Course>> =>
    api.get(`/courses/${id}/`),

  getPopular: (): Promise<AxiosResponse<CourseListItem[]>> =>
    api.get('/popular/'),

  compare: (courseIds: number[]): Promise<AxiosResponse<{ courses: Course[]; comparison_date: string }>> =>
    api.post('/compare/', { course_ids: courseIds }),

  getStatistics: (): Promise<AxiosResponse<CourseStatistics>> =>
    api.get('/statistics/'),

  getReviews: (courseId: number): Promise<AxiosResponse<ApiResponse<CourseReview>>> =>
    api.get(`/courses/${courseId}/reviews/`),

  addReview: (courseId: number, review: { rating: number; title: string; content: string }) =>
    api.post(`/courses/${courseId}/reviews/`, review),
};

// Saved Courses API
export const savedCoursesApi = {
  getList: (): Promise<AxiosResponse<ApiResponse<SavedCourse>>> =>
    api.get('/saved-courses/'),

  save: (courseId: number, notes?: string) =>
    api.post('/saved-courses/', { course_id: courseId, notes }),

  update: (id: number, notes: string) =>
    api.patch(`/saved-courses/${id}/`, { notes }),

  remove: (id: number) => api.delete(`/saved-courses/${id}/`),
};

// AI Assistant API
export const aiApi = {
  chatQuery: (message: string, sessionId?: string) =>
    api.post('/ai/chat/query/', { message, session_id: sessionId }),

  smartSearch: (query: string, filters?: any): Promise<AxiosResponse<SmartSearchResult>> =>
    api.post('/ai/search/smart/', { query, filters }),

  getChatSessions: (): Promise<AxiosResponse<ApiResponse<ChatSession>>> =>
    api.get('/ai/chat/sessions/'),

  getChatSession: (sessionId: string): Promise<AxiosResponse<ChatSession>> =>
    api.get(`/ai/chat/sessions/${sessionId}/`),

  getRecommendations: (): Promise<AxiosResponse<ApiResponse<UserRecommendation>>> =>
    api.get('/ai/recommendations/'),

  generateRecommendations: () => api.post('/ai/recommendations/generate/'),

  dismissRecommendation: (id: number) =>
    api.post(`/ai/recommendations/${id}/dismiss/`),
};

export default api;