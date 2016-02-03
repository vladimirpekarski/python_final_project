import hashlib
import datetime
import random

from django.core.management.base import BaseCommand, CommandError
from final_app.models import LogGameEvents, PlayerAchievements, Players, PlayerSessions, PlayerStats


class Command(BaseCommand):
    help = 'Fill up db with data'

    def add_arguments(self, parser):
        parser.add_argument('--player-count', default=100, type=int)
        parser.add_argument('--session-count-per-user', default=10, type=int)

    def _create_session(self, player_object, session_index):
        session = PlayerSessions()
        session_unique_part = str(session_index) + str(datetime.datetime.now())
        session_uuid = hashlib.sha1(session_unique_part).hexdigest()
        session.player = player_object
        session.sid = session_uuid
        session.is_finished = bool(random.randint(0, 1))

        session_ttl = random.randint(10, 7200)
        session.updated = datetime.datetime.now() + datetime.timedelta(seconds=session_ttl)
        session.save()

    def _create_achievements(self, player_object, achievement_index):
        achievement = PlayerAchievements()
        achievement.player = player_object
        achievement.achievement_id = achievement_index
        achievement.save()

    def _create_stats(self, player_object, stats_index):
        stats = PlayerStats()
        stats.player = player_object
        stats.stat_id = stats_index
        stats_value = random.randint(50, 50000)
        stats.value = stats_value
        stats.save()

    def _create_log_event(self, player_object, log_index):
        log_event = LogGameEvents()
        log_event.player = player_object
        log_event.event_type = log_index
        event_data = 'event_' + str(log_index) + str(datetime.datetime.now())
        log_event.event_data = event_data
        log_event.save()

    def _create_player(self, player_index, options):
        player = Players()
        nickname_unique_part = str(player_index) + str(datetime.datetime.now())
        nickname_unique_hash = hashlib.sha1(nickname_unique_part).hexdigest()[:10]
        player.nickname = "test_{}".format(nickname_unique_hash)
        player.email = "{}@tut.by".format(player.nickname)
        player.xp = 0
        player.save()
        for session_index in xrange(options["session_count_per_user"]):
            self._create_session(player, session_index)

        for achievement_index in xrange(5):
            self._create_achievements(player, achievement_index)

        for stats_index in xrange(5):
            self._create_stats(player, stats_index)

        for log_index in xrange(5):
            self._create_log_event(player, log_index)

    def handle(self, *args, **options):
        for i in xrange(options["player_count"]):
            self._create_player(i, options)
