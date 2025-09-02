export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  profile_picture?: string;
  date_of_birth?: string;
  country?: string;
  preferred_study_level?: string;
  preferred_fields?: string[];
  budget_min?: number;
  budget_max?: number;
  date_joined: string;
}

export interface University {
  id: number;
  name: string;
  country: string;
  city: string;
  website: string;
  logo?: string;
  description?: string;
  ranking_global?: number;
  ranking_national?: number;
  established_year?: number;
  student_population?: number;
  acceptance_rate?: number;
  contact_email?: string;
  contact_phone?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  courses_count?: number;
  contact_info?: UniversityContact;
}

export interface UniversityContact {
  admissions_email?: string;
  admissions_phone?: string;
  international_office_email?: string;
  international_office_phone?: string;
  financial_aid_email?: string;
  financial_aid_phone?: string;
}

export interface Course {
  id: number;
  title: string;
  university: University;
  level: 'bachelor' | 'master' | 'phd' | 'diploma' | 'certificate';
  field_of_study: string;
  description?: string;
  duration_value: number;
  duration_unit: 'months' | 'years' | 'weeks';
  duration_display: string;
  tuition_fee: number;
  currency: string;
  application_fee?: number;
  admission_requirements?: string;
  language_requirements?: string;
  prerequisites?: string;
  career_prospects?: string;
  course_url?: string;
  application_deadline?: string;
  start_date?: string;
  is_online: boolean;
  is_part_time: boolean;
  credits?: number;
  gpa_requirement?: number;
  popularity_score: number;
  average_rating?: number;
  reviews_count?: number;
  is_saved?: boolean;
  created_at: string;
  updated_at: string;
}

export interface CourseListItem {
  id: number;
  title: string;
  university_name: string;
  university_country: string;
  level: string;
  field_of_study: string;
  duration_display: string;
  tuition_fee: number;
  currency: string;
  is_online: boolean;
  is_part_time: boolean;
  average_rating?: number;
  is_saved?: boolean;
}

export interface SavedCourse {
  id: number;
  course: CourseListItem;
  notes?: string;
  created_at: string;
}

export interface CourseReview {
  id: number;
  user_name: string;
  course_title: string;
  rating: number;
  title: string;
  content: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface SearchFilters {
  search?: string;
  level?: string[];
  field_of_study?: string[];
  countries?: string[];
  min_fee?: number;
  max_fee?: number;
  is_online?: boolean;
  is_part_time?: boolean;
  currency?: string;
  ordering?: string;
}

export interface ChatSession {
  id: number;
  session_id: string;
  title?: string;
  messages: ChatMessage[];
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id: number;
  message_type: 'user' | 'assistant' | 'system';
  content: string;
  metadata?: any;
  timestamp: string;
}

export interface UserRecommendation {
  id: number;
  recommendation_type: 'course' | 'university' | 'field';
  title: string;
  description: string;
  confidence_score: number;
  reasoning?: string;
  metadata?: any;
  is_dismissed: boolean;
  created_at: string;
}

export interface SmartSearchResult {
  query_id: number;
  processed_query: string;
  extracted_filters: any;
  suggested_courses: CourseListItem[];
  confidence: number;
  processing_time: number;
}

export interface ApiResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

export interface AuthTokens {
  access: string;
  refresh: string;
  user: User;
}

export interface CourseStatistics {
  total_universities: number;
  total_courses: number;
  countries_count: number;
  fields_of_study: number;
  average_tuition_fee: number;
  level_distribution: Record<string, number>;
  top_countries: Array<{country: string; course_count: number}>;
}