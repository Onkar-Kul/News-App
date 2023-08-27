# News-App
The Django News APP Project is a web application built using the Django framework that allows users to stay informed about the latest news articles from various sources. This project includes a range of views and functionalities, providing user registration, login, and a personalized news dashboard.

### Project Features
User Registration and Login:
Users can register and create accounts using a custom user registration form. After registration, users can log in securely using their credentials.

__Personalized News Dashboard__:
The application offers a personalized news dashboard where registered users can view a curated list of news articles. The dashboard presents top headlines and allows users to search for news articles based on keywords, sources, categories, languages, and publication dates.

__User-Friendly Interface__:
The application's user interface is designed to be intuitive and user-friendly. Users can easily navigate through the dashboard, view articles, and customize their news feed based on their interests.

__NewsAPI Integration__:
The project integrates the NewsAPI to fetch the latest news articles. Users can access articles from various sources and stay updated on current events.

__Efficient Caching Mechanism__:
To enhance performance, the application utilizes a caching mechanism to store and retrieve frequently accessed data, reducing the need for repeated API requests.

### Project Folder Structure
```
Practice_Project
├─ .gitignore
├─ db.sqlite3
├─ manage.py
├─ news_articles
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ newsapp
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  │     └─ __init__.cpython-38.pyc
│  ├─ models.py
│  ├─ tests.py
│  ├─ urls.py
│  └─ views.py
├─ static
│  └─ css
│     └─ signup.css
└─ templates
   ├─ base.html
   ├─ dashboard.html
   ├─ filtered_dashboard.html
   ├─ home.html
   ├─ login.html
   ├─ signup.html
   └─ user_base.html

```

### Guidlines for project installation
1. Clone repository: ``` git clone <Path> ```
2. Create Environment: ``` python -m venv environment name```
3. Activate Environment: ``` source environment_name/bin/activate or environment_name\Scripts\activate```
4. Install Requirements: ``` pip install -r requirements.txt```
5. Migrations: ``` python manage.py migrate```
6. Project Run: ``` python manage.py runserver```