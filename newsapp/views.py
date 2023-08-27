from datetime import timedelta, datetime, timezone

import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views import generic
from .forms import CustomUserCreationForm
from newsapi import NewsApiClient


class HomeView(generic.TemplateView):
    """
        View class for rendering the home page with top news headlines.

        This class-based view renders the 'home.html' template, displaying the top news headlines
        fetched from the NewsAPI. The top headlines are included in the context to be used in the template.

        Attributes:
            template_name (str): The name of the template used for rendering the home page.

        Methods:
            get_context_data(**kwargs): Enhances the context data with top news headlines.

        """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        newsapi = NewsApiClient(api_key='015d93a3dbac4e13bfef2a8441c7844c')
        top_headlines = newsapi.get_top_headlines(page=1)
        context['top_headlines'] = top_headlines
        return context


class UserRegistrationView(SuccessMessageMixin, CreateView):
    """
        View class for user registration and account creation.

        This class-based view handles the registration process by utilizing the provided
        'CustomUserCreationForm'. It uses the 'CreateView' to manage the creation of the user account,
        and it adds the 'SuccessMessageMixin' to display a success message upon successful registration.

        Attributes:
            form_class (Form): The form class responsible for user registration.
            model (Model): The model class used to create the user account.
            template_name (str): The name of the template used for rendering the registration page.
            success_message (str): The success message displayed after a successful registration.
            success_url (str): The URL to which the user is redirected after successful registration.

        """

    form_class = CustomUserCreationForm
    model = User
    template_name = 'signup.html'
    success_message = "Registration has been successful!!"
    success_url = '/login/'  # Redirect to login page after successful registration


class UserLoginView(SuccessMessageMixin, LoginView):
    """
        View class for user login and authentication.

        This class-based view handles user authentication and login using the provided 'LoginView'.
        It includes the 'SuccessMessageMixin' to display a success message upon successful login.

        Attributes:
            template_name (str): The name of the template used for rendering the login page.
            success_message (str): The success message displayed after a successful login.
            success_url (str): The URL to which the user is redirected after successful login.

        Methods:
            get_success_url(): Returns the success URL for redirection after successful login.

        """

    template_name = 'login.html'
    success_message = "Singed in successfully!!"
    success_url = '/user-dashboard/'

    def get_success_url(self):
        return self.success_url


class UserLogout(SuccessMessageMixin, LogoutView):
    success_message = "Signed out in successfully!!"
    next_page = reverse_lazy('login')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UserDashboard(generic.ListView):
    """
        View class responsible for displaying a user's news dashboard.

        This class-based view fetches news articles from the NewsAPI based on user preferences,
        such as search keywords, source names, categories, and language. The fetched articles are
        displayed in the template 'dashboard.html'.

        Attributes:
            template_name (str): The name of the template used for rendering the dashboard.
            context_object_name (str): The variable name used to pass the articles data to the template.

        Methods:
            get_queryset(): Fetches news articles based on user preferences from the NewsAPI.
            get_context_data(**kwargs): Enhances the context data with additional information.

        """

    template_name = 'dashboard.html'
    context_object_name = 'articles'

    def get_queryset(self):
        """
                Fetches news articles based on user preferences.

                This method interacts with the NewsAPI to retrieve news articles based on user-defined
                search parameters such as search keywords, source names, categories, and language.
                The fetched articles are used as the queryset for the ListView.

                Returns:
                    list: A list of news articles based on user preferences.

                """

        search_key = self.request.GET.get('search')
        refresh = self.request.GET.get('refresh') == 'true'
        date_published = self.request.GET.get('date_published')
        source_name = self.request.GET.get('source_name')
        source_category = self.request.GET.get('source_category')
        article_language = self.request.GET.get('article_language')

        # api_key = '9f56c9c8397f4b90b6f260b4ff6b6443'
        api_key = '015d93a3dbac4e13bfef2a8441c7844c'

        newsapi = NewsApiClient(api_key=api_key)

        if search_key:
            cache_key = f'newsapi_search_{search_key}'
            cached_results = cache.get(cache_key)

            filters = {
                'q': search_key,
                'sort_by': 'publishedAt',
                'language': article_language or 'en',
            }

            if date_published:
                filters['from_param'] = date_published

            if source_name:
                filters['sources'] = source_name

            if source_category:
                sources = newsapi.get_sources(category=source_category)
                source_ids = [source['id'] for source in sources['sources']]
                filters['sources'] = ','.join(source_ids)

            if refresh and cached_results and 'articles' in cached_results:
                last_published_at = cached_results['articles'][0]['publishedAt']
                last_published_date = datetime.strptime(last_published_at, "%Y-%m-%dT%H:%M:%S%z")
                last_published_date = last_published_date.replace(tzinfo=timezone.utc)
                # last_published_date = datetime.fromisoformat(last_published_at[:-1]).replace(tzinfo=timezone.utc)
                filters['from_param'] = last_published_date.isoformat()
                new_articles = newsapi.get_everything(**filters)
                cached_results['articles'] = new_articles['articles'] + cached_results['articles']
                cache.set(cache_key, cached_results, timeout=900)

            elif cached_results is None:
                new_articles = newsapi.get_everything(**filters)
            else:
                new_articles = cached_results

            return new_articles.get('articles', [])  # Extract 'articles' key or return an empty list
        else:
            top_headlines = newsapi.get_top_headlines()
            return top_headlines.get('articles', [])  # Extract 'articles' key or return an empty list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_key'] = self.request.GET.get('search')
        return context
