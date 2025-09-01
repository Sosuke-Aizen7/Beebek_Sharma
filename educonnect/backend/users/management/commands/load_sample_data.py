from django.core.management.base import BaseCommand
from decimal import Decimal
from courses.models import University, Course
from users.models import User


class Command(BaseCommand):
    help = 'Load sample data for EduConnect platform'

    def handle(self, *args, **options):
        self.stdout.write("Loading sample data for EduConnect...")
        
        # Create admin user
        self.create_admin_user()
        
        # Create universities
        universities = self.create_sample_universities()
        
        # Create courses
        courses = self.create_sample_courses(universities)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded sample data!')
        )
        self.stdout.write(f'Created {len(universities)} universities')
        self.stdout.write(f'Created {len(courses)} courses')
        self.stdout.write('\nAdmin login: admin@educonnect.com / admin123')

    def create_admin_user(self):
        """Create admin user"""
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
            self.stdout.write("Created admin user")
        else:
            self.stdout.write("Admin user already exists")

    def create_sample_universities(self):
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
                self.stdout.write(f"Created university: {university.name}")
        
        return created_universities

    def create_sample_courses(self, universities):
        """Create sample courses"""
        courses_data = [
            # Harvard courses
            {
                'university': universities[0],
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
                'university': universities[1],
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
            # Add more sample courses...
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
                self.stdout.write(f"Created course: {course.title}")
        
        return created_courses