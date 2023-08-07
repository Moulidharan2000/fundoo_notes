from .models import LogModel


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log = LogModel.objects.filter(method=request.method, url=request.path)
        if not log.exists():
            LogModel.objects.create(method=request.method, url=request.path)
        else:
            log = log.first()
            log.count += 1
            log.save()
        response = self.get_response(request)
        return response
