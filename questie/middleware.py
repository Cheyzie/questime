from django.http import HttpResponse
from rest_framework import status
import logging


class FirstMiddleware:
    def __init__(self, get_response):
        self._logger = logging.getLogger(__name__)
        self._get_response = get_response

    def __call__(self, request):
        print(__name__)
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        self._logger.warning(exception)
        return HttpResponse(str({"message":"something wrong, try again"}),status=status.HTTP_500_INTERNAL_SERVER_ERROR)