import os
import math
import random
from datetime import datetime, timedelta
from flask import (
    render_template, redirect, url_for, flash, 
    request, jsonify, session, abort
)
from flask_login import (
    login_user, logout_user, current_user, 
    login_required
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import func

from app import app, db
from models import (
    User, Question, QuestionOption, QuestionCategory,
    Exam, ExamQuestion, ExamAttempt, UserAnswer
)
from forms import (
    LoginForm, RegistrationForm, QuestionForm, OptionForm,
    ExamForm, UserAnswerForm, CategoryForm, ProfileForm
)

# Home/Landing page
@app.route('/')
def index():
    return render_template('index.html', title='AWS Solution Architect Exam Simulator')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# User dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's exam attempts
    attempts = ExamAttempt.query.filter_by(user_id=current_user.id).order_by(ExamAttempt.start_time.desc()).all()
    
    # Get available exams for the user
    available_exams = Exam.query.filter_by(is_active=True).all()
    
    # Calculate user stats
    total_attempts = len(attempts)
    passed_attempts = sum(1 for a in attempts if a.is_passed)
    pass_rate = (passed_attempts / total_attempts * 100) if total_attempts > 0 else 0
    
    # Get the latest attempt
    latest_attempt = attempts[0] if attempts else None
    
    return render_template(
        'dashboard.html', 
        title='Dashboard',
        attempts=attempts,
        available_exams=available_exams,
        total_attempts=total_attempts,
        passed_attempts=passed_attempts,
        pass_rate=pass_rate,
        latest_attempt=latest_attempt
    )

# Exam instructions before starting
@app.route('/exam/<int:exam_id>/instructions')
@login_required
def exam_instructions(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    
    # Check if user has an in-progress attempt for this exam
    in_progress_attempt = ExamAttempt.query.filter_by(
        user_id=current_user.id,
        exam_id=exam.id,
        is_completed=False
    ).first()
    
    if in_progress_attempt:
        # Redirect to continue the in-progress exam
        return redirect(url_for('take_exam', attempt_id=in_progress_attempt.id))
    
    return render_template('exam_instructions.html', title='Exam Instructions', exam=exam)

# Start a new exam
@app.route('/exam/<int:exam_id>/start')
@login_required
def start_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    
    # Check if user has an in-progress attempt for this exam
    in_progress_attempt = ExamAttempt.query.filter_by(
        user_id=current_user.id,
        exam_id=exam.id,
        is_completed=False
    ).first()
    
    if in_progress_attempt:
        # Redirect to continue the in-progress exam
        return redirect(url_for('take_exam', attempt_id=in_progress_attempt.id))
    
    # Create a new exam attempt
    attempt = ExamAttempt(
        user_id=current_user.id,
        exam_id=exam.id,
        start_time=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.flush()  # Get the ID without committing
    
    # Get all questions for this exam
    exam_questions = ExamQuestion.query.filter_by(exam_id=exam.id).order_by(ExamQuestion.order).all()
    
    # Create user answer entries for each question
    for exam_question in exam_questions:
        user_answer = UserAnswer(
            attempt_id=attempt.id,
            question_id=exam_question.question_id,
            is_marked_for_review=False
        )
        db.session.add(user_answer)
    
    db.session.commit()
    
    return redirect(url_for('take_exam', attempt_id=attempt.id))

# Take the exam
@app.route('/exam/attempt/<int:attempt_id>', methods=['GET', 'POST'])
@login_required
def take_exam(attempt_id):
    # Get the attempt and verify it belongs to the current user
    attempt = ExamAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id:
        abort(403)  # Forbidden
    
    if attempt.is_completed:
        # If the exam is already completed, redirect to results
        return redirect(url_for('exam_results', attempt_id=attempt.id))
    
    # Get the exam information
    exam = attempt.exam
    
    # Calculate remaining time
    end_time = attempt.start_time + timedelta(minutes=exam.duration_minutes)
    remaining_seconds = int((end_time - datetime.utcnow()).total_seconds())
    
    # If time is up, auto-submit the exam
    if remaining_seconds <= 0:
        return redirect(url_for('finish_exam', attempt_id=attempt.id))
    
    # Get all user answers for this attempt
    user_answers = UserAnswer.query.filter_by(attempt_id=attempt.id).all()
    
    # Get the current question index from query parameters
    current_idx = request.args.get('q', 1, type=int) - 1
    total_questions = len(user_answers)
    
    # Ensure the question index is valid
    if current_idx < 0 or current_idx >= total_questions:
        current_idx = 0
    
    # Get the current question
    current_answer = user_answers[current_idx]
    current_question = current_answer.question
    
    # Create the form
    form = UserAnswerForm(obj=current_answer)
    form.question_id.data = current_question.id
    form.selected_option.choices = [(option.id, option.option_text) for option in current_question.options]
    
    # Process form submission
    if form.validate_on_submit():
        # Save the current answer
        current_answer.selected_option_id = form.selected_option.data
        current_answer.is_marked_for_review = form.is_marked.data
        db.session.commit()
        
        # Determine where to go next
        if form.finish.data:
            return redirect(url_for('finish_exam', attempt_id=attempt.id))
        elif form.previous.data and current_idx > 0:
            return redirect(url_for('take_exam', attempt_id=attempt.id, q=current_idx))
        elif form.next.data and current_idx < total_questions - 1:
            return redirect(url_for('take_exam', attempt_id=attempt.id, q=current_idx + 2))
        else:
            # Stay on the same question
            return redirect(url_for('take_exam', attempt_id=attempt.id, q=current_idx + 1))
    
    # If there's a selected option, set it in the form
    if current_answer.selected_option_id:
        form.selected_option.data = current_answer.selected_option_id
    
    # Set the marked for review checkbox
    form.is_marked.data = current_answer.is_marked_for_review
    
    # Prepare question navigation info
    nav_info = []
    for i, answer in enumerate(user_answers):
        status = 'unanswered'
        if answer.selected_option_id:
            status = 'answered'
        if answer.is_marked_for_review:
            status = 'marked'
        
        nav_info.append({
            'index': i + 1,
            'status': status,
            'is_current': i == current_idx
        })
    
    return render_template(
        'exam.html',
        title='AWS Solution Architect Exam',
        form=form,
        attempt=attempt,
        exam=exam,
        question=current_question,
        current_idx=current_idx,
        total_questions=total_questions,
        nav_info=nav_info,
        remaining_seconds=remaining_seconds
    )

# Finish the exam and calculate results
@app.route('/exam/attempt/<int:attempt_id>/finish')
@login_required
def finish_exam(attempt_id):
    # Get the attempt and verify it belongs to the current user
    attempt = ExamAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id:
        abort(403)  # Forbidden
    
    # If the exam is already completed, redirect to results
    if attempt.is_completed:
        return redirect(url_for('exam_results', attempt_id=attempt.id))
    
    # Mark the attempt as completed
    attempt.is_completed = True
    attempt.end_time = datetime.utcnow()
    
    # Calculate the score
    total_questions = 0
    correct_answers = 0
    
    # Get all user answers for this attempt
    user_answers = UserAnswer.query.filter_by(attempt_id=attempt.id).all()
    
    for answer in user_answers:
        total_questions += 1
        
        # Get the correct option for this question
        correct_option = QuestionOption.query.filter_by(
            question_id=answer.question_id,
            is_correct=True
        ).first()
        
        if correct_option and answer.selected_option_id == correct_option.id:
            answer.is_correct = True
            correct_answers += 1
        else:
            answer.is_correct = False
    
    # Calculate score as a percentage
    if total_questions > 0:
        attempt.score = (correct_answers / total_questions) * 100
    else:
        attempt.score = 0
    
    # Determine if the user passed the exam
    attempt.is_passed = attempt.score >= attempt.exam.pass_percentage
    
    db.session.commit()
    
    return redirect(url_for('exam_results', attempt_id=attempt.id))

# View exam results
@app.route('/exam/attempt/<int:attempt_id>/results')
@login_required
def exam_results(attempt_id):
    # Get the attempt and verify it belongs to the current user
    attempt = ExamAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id and not current_user.is_admin:
        abort(403)  # Forbidden
    
    # If the exam is not completed yet, redirect to take the exam
    if not attempt.is_completed:
        return redirect(url_for('take_exam', attempt_id=attempt.id))
    
    # Get all user answers for this attempt
    user_answers = UserAnswer.query.filter_by(attempt_id=attempt.id).all()
    
    # Calculate stats for each category
    categories = {}
    for answer in user_answers:
        question = answer.question
        if question.category:
            category_name = question.category.name
            if category_name not in categories:
                categories[category_name] = {'total': 0, 'correct': 0}
            
            categories[category_name]['total'] += 1
            if answer.is_correct:
                categories[category_name]['correct'] += 1
    
    # Calculate percentages for categories
    for category in categories.values():
        category['percentage'] = (category['correct'] / category['total']) * 100 if category['total'] > 0 else 0
    
    return render_template(
        'results.html',
        title='Exam Results',
        attempt=attempt,
        exam=attempt.exam,
        user_answers=user_answers,
        categories=categories
    )

# Review completed exam
@app.route('/exam/attempt/<int:attempt_id>/review')
@login_required
def exam_review(attempt_id):
    # Get the attempt and verify it belongs to the current user
    attempt = ExamAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id and not current_user.is_admin:
        abort(403)  # Forbidden
    
    # If the exam is not completed yet, redirect to take the exam
    if not attempt.is_completed:
        return redirect(url_for('take_exam', attempt_id=attempt.id))
    
    # Get all user answers for this attempt
    user_answers = UserAnswer.query.filter_by(attempt_id=attempt.id).all()
    
    # Get the current question index from query parameters
    current_idx = request.args.get('q', 1, type=int) - 1
    total_questions = len(user_answers)
    
    # Ensure the question index is valid
    if current_idx < 0 or current_idx >= total_questions:
        current_idx = 0
    
    # Get the current question and answer
    current_answer = user_answers[current_idx]
    current_question = current_answer.question
    
    # Get all options for the current question
    options = current_question.options
    
    # Determine the correct option
    correct_option = next((o for o in options if o.is_correct), None)
    
    return render_template(
        'exam_review.html',
        title='Exam Review',
        attempt=attempt,
        exam=attempt.exam,
        question=current_question,
        answer=current_answer,
        options=options,
        correct_option=correct_option,
        current_idx=current_idx,
        total_questions=total_questions,
        user_answers=user_answers
    )

# User profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(current_user.username, current_user.email)
    
    if form.validate_on_submit():
        # Update user profile
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        # Change password if provided
        if form.current_password.data:
            # Verify current password
            if check_password_hash(current_user.password_hash, form.current_password.data):
                if form.new_password.data:
                    current_user.password_hash = generate_password_hash(form.new_password.data)
            else:
                flash('Current password is incorrect.', 'danger')
                return render_template('profile.html', title='Profile', form=form)
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    # Get user's exam statistics
    attempts = ExamAttempt.query.filter_by(user_id=current_user.id).all()
    total_attempts = len(attempts)
    completed_attempts = sum(1 for a in attempts if a.is_completed)
    passed_attempts = sum(1 for a in attempts if a.is_passed)
    
    pass_rate = (passed_attempts / completed_attempts * 100) if completed_attempts > 0 else 0
    
    # Get latest exam scores
    latest_scores = ExamAttempt.query.filter_by(
        user_id=current_user.id,
        is_completed=True
    ).order_by(ExamAttempt.end_time.desc()).limit(5).all()
    
    return render_template(
        'profile.html',
        title='Profile',
        form=form,
        total_attempts=total_attempts,
        completed_attempts=completed_attempts,
        passed_attempts=passed_attempts,
        pass_rate=pass_rate,
        latest_scores=latest_scores
    )

# User performance analytics
@app.route('/analytics')
@login_required
def analytics():
    # Get all completed exams for the current user
    attempts = ExamAttempt.query.filter_by(
        user_id=current_user.id,
        is_completed=True
    ).order_by(ExamAttempt.end_time).all()
    
    # Prepare data for charts
    score_data = {
        'labels': [attempt.end_time.strftime('%Y-%m-%d %H:%M') for attempt in attempts],
        'scores': [attempt.score for attempt in attempts],
        'pass_marks': [attempt.exam.pass_percentage for attempt in attempts]
    }
    
    # Get category performance data
    category_data = {}
    for attempt in attempts:
        for answer in attempt.answers:
            question = answer.question
            if question.category:
                category_name = question.category.name
                if category_name not in category_data:
                    category_data[category_name] = {'total': 0, 'correct': 0}
                
                category_data[category_name]['total'] += 1
                if answer.is_correct:
                    category_data[category_name]['correct'] += 1
    
    # Calculate percentages for categories
    category_percentages = {}
    for category, counts in category_data.items():
        percentage = (counts['correct'] / counts['total'] * 100) if counts['total'] > 0 else 0
        category_percentages[category] = round(percentage, 1)
    
    # Get time spent data
    time_spent_data = []
    for attempt in attempts:
        if attempt.start_time and attempt.end_time:
            duration = (attempt.end_time - attempt.start_time).total_seconds() / 60  # in minutes
            time_spent_data.append({
                'exam_title': attempt.exam.title,
                'date': attempt.end_time.strftime('%Y-%m-%d %H:%M'),
                'duration': round(duration, 1),
                'allocated_time': attempt.exam.duration_minutes
            })
    
    return render_template(
        'analytics.html',
        title='Performance Analytics',
        score_data=score_data,
        category_percentages=category_percentages,
        time_spent_data=time_spent_data
    )

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    # Get counts for dashboard
    user_count = User.query.count()
    exam_count = Exam.query.count()
    question_count = Question.query.count()
    attempt_count = ExamAttempt.query.count()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Get recent exam attempts
    recent_attempts = ExamAttempt.query.order_by(ExamAttempt.start_time.desc()).limit(10).all()
    
    # Get pass rate stats
    completed_attempts = ExamAttempt.query.filter_by(is_completed=True).count()
    passed_attempts = ExamAttempt.query.filter_by(is_passed=True).count()
    pass_rate = (passed_attempts / completed_attempts * 100) if completed_attempts > 0 else 0
    
    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard',
        user_count=user_count,
        exam_count=exam_count,
        question_count=question_count,
        attempt_count=attempt_count,
        recent_users=recent_users,
        recent_attempts=recent_attempts,
        pass_rate=pass_rate
    )

# Question management routes
@app.route('/admin/questions')
@login_required
def manage_questions():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    # Get query parameters for filtering
    category_id = request.args.get('category', type=int)
    difficulty = request.args.get('difficulty')
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    
    # Start with base query
    query = Question.query
    
    # Apply filters if provided
    if category_id:
        query = query.filter_by(category_id=category_id)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if search:
        query = query.filter(Question.question_text.ilike(f'%{search}%'))
    
    # Paginate the results
    questions = query.order_by(Question.id.desc()).paginate(page=page, per_page=10)
    
    # Get categories for the filter dropdown
    categories = QuestionCategory.query.all()
    
    return render_template(
        'admin/question_management.html',
        title='Manage Questions',
        questions=questions,
        categories=categories,
        current_category=category_id,
        current_difficulty=difficulty,
        search=search
    )

@app.route('/admin/questions/add', methods=['GET', 'POST'])
@login_required
def add_question():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    form = QuestionForm()
    
    # Populate category choices
    categories = QuestionCategory.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    form.category_id.choices.insert(0, (0, 'No Category'))
    
    if form.validate_on_submit():
        question = Question(
            question_text=form.question_text.data,
            explanation=form.explanation.data,
            difficulty=form.difficulty.data,
            category_id=form.category_id.data if form.category_id.data != 0 else None
        )
        db.session.add(question)
        db.session.commit()
        
        flash('Question has been added!', 'success')
        return redirect(url_for('edit_question', question_id=question.id))
    
    return render_template(
        'admin/question_management.html',
        title='Add Question',
        form=form,
        add_mode=True
    )

@app.route('/admin/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    question = Question.query.get_or_404(question_id)
    form = QuestionForm(obj=question)
    option_form = OptionForm()
    
    # Populate category choices
    categories = QuestionCategory.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    form.category_id.choices.insert(0, (0, 'No Category'))
    
    if form.validate_on_submit():
        question.question_text = form.question_text.data
        question.explanation = form.explanation.data
        question.difficulty = form.difficulty.data
        question.category_id = form.category_id.data if form.category_id.data != 0 else None
        question.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Question has been updated!', 'success')
        return redirect(url_for('edit_question', question_id=question.id))
    
    # If it's a GET request, set the category_id to 0 if it's None
    if request.method == 'GET':
        form.category_id.data = question.category_id or 0
    
    return render_template(
        'admin/question_management.html',
        title='Edit Question',
        form=form,
        option_form=option_form,
        question=question,
        edit_mode=True
    )

@app.route('/admin/questions/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    question = Question.query.get_or_404(question_id)
    
    # Check if the question is used in any exams
    exam_questions = ExamQuestion.query.filter_by(question_id=question.id).first()
    if exam_questions:
        flash('This question cannot be deleted because it is used in one or more exams.', 'danger')
        return redirect(url_for('edit_question', question_id=question.id))
    
    db.session.delete(question)
    db.session.commit()
    
    flash('Question has been deleted!', 'success')
    return redirect(url_for('manage_questions'))

@app.route('/admin/questions/<int:question_id>/options/add', methods=['POST'])
@login_required
def add_option(question_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    question = Question.query.get_or_404(question_id)
    form = OptionForm()
    
    if form.validate_on_submit():
        # If this is a correct option and there's already a correct one,
        # update the existing correct option to be incorrect
        if form.is_correct.data:
            existing_correct = QuestionOption.query.filter_by(
                question_id=question.id,
                is_correct=True
            ).first()
            
            if existing_correct:
                existing_correct.is_correct = False
        
        option = QuestionOption(
            question_id=question.id,
            option_text=form.option_text.data,
            is_correct=form.is_correct.data
        )
        
        db.session.add(option)
        db.session.commit()
        
        flash('Option has been added!', 'success')
    
    return redirect(url_for('edit_question', question_id=question.id))

@app.route('/admin/options/<int:option_id>/delete', methods=['POST'])
@login_required
def delete_option(option_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    option = QuestionOption.query.get_or_404(option_id)
    question_id = option.question_id
    
    db.session.delete(option)
    db.session.commit()
    
    flash('Option has been deleted!', 'success')
    return redirect(url_for('edit_question', question_id=question_id))

@app.route('/admin/options/<int:option_id>/set_correct', methods=['POST'])
@login_required
def set_correct_option(option_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    option = QuestionOption.query.get_or_404(option_id)
    question_id = option.question_id
    
    # Update all options for this question to be incorrect
    QuestionOption.query.filter_by(question_id=question_id).update({'is_correct': False})
    
    # Set this option as correct
    option.is_correct = True
    db.session.commit()
    
    flash('Correct answer has been updated!', 'success')
    return redirect(url_for('edit_question', question_id=question_id))

# Category management routes
@app.route('/admin/categories')
@login_required
def manage_categories():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    categories = QuestionCategory.query.all()
    form = CategoryForm()
    
    return render_template(
        'admin/question_management.html',
        title='Manage Categories',
        categories=categories,
        form=form,
        category_mode=True
    )

@app.route('/admin/categories/add', methods=['POST'])
@login_required
def add_category():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = QuestionCategory(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        
        flash('Category has been added!', 'success')
    
    return redirect(url_for('manage_categories'))

@app.route('/admin/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    category = QuestionCategory.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        
        db.session.commit()
        flash('Category has been updated!', 'success')
        return redirect(url_for('manage_categories'))
    
    categories = QuestionCategory.query.all()
    
    return render_template(
        'admin/question_management.html',
        title='Edit Category',
        categories=categories,
        form=form,
        edit_category=category,
        category_mode=True
    )

@app.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    category = QuestionCategory.query.get_or_404(category_id)
    
    # Check if the category has questions
    if category.questions:
        flash('This category cannot be deleted because it contains questions.', 'danger')
        return redirect(url_for('manage_categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Category has been deleted!', 'success')
    return redirect(url_for('manage_categories'))

# Exam management routes
@app.route('/admin/exams')
@login_required
def manage_exams():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    exams = Exam.query.all()
    
    return render_template(
        'admin/question_management.html',
        title='Manage Exams',
        exams=exams,
        exam_mode=True
    )

@app.route('/admin/exams/add', methods=['GET', 'POST'])
@login_required
def add_exam():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    form = ExamForm()
    
    # Get all questions for the multi-select field
    questions = Question.query.all()
    form.questions.choices = [(q.id, q.question_text[:100] + '...') for q in questions]
    
    if form.validate_on_submit():
        exam = Exam(
            title=form.title.data,
            description=form.description.data,
            duration_minutes=form.duration_minutes.data,
            pass_percentage=form.pass_percentage.data,
            is_active=form.is_active.data
        )
        db.session.add(exam)
        db.session.flush()  # Get the exam ID without committing
        
        # Add selected questions to the exam
        for i, question_id in enumerate(form.questions.data):
            exam_question = ExamQuestion(
                exam_id=exam.id,
                question_id=question_id,
                order=i + 1
            )
            db.session.add(exam_question)
        
        db.session.commit()
        
        flash('Exam has been created!', 'success')
        return redirect(url_for('manage_exams'))
    
    return render_template(
        'admin/question_management.html',
        title='Add Exam',
        form=form,
        add_exam=True,
        exam_mode=True
    )

@app.route('/admin/exams/<int:exam_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_exam(exam_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    exam = Exam.query.get_or_404(exam_id)
    form = ExamForm(obj=exam)
    
    # Get all questions for the multi-select field
    questions = Question.query.all()
    form.questions.choices = [(q.id, q.question_text[:100] + '...') for q in questions]
    
    # Set the selected questions in the form
    if request.method == 'GET':
        exam_questions = ExamQuestion.query.filter_by(exam_id=exam.id).order_by(ExamQuestion.order).all()
        form.questions.data = [eq.question_id for eq in exam_questions]
    
    if form.validate_on_submit():
        exam.title = form.title.data
        exam.description = form.description.data
        exam.duration_minutes = form.duration_minutes.data
        exam.pass_percentage = form.pass_percentage.data
        exam.is_active = form.is_active.data
        
        # Delete existing exam questions
        ExamQuestion.query.filter_by(exam_id=exam.id).delete()
        
        # Add selected questions to the exam
        for i, question_id in enumerate(form.questions.data):
            exam_question = ExamQuestion(
                exam_id=exam.id,
                question_id=question_id,
                order=i + 1
            )
            db.session.add(exam_question)
        
        db.session.commit()
        
        flash('Exam has been updated!', 'success')
        return redirect(url_for('manage_exams'))
    
    return render_template(
        'admin/question_management.html',
        title='Edit Exam',
        form=form,
        edit_exam=exam,
        exam_mode=True
    )

@app.route('/admin/exams/<int:exam_id>/delete', methods=['POST'])
@login_required
def delete_exam(exam_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    exam = Exam.query.get_or_404(exam_id)
    
    # Check if there are any attempts for this exam
    attempts = ExamAttempt.query.filter_by(exam_id=exam.id).first()
    if attempts:
        flash('This exam cannot be deleted because there are attempts linked to it.', 'danger')
        return redirect(url_for('manage_exams'))
    
    # Delete all exam questions
    ExamQuestion.query.filter_by(exam_id=exam.id).delete()
    
    # Delete the exam
    db.session.delete(exam)
    db.session.commit()
    
    flash('Exam has been deleted!', 'success')
    return redirect(url_for('manage_exams'))

@app.route('/admin/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search')
    
    # Start with base query
    query = User.query
    
    # Apply search filter if provided
    if search:
        query = query.filter(
            db.or_(
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    # Paginate the results
    users = query.order_by(User.id).paginate(page=page, per_page=20)
    
    return render_template(
        'admin/user_management.html',
        title='Manage Users',
        users=users,
        search=search
    )

@app.route('/admin/users/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    user = User.query.get_or_404(user_id)
    
    # Don't allow revoking admin from self
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('manage_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin access {status} for {user.username}.', 'success')
    
    return redirect(url_for('manage_users'))

@app.route('/admin/users/<int:user_id>/reset_password', methods=['POST'])
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        abort(403)  # Forbidden
    
    user = User.query.get_or_404(user_id)
    
    # Generate a random temporary password
    temp_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
    
    user.password_hash = generate_password_hash(temp_password)
    db.session.commit()
    
    flash(f'Password reset for {user.username}. Temporary password: {temp_password}', 'success')
    
    return redirect(url_for('manage_users'))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
