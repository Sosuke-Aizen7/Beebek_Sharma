import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { 
  MagnifyingGlassIcon, 
  AcademicCapIcon, 
  GlobeAltIcon,
  SparklesIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline';
import { coursesApi, universitiesApi } from '../services/api';
import { CourseListItem, University, CourseStatistics } from '../types';

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch data for homepage
  const { data: popularCourses } = useQuery({
    queryKey: ['popular-courses'],
    queryFn: () => coursesApi.getPopular(),
  });

  const { data: featuredUniversities } = useQuery({
    queryKey: ['featured-universities'],
    queryFn: () => universitiesApi.getFeatured(),
  });

  const { data: statistics } = useQuery({
    queryKey: ['course-statistics'],
    queryFn: () => coursesApi.getStatistics(),
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleSmartSearch = (query: string) => {
    navigate(`/smart-search?q=${encodeURIComponent(query)}`);
  };

  return (
    <div className="bg-white dark:bg-gray-900">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-blue-800">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Discover Your Perfect
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">
                Educational Journey
              </span>
            </h1>
            <p className="text-xl text-gray-200 mb-8 max-w-3xl mx-auto">
              Explore thousands of courses from top international universities. 
              Compare programs, fees, and requirements all in one place.
            </p>

            {/* Search Bar */}
            <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search for courses, universities, or fields of study..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-4 text-lg rounded-lg border-0 focus:ring-2 focus:ring-yellow-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white shadow-lg"
                />
                <MagnifyingGlassIcon className="absolute left-4 top-4 h-6 w-6 text-gray-400" />
              </div>
            </form>

            {/* Quick Search Suggestions */}
            <div className="flex flex-wrap justify-center gap-3 mb-12">
              {[
                'Computer Science Masters in Germany',
                'Affordable MBA programs',
                'PhD in Engineering',
                'Online courses in Business'
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => handleSmartSearch(suggestion)}
                  className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-full text-sm transition-all duration-200 backdrop-blur-sm"
                >
                  {suggestion}
                </button>
              ))}
            </div>

            {/* Statistics */}
            {statistics?.data && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
                <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm">
                  <div className="text-3xl font-bold text-white">{statistics.data.total_universities.toLocaleString()}</div>
                  <div className="text-gray-200 text-sm">Universities</div>
                </div>
                <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm">
                  <div className="text-3xl font-bold text-white">{statistics.data.total_courses.toLocaleString()}</div>
                  <div className="text-gray-200 text-sm">Courses</div>
                </div>
                <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm">
                  <div className="text-3xl font-bold text-white">{statistics.data.countries_count}</div>
                  <div className="text-gray-200 text-sm">Countries</div>
                </div>
                <div className="bg-white bg-opacity-10 rounded-lg p-4 backdrop-blur-sm">
                  <div className="text-3xl font-bold text-white">{statistics.data.fields_of_study}</div>
                  <div className="text-gray-200 text-sm">Fields of Study</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose EduConnect?
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Everything you need to find and compare international education opportunities
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 dark:bg-primary-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <GlobeAltIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Global Coverage
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Access courses from universities worldwide with comprehensive information and real-time updates.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 dark:bg-primary-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <SparklesIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                AI-Powered Search
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Use natural language to find courses. Our AI understands your needs and provides personalized recommendations.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 dark:bg-primary-900 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <AcademicCapIcon className="h-8 w-8 text-primary-600 dark:text-primary-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Compare & Save
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Compare courses side by side, save your favorites, and track your application progress.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Popular Courses Section */}
      {popularCourses?.data && popularCourses.data.length > 0 && (
        <div className="py-16 bg-white dark:bg-gray-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
                Popular Courses
              </h2>
              <Link
                to="/courses"
                className="flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
              >
                View All
                <ArrowRightIcon className="ml-1 h-5 w-5" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {popularCourses.data.slice(0, 6).map((course) => (
                <div
                  key={course.id}
                  className="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 hover:shadow-lg transition-shadow duration-200"
                >
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {course.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 text-sm mb-2">
                    {course.university_name} • {course.university_country}
                  </p>
                  <div className="flex items-center justify-between mb-4">
                    <span className="bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 px-2 py-1 rounded text-xs font-medium">
                      {course.level}
                    </span>
                    <span className="text-gray-900 dark:text-white font-semibold">
                      {course.currency} {course.tuition_fee.toLocaleString()}
                    </span>
                  </div>
                  <Link
                    to={`/courses/${course.id}`}
                    className="block w-full text-center bg-primary-600 hover:bg-primary-700 text-white py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    View Details
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Featured Universities Section */}
      {featuredUniversities?.data && featuredUniversities.data.length > 0 && (
        <div className="py-16 bg-gray-50 dark:bg-gray-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
                Featured Universities
              </h2>
              <Link
                to="/universities"
                className="flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
              >
                View All
                <ArrowRightIcon className="ml-1 h-5 w-5" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featuredUniversities.data.slice(0, 6).map((university) => (
                <div
                  key={university.id}
                  className="bg-white dark:bg-gray-900 rounded-lg p-6 hover:shadow-lg transition-shadow duration-200"
                >
                  <div className="flex items-center mb-4">
                    {university.logo && (
                      <img
                        src={university.logo}
                        alt={university.name}
                        className="w-12 h-12 rounded-lg mr-4 object-cover"
                      />
                    )}
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {university.name}
                      </h3>
                      <p className="text-gray-600 dark:text-gray-300 text-sm">
                        {university.city}, {university.country}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between mb-4">
                    {university.ranking_global && (
                      <span className="bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 px-2 py-1 rounded text-xs font-medium">
                        Rank #{university.ranking_global}
                      </span>
                    )}
                    <span className="text-gray-600 dark:text-gray-300 text-sm">
                      {university.courses_count} courses
                    </span>
                  </div>
                  
                  <Link
                    to={`/universities/${university.id}`}
                    className="block w-full text-center bg-gray-900 dark:bg-white hover:bg-gray-800 dark:hover:bg-gray-100 text-white dark:text-gray-900 py-2 rounded-md text-sm font-medium transition-colors duration-200"
                  >
                    Explore University
                  </Link>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* CTA Section */}
      <div className="py-16 bg-primary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Start Your Journey?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands of students who have found their perfect course through EduConnect
          </p>
          <div className="space-x-4">
            <Link
              to="/register"
              className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold transition-colors duration-200"
            >
              Get Started Free
            </Link>
            <Link
              to="/courses"
              className="border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-3 rounded-lg font-semibold transition-colors duration-200"
            >
              Browse Courses
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;