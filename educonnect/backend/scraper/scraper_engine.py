import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from decimal import Decimal
from django.utils import timezone

from .models import ScrapingJob, ScrapingRule, ScrapedData
from courses.models import University, Course


class UniversityScraper:
    def __init__(self, university, scraping_rule):
        self.university = university
        self.rule = scraping_rule
        self.session = requests.Session()
        self.driver = None
        
        # Set up custom headers
        if scraping_rule.custom_headers:
            self.session.headers.update(scraping_rule.custom_headers)
        else:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })

    def setup_selenium(self):
        """Set up Selenium WebDriver if needed"""
        if self.rule.use_selenium:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(options=chrome_options)

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
        self.session.close()

    def scrape_courses(self):
        """Main method to scrape courses from university website"""
        job = ScrapingJob.objects.create(
            university=self.university,
            status='running',
            started_at=timezone.now()
        )
        
        try:
            self.setup_selenium()
            
            if self.rule.use_selenium:
                courses_data = self._scrape_with_selenium()
            else:
                courses_data = self._scrape_with_requests()
            
            # Process scraped data
            courses_created = 0
            courses_updated = 0
            
            for course_data in courses_data:
                try:
                    course, created = self._process_course_data(course_data, job)
                    if created:
                        courses_created += 1
                    else:
                        courses_updated += 1
                except Exception as e:
                    # Log individual course processing errors
                    ScrapedData.objects.create(
                        scraping_job=job,
                        source_url=course_data.get('url', ''),
                        raw_data=course_data,
                        processed=False,
                        error_message=str(e)
                    )
            
            # Update job status
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.courses_found = len(courses_data)
            job.courses_created = courses_created
            job.courses_updated = courses_updated
            job.save()
            
            return job
        
        except Exception as e:
            job.status = 'failed'
            job.completed_at = timezone.now()
            job.error_message = str(e)
            job.save()
            raise e
        
        finally:
            self.cleanup()

    def _scrape_with_requests(self):
        """Scrape using requests and BeautifulSoup"""
        courses_data = []
        
        try:
            response = self.session.get(self.rule.base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            course_elements = soup.select(self.rule.course_list_selector)
            
            for element in course_elements:
                course_data = self._extract_course_data(element, soup)
                if course_data:
                    courses_data.append(course_data)
                
                # Respect rate limiting
                time.sleep(self.rule.wait_time)
        
        except Exception as e:
            raise Exception(f"Failed to scrape with requests: {str(e)}")
        
        return courses_data

    def _scrape_with_selenium(self):
        """Scrape using Selenium for JavaScript-heavy sites"""
        courses_data = []
        
        try:
            self.driver.get(self.rule.base_url)
            
            # Wait for course list to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.rule.course_list_selector))
            )
            
            course_elements = self.driver.find_elements(By.CSS_SELECTOR, self.rule.course_list_selector)
            
            for element in course_elements:
                course_data = self._extract_course_data_selenium(element)
                if course_data:
                    courses_data.append(course_data)
                
                # Respect rate limiting
                time.sleep(self.rule.wait_time)
        
        except Exception as e:
            raise Exception(f"Failed to scrape with Selenium: {str(e)}")
        
        return courses_data

    def _extract_course_data(self, element, soup):
        """Extract course data from HTML element using BeautifulSoup"""
        try:
            course_data = {
                'url': self.rule.base_url
            }
            
            # Extract title
            if self.rule.course_title_selector:
                title_elem = element.select_one(self.rule.course_title_selector)
                if title_elem:
                    course_data['title'] = title_elem.get_text(strip=True)
            
            # Extract fee
            if self.rule.course_fee_selector:
                fee_elem = element.select_one(self.rule.course_fee_selector)
                if fee_elem:
                    fee_text = fee_elem.get_text(strip=True)
                    course_data['fee'] = self._extract_fee(fee_text)
            
            # Extract duration
            if self.rule.course_duration_selector:
                duration_elem = element.select_one(self.rule.course_duration_selector)
                if duration_elem:
                    duration_text = duration_elem.get_text(strip=True)
                    course_data['duration'] = self._extract_duration(duration_text)
            
            # Extract level
            if self.rule.course_level_selector:
                level_elem = element.select_one(self.rule.course_level_selector)
                if level_elem:
                    level_text = level_elem.get_text(strip=True)
                    course_data['level'] = self._extract_level(level_text)
            
            # Extract description
            if self.rule.course_description_selector:
                desc_elem = element.select_one(self.rule.course_description_selector)
                if desc_elem:
                    course_data['description'] = desc_elem.get_text(strip=True)
            
            return course_data if course_data.get('title') else None
        
        except Exception as e:
            return None

    def _extract_course_data_selenium(self, element):
        """Extract course data using Selenium WebElement"""
        try:
            course_data = {
                'url': self.driver.current_url
            }
            
            # Extract title
            if self.rule.course_title_selector:
                try:
                    title_elem = element.find_element(By.CSS_SELECTOR, self.rule.course_title_selector)
                    course_data['title'] = title_elem.text.strip()
                except:
                    pass
            
            # Extract fee
            if self.rule.course_fee_selector:
                try:
                    fee_elem = element.find_element(By.CSS_SELECTOR, self.rule.course_fee_selector)
                    fee_text = fee_elem.text.strip()
                    course_data['fee'] = self._extract_fee(fee_text)
                except:
                    pass
            
            # Extract duration
            if self.rule.course_duration_selector:
                try:
                    duration_elem = element.find_element(By.CSS_SELECTOR, self.rule.course_duration_selector)
                    duration_text = duration_elem.text.strip()
                    course_data['duration'] = self._extract_duration(duration_text)
                except:
                    pass
            
            return course_data if course_data.get('title') else None
        
        except Exception as e:
            return None

    def _extract_fee(self, fee_text):
        """Extract numerical fee from text"""
        try:
            # Remove currency symbols and extract numbers
            fee_numbers = re.findall(r'[\d,]+\.?\d*', fee_text.replace(',', ''))
            if fee_numbers:
                return float(fee_numbers[0])
        except:
            pass
        return None

    def _extract_duration(self, duration_text):
        """Extract duration information from text"""
        try:
            # Look for patterns like "2 years", "18 months", etc.
            duration_match = re.search(r'(\d+)\s*(year|month|week)', duration_text.lower())
            if duration_match:
                value = int(duration_match.group(1))
                unit = duration_match.group(2) + 's'  # Make plural
                return {'value': value, 'unit': unit}
        except:
            pass
        return None

    def _extract_level(self, level_text):
        """Extract course level from text"""
        level_text_lower = level_text.lower()
        
        if 'bachelor' in level_text_lower or 'undergraduate' in level_text_lower:
            return 'bachelor'
        elif 'master' in level_text_lower or 'postgraduate' in level_text_lower:
            return 'master'
        elif 'phd' in level_text_lower or 'doctorate' in level_text_lower:
            return 'phd'
        elif 'diploma' in level_text_lower:
            return 'diploma'
        elif 'certificate' in level_text_lower:
            return 'certificate'
        
        return 'bachelor'  # Default

    def _process_course_data(self, course_data, job):
        """Process scraped course data and create/update Course object"""
        if not course_data.get('title'):
            raise ValueError("Course title is required")
        
        # Create ScrapedData record
        scraped_data = ScrapedData.objects.create(
            scraping_job=job,
            source_url=course_data.get('url', ''),
            raw_data=course_data
        )
        
        try:
            # Check if course already exists
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                university=self.university,
                defaults={
                    'level': course_data.get('level', 'bachelor'),
                    'field_of_study': self._determine_field_of_study(course_data['title']),
                    'description': course_data.get('description', ''),
                    'duration_value': course_data.get('duration', {}).get('value', 1),
                    'duration_unit': course_data.get('duration', {}).get('unit', 'years'),
                    'tuition_fee': course_data.get('fee', 0),
                    'currency': 'USD',  # Default, should be configurable
                    'course_url': course_data.get('url', ''),
                }
            )
            
            if not created:
                # Update existing course
                if course_data.get('fee'):
                    course.tuition_fee = course_data['fee']
                if course_data.get('description'):
                    course.description = course_data['description']
                course.save()
            
            # Link scraped data to course
            scraped_data.course = course
            scraped_data.processed = True
            scraped_data.save()
            
            return course, created
        
        except Exception as e:
            scraped_data.error_message = str(e)
            scraped_data.save()
            raise e

    def _determine_field_of_study(self, title):
        """Determine field of study from course title"""
        title_lower = title.lower()
        
        field_keywords = {
            'Computer Science': ['computer', 'software', 'programming', 'data science', 'ai', 'machine learning'],
            'Engineering': ['engineering', 'mechanical', 'electrical', 'civil', 'chemical'],
            'Business': ['business', 'management', 'mba', 'finance', 'marketing', 'economics'],
            'Medicine': ['medicine', 'medical', 'health', 'nursing', 'pharmacy'],
            'Law': ['law', 'legal', 'jurisprudence'],
            'Arts': ['arts', 'design', 'creative', 'music', 'literature'],
            'Science': ['biology', 'chemistry', 'physics', 'mathematics'],
            'Education': ['education', 'teaching', 'pedagogy'],
        }
        
        for field, keywords in field_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                return field
        
        return 'General Studies'  # Default


def run_scraping_job(university_id):
    """Run scraping job for a specific university"""
    try:
        university = University.objects.get(id=university_id)
        scraping_rule = university.scraping_rule
        
        scraper = UniversityScraper(university, scraping_rule)
        job = scraper.scrape_courses()
        
        return job
    
    except University.DoesNotExist:
        raise Exception(f"University with ID {university_id} not found")
    
    except Exception as e:
        raise Exception(f"Scraping job failed: {str(e)}")


def run_all_scraping_jobs():
    """Run scraping jobs for all universities with active scraping rules"""
    universities = University.objects.filter(
        is_active=True,
        scraping_rule__is_active=True
    )
    
    results = []
    
    for university in universities:
        try:
            job = run_scraping_job(university.id)
            results.append({
                'university': university.name,
                'status': job.status,
                'courses_found': job.courses_found,
                'courses_created': job.courses_created,
                'courses_updated': job.courses_updated
            })
        except Exception as e:
            results.append({
                'university': university.name,
                'status': 'failed',
                'error': str(e)
            })
    
    return results