from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, 
    TextAreaField, SelectField, IntegerField, FloatField,
    RadioField, HiddenField, SelectMultipleField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, 
    ValidationError, Optional, NumberRange
)
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class QuestionForm(FlaskForm):
    question_text = TextAreaField('Question', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    difficulty = SelectField('Difficulty', choices=[
        ('easy', 'Easy'), 
        ('medium', 'Medium'), 
        ('hard', 'Hard')
    ], validators=[DataRequired()])
    explanation = TextAreaField('Explanation', validators=[Optional()])
    submit = SubmitField('Save Question')

class OptionForm(FlaskForm):
    option_text = TextAreaField('Option Text', validators=[DataRequired()])
    is_correct = BooleanField('Is Correct Answer')
    submit = SubmitField('Add Option')

class ExamForm(FlaskForm):
    title = StringField('Exam Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    duration_minutes = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    pass_percentage = FloatField('Passing Percentage', validators=[DataRequired(), NumberRange(min=1, max=100)])
    is_active = BooleanField('Is Active')
    questions = SelectMultipleField('Questions', coerce=int)
    submit = SubmitField('Save Exam')

class UserAnswerForm(FlaskForm):
    question_id = HiddenField('Question ID', validators=[DataRequired()])
    selected_option = RadioField('Answer', coerce=int, validators=[Optional()])
    is_marked = BooleanField('Mark for Review')
    submit = SubmitField('Save and Continue')
    previous = SubmitField('Previous')
    next = SubmitField('Next')
    finish = SubmitField('Finish Exam')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Category')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password')])
    submit = SubmitField('Update Profile')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please use a different one.')
