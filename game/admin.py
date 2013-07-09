from django.contrib import admin
from game.models.game_info import GameInfo
from game.models.session import Session
from game.models.user import UserProfile

admin.site.register(GameInfo)
admin.site.register(Session)
admin.site.register(UserProfile)
