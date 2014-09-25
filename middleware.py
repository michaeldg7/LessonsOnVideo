from datetime import datetime

from django.contrib.auth import logout


class TimeOutMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            if 'last_request' in request.session:
                elapsedTime = datetime.now() - request.session['last_request']
                if elapsedTime.seconds > 15*60:
                    del request.session['last_request']
                    logout(request)

            request.session['last_request'] = datetime.now()
        else:
            if 'last_request' in request.session:
                del request.session['last_request']

        return None
