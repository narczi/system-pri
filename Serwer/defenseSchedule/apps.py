from django.apps import AppConfig


class DefenseScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'defenseSchedule'

    def ready(self):
        import defenseSchedule.signals 
