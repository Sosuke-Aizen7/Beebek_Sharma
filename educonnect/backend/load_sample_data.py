#!/usr/bin/env python
"""
Script to load sample data for EduConnect platform
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educonnect_backend.settings')
django.setup()

from courses.models import University, Course, UniversityContact
from users.models import User


def create_sample_universities():
    """Create sample universities"""
    universities_data = [
        {
            'name': 'Harvard University',
            'country': 'USA',
            'city': 'Cambridge',
            'website': 'https://www.harvard.edu',
            'description': 'Harvard University is a private Ivy League research university in Cambridge, Massachusetts.',
            'ranking_global': 1,
            'ranking_national': 1,
            'established_year': 1636,
            'student_population': 23000,
            'acceptance_rate': Decimal('5.2'),
            'contact_email': 'admissions@harvard.edu',
            'address': 'Cambridge, MA 02138, USA'
        },
        {
            'name': 'Stanford University',
            'country': 'USA',
            'city': 'Stanford',
            'website': 'https://www.stanford.edu',
            'description': 'Stanford University is a private research university in Stanford, California.',
            'ranking_global': 2,
            'ranking_national': 2,
            'established_year': 1885,
            'student_population': 17000,
            'acceptance_rate': Decimal('4.3'),
            'contact_email': 'admission@stanford.edu',
            'address': 'Stanford, CA 94305, USA'
        },
        {
            'name': 'University of Oxford',
            'country': 'UK',
            'city': 'Oxford',
            'website': 'https://www.ox.ac.uk',
            'description': 'The University of Oxford is a collegiate research university in Oxford, England.',
            'ranking_global': 3,
            'ranking_national': 1,
            'established_year': 1096,
            'student_population': 24000,
            'acceptance_rate': Decimal('17.5'),
            'contact_email': 'admissions@ox.ac.uk',
            'address': 'Oxford OX1 2JD, UK'
        },
        {
            'name': 'Technical University of Munich',
            'country': 'Germany',
            'city': 'Munich',
            'website': 'https://www.tum.de',
            'description': 'The Technical University of Munich is a public research university in Munich, Germany.',
            'ranking_global': 50,
            'ranking_national': 1,
            'established_year': 1868,
            'student_population': 45000,
            'acceptance_rate': Decimal('8.0'),
            'contact_email': 'studium@tum.de',
            'address': 'Arcisstraße 21, 80333 München, Germany'
        },
        {
            'name': 'University of Toronto',
            'country': 'Canada',
            'city': 'Toronto',
            'website': 'https://www.utoronto.ca',
            'description': 'The University of Toronto is a public research university in Toronto, Ontario, Canada.',
            'ranking_global': 25,
            'ranking_national': 1,
            'established_year': 1827,
            'student_population': 97000,
            'acceptance_rate': Decimal('43.0'),
            'contact_email': 'admissions@utoronto.ca',
            'address': '27 King\'s College Cir, Toronto, ON M5S 1A1, Canada'
        }
    ]
    
    created_universities = []
    for uni_data in universities_data:
        university, created = University.objects.get_or_create(
            name=uni_data['name'],
            defaults=uni_data
        )
        created_universities.append(university)
        if created:
            print(f"Created university: {university.name}")
        else:
            print(f"University already exists: {university.name}")
    
    return created_universities


def create_sample_courses(universities):
    """Create sample courses for universities"""
    courses_data = [
        # Harvard courses
        {
            'university': universities[0],  # Harvard
            'title': 'Master of Science in Computer Science',
            'level': 'master',
            'field_of_study': 'Computer Science',
            'description': 'Advanced computer science program focusing on algorithms, machine learning, and software engineering.',
            'duration_value': 2,
            'duration_unit': 'years',
            'tuition_fee': Decimal('54880'),
            'currency': 'USD',
            'admission_requirements': 'Bachelor\'s degree in CS or related field, GRE scores, letters of recommendation',
            'gpa_requirement': Decimal('3.7'),
            'popularity_score': 95
        },
        {
            'university': universities[0],  # Harvard
            'title': 'Bachelor of Arts in Economics',
            'level': 'bachelor',
            'field_of_study': 'Economics',
            'description': 'Comprehensive economics program with focus on theory and practical applications.',
            'duration_value': 4,
            'duration_unit': 'years',
            'tuition_fee': Decimal('51925'),
            'currency': 'USD',
            'admission_requirements': 'High school diploma, SAT/ACT scores, essays, recommendations',
            'gpa_requirement': Decimal('3.9'),
            'popularity_score': 88
        },
        # Stanford courses
        {
            'university': universities[1],  # Stanford
            'title': 'Master of Business Administration (MBA)',
            'level': 'master',
            'field_of_study': 'Business',
            'description': 'Two-year full-time MBA program with emphasis on innovation and leadership.',
            'duration_value': 2,
            'duration_unit': 'years',
            'tuition_fee': Decimal('77868'),
            'currency': 'USD',
            'admission_requirements': 'Bachelor\'s degree, GMAT/GRE, work experience, essays',
            'gpa_requirement': Decimal('3.8'),
            'popularity_score': 92
        },
        {
            'university': universities[1],  # Stanford
            'title': 'Bachelor of Science in Engineering',
            'level': 'bachelor',
            'field_of_study': 'Engineering',
            'description': 'Interdisciplinary engineering program with various specialization tracks.',
            'duration_value': 4,
            'duration_unit': 'years',
            'tuition_fee': Decimal('56169'),
            'currency': 'USD',
            'admission_requirements': 'High school diploma with strong math and science background',
            'gpa_requirement': Decimal('3.8'),
            'popularity_score': 85
        },
        # Oxford courses
        {
            'university': universities[2],  # Oxford
            'title': 'Doctor of Philosophy in History',
            'level': 'phd',
            'field_of_study': 'History',
            'description': 'Research-intensive PhD program in various historical periods and methodologies.',
            'duration_value': 3,
            'duration_unit': 'years',
            'tuition_fee': Decimal('28040'),
            'currency': 'GBP',
            'admission_requirements': 'Master\'s degree in History or related field, research proposal',
            'gpa_requirement': Decimal('3.7'),
            'popularity_score': 78
        },
        {
            'university': universities[2],  # Oxford
            'title': 'Bachelor of Arts in Philosophy, Politics and Economics',
            'level': 'bachelor',
            'field_of_study': 'Liberal Arts',
            'description': 'Interdisciplinary program combining philosophy, politics, and economics.',
            'duration_value': 3,
            'duration_unit': 'years',
            'tuition_fee': Decimal('28370'),
            'currency': 'GBP',
            'admission_requirements': 'A-levels AAA, personal statement, interview',
            'gpa_requirement': Decimal('3.9'),
            'popularity_score': 90
        },
        # TUM courses
        {
            'university': universities[3],  # TUM
            'title': 'Master of Science in Data Engineering and Analytics',
            'level': 'master',
            'field_of_study': 'Data Science',
            'description': 'Advanced program focusing on big data, machine learning, and analytics.',
            'duration_value': 2,
            'duration_unit': 'years',
            'tuition_fee': Decimal('150'),
            'currency': 'EUR',
            'admission_requirements': 'Bachelor\'s in CS, Mathematics, or Engineering with good grades',
            'gpa_requirement': Decimal('3.0'),
            'popularity_score': 82
        },
        {
            'university': universities[3],  # TUM
            'title': 'Bachelor of Science in Mechanical Engineering',
            'level': 'bachelor',
            'field_of_study': 'Engineering',
            'description': 'Comprehensive mechanical engineering program with hands-on experience.',
            'duration_value': 3,
            'duration_unit': 'years',
            'tuition_fee': Decimal('150'),
            'currency': 'EUR',
            'admission_requirements': 'Abitur or equivalent, German language proficiency',
            'gpa_requirement': Decimal('2.5'),
            'popularity_score': 75
        },
        # University of Toronto courses
        {
            'university': universities[4],  # UofT
            'title': 'Master of Applied Science in Biomedical Engineering',
            'level': 'master',
            'field_of_study': 'Biomedical Engineering',
            'description': 'Research-focused program in biomedical engineering and medical technology.',
            'duration_value': 2,
            'duration_unit': 'years',
            'tuition_fee': Decimal('58160'),
            'currency': 'CAD',
            'admission_requirements': 'Bachelor\'s in Engineering or related field, research experience',
            'gpa_requirement': Decimal('3.3'),
            'popularity_score': 80
        },
        {
            'university': universities[4],  # UofT
            'title': 'Bachelor of Commerce',
            'level': 'bachelor',
            'field_of_study': 'Business',
            'description': 'Comprehensive business program with various specialization options.',
            'duration_value': 4,
            'duration_unit': 'years',
            'tuition_fee': Decimal('61690'),
            'currency': 'CAD',
            'admission_requirements': 'High school diploma, strong academic record, extracurriculars',
            'gpa_requirement': Decimal('3.5'),
            'popularity_score': 77
        }
    ]
    
    created_courses = []
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            title=course_data['title'],
            university=course_data['university'],
            defaults=course_data
        )
        created_courses.append(course)
        if created:
            print(f"Created course: {course.title} at {course.university.name}")
        else:
            print(f"Course already exists: {course.title}")
    
    return created_courses


def create_admin_user():
    """Create admin user"""
    try:
        admin_user, created = User.objects.get_or_create(
            email='admin@educonnect.com',
            defaults={
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'is_email_verified': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print("Created admin user: admin@educonnect.com / admin123")
        else:
            print("Admin user already exists")
        
        return admin_user
    except Exception as e:
        print(f"Error creating admin user: {e}")


def main():
    """Main function to load all sample data"""
    print("Loading sample data for EduConnect...")
    
    try:
        # Create admin user
        create_admin_user()
        
        # Create universities
        universities = create_sample_universities()
        
        # Create courses
        courses = create_sample_courses(universities)
        
        print(f"\nSample data loaded successfully!")
        print(f"Created {len(universities)} universities")
        print(f"Created {len(courses)} courses")
        print("\nYou can now:")
        print("1. Access admin panel at http://localhost:8000/admin/")
        print("2. Login with: admin@educonnect.com / admin123")
        print("3. Start the React frontend and explore the platform")
        
    except Exception as e:
        print(f"Error loading sample data: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()