from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SpeedtestResult

class SpeedtestResultList(ListView):
    model = SpeedtestResult

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html', {})

def get_data(request, *args, **kwargs):
    data = {
        "download": 200,
        "upload": 20,
    }
    return JsonResponse(data)

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # usernames = [user.username for user in User.objects.all()]
        labels = [obj.datetime for obj in SpeedtestResult.objects.all()]
        # labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        # default_items = [1, 2, 3, 4, 5, 6]
        downloads = [obj.download for obj in SpeedtestResult.objects.all()]
        uploads = [obj.upload for obj in SpeedtestResult.objects.all()]
        data = {
            "labels": labels,
            "downloads": downloads,
            "uploads": uploads,
        }
        return Response(data)