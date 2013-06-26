"""
View Module
"""
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.utils.datastructures import SortedDict


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

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class GameList(LView):
    """
    View class for list of games
    """
    template_name = 'game_list.html'
    page_title = 'Games List'

