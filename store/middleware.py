from django.db import connection

class LogUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            self.log_user_action(request.user.username, "бет ашылды", request.path)

        return response

    def log_user_action(self, username, action, path):
        with connection.cursor() as cursor:
            cursor.execute("SELECT log_user_action(%s, %s, %s)", [username, action, path])
