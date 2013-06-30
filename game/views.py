"""
View Module
"""
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.utils.datastructures import SortedDict
from django.shortcuts import redirect
from django.contrib.auth import logout
from game.models.game_info import GameInfo
from game.models.user import UserProfile


def template_factory(base_class):
    class BaseView(base_class):
        """
        Provide the base site context
        """
        nav_list = [
                {'name': "Games List", 'ref': "/games/"},
            ]

        script_list = [
                'jquery.js',
                'bootstrap.js',
                ]

        session_message = ""

        def dispatch(self, request, *args, **kwargs):
            if request.session.get("message"):
                self.__class__.session_message = request.session["message"]
                request.session["message"] = None
            response = super(BaseView, self).dispatch(request, *args, **kwargs)
            return response

        def get_context_data(self, **kwargs):
            """
            Give base site context
            """
            context = super(BaseView, self).get_context_data(**kwargs)
            if self.__class__.session_message:
                context['message'] = self.__class__.session_message
                self.__class__.session_message = None
            context['nav_list'] = self.__class__.nav_list
            context['page_title'] = self.__class__.page_title
            context['script_list'] = self.__class__.script_list
            return context

    return BaseView


TView = template_factory(TemplateView)
LView = template_factory(ListView)


class HomeView(TView):
    """
    View class for home page
    """
    template_name = 'home.html'
    page_title = 'Home'


def logged_view(request):
    if not UserProfile.objects.filter(user=request.user).count():
        UserProfile.objects.create(user=request.user)
    request.session["message"] = {
            "text": "Successfully logged in!",
            "type": "alert-success",
            }
    return redirect('/')


def login_error_view(request):
    request.session["message"] = {
            "text": "Authentication Error",
            "type": "alert-error",
            }
    return redirect('/')


def logout_view(request):
    logout(request)
    request.session["message"] = {
            "text": "Successfully logged out",
            "type": "alert-success",
            }
    return redirect('/')


class GameList(LView):
    """
    View class for list of games
    """
    template_name = 'game_list.html'
    page_title = 'Games List'
    model = GameInfo


