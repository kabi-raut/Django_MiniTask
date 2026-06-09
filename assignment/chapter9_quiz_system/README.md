# Online Quiz System - Chapter 9

A comprehensive Django-based Online Quiz System that allows admins to create quizzes and users to take them with score tracking and user authentication.

## Features

### 1. **Admin Functionality**
- Create, edit, and delete quizzes
- Add questions (Multiple Choice & True/False) to quizzes
- Manage answer choices for each question
- Set passing percentage for quizzes
- Set time limits for quizzes (optional)
- Activate/deactivate quizzes
- View all student attempts and scores
- Full Django admin interface integration

### 2. **User Functionality**
- Browse available quizzes
- Take quizzes with timer support
- Auto-submit on time limit expiration
- Review quiz results with detailed feedback
- View score breakdown by question
- Track attempt history
- See which answers were correct/incorrect
- Personal dashboard with statistics

### 3. **Authentication & Authorization**
- User login required for all quiz features
- Admin-only access to quiz management
- Quiz creator can manage their own quizzes
- User attempts are isolated and secure

### 4. **Database Models**

#### Quiz
- Title and description
- Created by (Admin/Staff user)
- Passing percentage threshold
- Time limit (optional)
- Active/Inactive status
- Timestamps (creation, update)

#### Question
- Question text
- Question type (Multiple Choice / True/False)
- Points value
- Order within quiz
- Relationship to Quiz

#### Choice
- Choice text
- Correct answer flag
- Order within question
- Relationship to Question

#### QuizAttempt
- User who attempted
- Quiz attempted
- Start and completion time
- Score and total points
- Pass/Fail status
- Timestamps

#### QuestionAnswer
- User's selected choice
- Question reference
- Attempt reference
- Answer timestamp
- Automatic correctness evaluation

## Usage

### For Admins

1. **Creating a Quiz**
   - Navigate to `/chapter9/create/`
   - Fill quiz details (title, description, passing percentage, time limit)
   - Click "Create Quiz"

2. **Adding Questions**
   - Go to quiz edit page (`/chapter9/quiz/<id>/edit/`)
   - Click "Add Question"
   - Add question text and choose question type
   - Specify points value
   - Add answer choices and mark the correct one

3. **Managing Quizzes**
   - View all quizzes: `/chapter9/`
   - Edit: Click "Edit" button on quiz card
   - Delete: Click "Delete" button (confirmation required)

### For Users

1. **Taking a Quiz**
   - Go to `/chapter9/` to see available quizzes
   - Click on a quiz to view details
   - Click "Start Quiz" to begin
   - Answer all questions (required)
   - Click "Submit Quiz" to finish

2. **Viewing Results**
   - See immediate score after submission
   - Review each question with your answer vs. correct answer
   - Check if you passed or failed
   - Retake the quiz anytime

3. **Dashboard**
   - Navigate to `/chapter9/dashboard/`
   - View statistics (total attempts, passed, failed, average score)
   - See all attempt history
   - Resume in-progress quizzes

## Key Features

### Score Tracking
- Points per question
- Total score calculation
- Percentage score display
- Pass/Fail status based on passing percentage threshold

### Time Management
- Optional time limits per quiz
- Countdown timer on quiz page
- Auto-submission when time expires
- Time-based disqualification

### Form Implementation
- `QuizForm` - Create/Edit quizzes with validation
- `QuestionForm` - Create/Edit questions with dynamic ordering
- `ChoiceForm` & `ChoiceFormSet` - Manage question choices efficiently
- `QuizTakeForm` - Dynamic form generation based on quiz questions

### Relationships
- User (Auth) → Quiz (created_by)
- User (Auth) → QuizAttempt (user)
- Quiz → Question (one-to-many)
- Question → Choice (one-to-many)
- QuizAttempt → QuestionAnswer (one-to-many)
- Question → QuestionAnswer (one-to-many)

## URL Patterns

| URL | Name | Purpose |
|-----|------|---------|
| `/chapter9/` | quiz_list | List all quizzes |
| `/chapter9/quiz/<id>/` | quiz_detail | View quiz details |
| `/chapter9/quiz/<id>/start/` | start_quiz | Start taking a quiz |
| `/chapter9/attempt/<id>/take/` | take_quiz | Quiz interface |
| `/chapter9/attempt/<id>/results/` | quiz_results | View results |
| `/chapter9/create/` | quiz_create | Create new quiz (admin) |
| `/chapter9/quiz/<id>/edit/` | quiz_edit | Edit quiz (admin) |
| `/chapter9/quiz/<id>/delete/` | quiz_delete | Delete quiz (admin) |
| `/chapter9/quiz/<id>/question/create/` | question_create | Add question (admin) |
| `/chapter9/question/<id>/edit/` | question_edit | Edit question (admin) |
| `/chapter9/dashboard/` | user_dashboard | User dashboard |

## Admin Interface

Access Django admin at `/admin/`:

- **Quiz Admin**: Full CRUD with inline questions
- **Question Admin**: Full CRUD with inline choices
- **Choice Admin**: Manage answer options
- **QuizAttempt Admin**: View attempts, scores, and user performance
- **QuestionAnswer Admin**: Review individual answers

## Security Features

1. **Authentication**: All quiz views require login
2. **Authorization**: Only admins/staff can create quizzes
3. **Ownership**: Only quiz creators can edit/delete their quizzes
4. **User Isolation**: Users can only see their own attempts
5. **CSRF Protection**: All forms protected with CSRF tokens

## Templates

- `quiz_list.html` - Browse available quizzes with stats
- `quiz_detail.html` - Quiz details and previous attempts
- `take_quiz.html` - Quiz interface with timer
- `quiz_results.html` - Detailed results and feedback
- `quiz_form.html` - Create/Edit quiz form
- `question_form.html` - Create/Edit question with choices
- `user_dashboard.html` - User performance dashboard
- `quiz_confirm_delete.html` - Deletion confirmation

## Static Files & Styling

Uses Bootstrap 5 for responsive design and Font Awesome for icons.

## Property Methods

### QuizAttempt
- `percentage`: Calculate score percentage
- `is_completed`: Check if attempt is finished
- `calculate_score()`: Calculate and save score

### QuestionAnswer
- `is_correct`: Check if answer is correct (property)

## Advanced Features

- **Inline Admin Management**: Edit questions and choices from quiz edit page
- **Timestamping**: Automatic tracking of creation and modification times
- **Annotations**: Quiz list shows stats (attempts, average score)
- **Formsets**: Efficient multiple choice management
- **Dynamic Forms**: Quiz form generated based on actual questions
- **Timer JavaScript**: Client-side countdown with auto-submit
- **Unique Constraints**: Prevent duplicate attempts and answers

## Getting Started

1. Register app in `settings.py` ✓
2. Include URLs in main `urls.py` ✓
3. Run migrations ✓
4. Create admin user
5. Access admin panel to create quizzes
6. Users can access quizzes at `/chapter9/`

## Example Quiz Structure

```
Quiz: "Python Basics"
├─ Question 1 (3 pts): What is Python?
│  ├─ Choice: A programming language (CORRECT)
│  ├─ Choice: A snake
│  ├─ Choice: An IDE
│  └─ Choice: None of the above
├─ Question 2 (2 pts): True/False - Python is dynamically typed
│  ├─ Choice: True (CORRECT)
│  └─ Choice: False
└─ Question 3 (3 pts): List 3 Python features...
```

## Notes

- Passing percentage is set at quiz level (default 50%)
- Points can vary per question
- Time limits are optional (None = unlimited)
- Users can retake quizzes multiple times
- All scores are tracked in database for analytics
- Bootstrap CSS framework used for responsive UI
