"""
View Module
"""
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.utils.datastructures import SortedDict
from django.shortcuts import redirect
from django.contrib.auth import logout


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

        def get_context_data(self, **kwargs):
            """
            Give base site context
            """
            context = super(BaseView, self).get_context_data(**kwargs)
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
    session_message = ""

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.__class__.session_message:
            context['message'] = self.__class__.session_message
            self.__class__.session_message = None
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.session["message"]:
            self.__class__.session_message = request.session["message"]
            request.session["message"] = None
        response = super(HomeView, self).dispatch(request, *args, **kwargs)
        return response


def logged_view(request):
    request.session["message"] = {
            "text": "Successfully logged in!",
            "type": "alert-success",
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

