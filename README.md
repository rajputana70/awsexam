# AWS Solution Architect SAA-C03 Exam Simulator

A web-based platform for simulating the AWS Solutions Architect Associate (SAA-C03) certification exam. This application is designed to provide a realistic exam environment to help candidates prepare for the actual certification test.

## Features

- **User Authentication System**
  - Registration and login functionality
  - Profile management with password reset capabilities
  - Role-based access (admin/regular users)

- **Exam Simulation**
  - Timed exams that replicate the actual AWS exam format
  - Question navigation with mark for review functionality
  - Automatic submission when time expires

- **Results Analysis**
  - Detailed score reports after exam completion
  - Category-based performance analysis
  - Explanation for correct answers
  - Visual charts for performance tracking

- **Admin Dashboard**
  - Question and exam management
  - User administration
  - Category organization
  - Performance statistics

- **Progress Tracking**
  - Personal analytics dashboard
  - Performance trends over time
  - Category strength and weakness identification

## Technical Requirements

- Python 3.11+
- PostgreSQL database
- Dependencies:
  - email-validator>=2.2.0
  - flask-login>=0.6.3
  - flask>=3.1.0
  - flask-sqlalchemy>=3.1.1
  - flask-wtf>=1.2.2
  - gunicorn>=23.0.0
  - psycopg2-binary>=2.9.10
  - sqlalchemy>=2.0.40
  - werkzeug>=3.1.3
  - wtforms>=3.2.1

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r project_requirements.txt
   ```
3. Configure environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: Secret key for Flask session encryption
   - `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`: PostgreSQL connection details

4. Initialize the database:
   ```
   python
   >>> from app import db
   >>> db.create_all()
   ```

5. Run the application:
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## Database Schema

The application uses the following database models:
- User
- Question
- QuestionCategory 
- QuestionOption
- Exam
- ExamQuestion
- ExamAttempt
- UserAnswer

## Usage

Once the application is running, users can:
1. Register for an account
2. Log in to access exams
3. Take practice exams with a timer
4. Review results and analytics
5. Track progress over time

Administrators can:
1. Manage questions and add explanations
2. Create and configure exams
3. Organize questions by categories
4. Monitor user performance statistics