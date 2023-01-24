from django.shortcuts import  render
from django.urls import reverse


def main(request):
    return render(request, 'dashboard_mct_new.html')