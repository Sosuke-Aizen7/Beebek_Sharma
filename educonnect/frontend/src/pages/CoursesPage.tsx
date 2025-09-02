import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSearchParams, Link } from 'react-router-dom';
import { coursesApi } from '../services/api';
import { SearchFilters, CourseListItem } from '../types';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { 
  FunnelIcon, 
  MagnifyingGlassIcon,
  BookmarkIcon,
  HeartIcon
} from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';

const CoursesPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [filters, setFilters] = useState<SearchFilters>({
    search: searchParams.get('q') || '',
    level: [],
    field_of_study: [],
    countries: [],
    min_fee: undefined,
    max_fee: undefined,
    is_online: undefined,
    ordering: '-popularity_score'
  });
  const [showFilters, setShowFilters] = useState(false);

  const { data: coursesData, isLoading, error } = useQuery({
    queryKey: ['courses', filters],
    queryFn: () => coursesApi.getList(filters),
  });

  const handleFilterChange = (key: keyof SearchFilters, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    
    // Update URL params
    const params = new URLSearchParams();
    Object.entries(newFilters).forEach(([k, v]) => {
      if (v !== undefined && v !== '' && (Array.isArray(v) ? v.length > 0 : true)) {
        params.set(k, Array.isArray(v) ? v.join(',') : String(v));
      }
    });
    setSearchParams(params);
  };

  const clearFilters = () => {
    const clearedFilters: SearchFilters = {
      search: '',
      level: [],
      field_of_study: [],
      countries: [],
      min_fee: undefined,
      max_fee: undefined,
      is_online: undefined,
      ordering: '-popularity_score'
    };
    setFilters(clearedFilters);
    setSearchParams({});
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 dark:text-red-400">Failed to load courses</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-4 bg-primary-600 text-white px-4 py-2 rounded-md"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Explore Courses
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Discover thousands of courses from top universities worldwide
        </p>
      </div>

      {/* Search and Filters */}
      <div className="mb-8 space-y-4">
        {/* Search Bar */}
        <div className="relative">
          <input
            type="text"
            placeholder="Search courses, universities, or fields..."
            value={filters.search || ''}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          />
          <MagnifyingGlassIcon className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
        </div>

        {/* Filter Toggle */}
        <div className="flex justify-between items-center">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400"
          >
            <FunnelIcon className="h-5 w-5 mr-2" />
            Filters
          </button>
          
          {coursesData && (
            <p className="text-gray-600 dark:text-gray-300">
              {coursesData.data.count} courses found
            </p>
          )}
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Level Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Level
                </label>
                <select
                  multiple
                  value={filters.level || []}
                  onChange={(e) => {
                    const values = Array.from(e.target.selectedOptions, option => option.value);
                    handleFilterChange('level', values);
                  }}
                  className="w-full border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
                  <option value="bachelor">Bachelor's</option>
                  <option value="master">Master's</option>
                  <option value="phd">PhD</option>
                  <option value="diploma">Diploma</option>
                  <option value="certificate">Certificate</option>
                </select>
              </div>

              {/* Fee Range */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Fee Range (USD)
                </label>
                <div className="flex space-x-2">
                  <input
                    type="number"
                    placeholder="Min"
                    value={filters.min_fee || ''}
                    onChange={(e) => handleFilterChange('min_fee', e.target.value ? Number(e.target.value) : undefined)}
                    className="w-full border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2"
                  />
                  <input
                    type="number"
                    placeholder="Max"
                    value={filters.max_fee || ''}
                    onChange={(e) => handleFilterChange('max_fee', e.target.value ? Number(e.target.value) : undefined)}
                    className="w-full border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2"
                  />
                </div>
              </div>

              {/* Sort By */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Sort By
                </label>
                <select
                  value={filters.ordering || ''}
                  onChange={(e) => handleFilterChange('ordering', e.target.value)}
                  className="w-full border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2"
                >
                  <option value="-popularity_score">Most Popular</option>
                  <option value="tuition_fee">Lowest Fee</option>
                  <option value="-tuition_fee">Highest Fee</option>
                  <option value="title">Name A-Z</option>
                  <option value="-title">Name Z-A</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={clearFilters}
                className="text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 text-sm"
              >
                Clear All Filters
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Course Grid */}
      {coursesData && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {coursesData.data.results.map((course: CourseListItem) => (
            <div
              key={course.id}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow duration-200"
            >
              <div className="flex justify-between items-start mb-3">
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  course.level === 'bachelor' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                  course.level === 'master' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
                  course.level === 'phd' ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200' :
                  'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                }`}>
                  {course.level}
                </span>
                <button className="text-gray-400 hover:text-red-500">
                  {course.is_saved ? <HeartSolidIcon className="h-5 w-5 text-red-500" /> : <HeartIcon className="h-5 w-5" />}
                </button>
              </div>

              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
                {course.title}
              </h3>

              <p className="text-gray-600 dark:text-gray-300 text-sm mb-2">
                {course.university_name}
              </p>

              <p className="text-gray-500 dark:text-gray-400 text-sm mb-3">
                {course.university_country} • {course.field_of_study}
              </p>

              <div className="flex items-center justify-between mb-4">
                <span className="text-gray-600 dark:text-gray-300 text-sm">
                  {course.duration_display}
                </span>
                {course.is_online && (
                  <span className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-2 py-1 rounded text-xs">
                    Online
                  </span>
                )}
              </div>

              <div className="flex items-center justify-between mb-4">
                <span className="text-lg font-bold text-gray-900 dark:text-white">
                  {course.currency} {course.tuition_fee.toLocaleString()}
                </span>
                {course.average_rating && (
                  <div className="flex items-center">
                    <span className="text-yellow-500">★</span>
                    <span className="text-gray-600 dark:text-gray-300 text-sm ml-1">
                      {course.average_rating}
                    </span>
                  </div>
                )}
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
      )}

      {/* Empty State */}
      {coursesData && coursesData.data.results.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <MagnifyingGlassIcon className="h-12 w-12 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No courses found
          </h3>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            Try adjusting your search criteria or filters
          </p>
          <button
            onClick={clearFilters}
            className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md"
          >
            Clear Filters
          </button>
        </div>
      )}
    </div>
  );
};

export default CoursesPage;