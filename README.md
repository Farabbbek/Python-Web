# Python-Web
Web application
# HeavyWeight - Fitness Tracking Application

HeavyWeight is a comprehensive web-based fitness tracking application built with Django that helps users manage their workout routines, track nutrition, and monitor their fitness progress.

## Features

- **User Authentication**
  - Secure login/signup system 
  - Customizable user profiles with profile pictures
  - Personal bio and contact information

- **Nutrition Tracking**
  - Food logging with calories and protein tracking
  - Daily meal planning
  - Nutritional progress monitoring

- **Workout Management**
  - Sets and reps tracking
  - Exercise progress monitoring
  - Personal records tracking

- **AI Coach Integration**
  - Personalized workout recommendations
  - 24/7 guidance availability
  - Adaptive training suggestions

## Technology Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **CSS Framework:** Bootstrap
- **Icons:** Font Awesome, Bootstrap Icons

## Installation

1. Clone the repository:
```sh
git clone https://github.com/Farabbbek/Python-Web.git
cd heavyweight
```

2. Create and activate virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Run migrations:
```sh
python manage.py migrate
```

5. Start development server:
```sh
python manage.py runserver
```

## Project Structure

```
heavyweight/
├── authapp/            # Authentication app
├── heavyweight/        # Main project settings
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── media/            # User uploaded files
└── requirements.txt  # Project dependencies
