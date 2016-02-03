from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import LogGameEvents, Players, PlayerAchievements, PlayerSessions, PlayerStats

admin.site.register(LogGameEvents)
admin.site.register(Players)
admin.site.register(PlayerAchievements)
admin.site.register(PlayerSessions)
admin.site.register(PlayerStats)

