import requests
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotAllowed

from django.shortcuts import render, redirect

from parse import parser
from parse.forms import UpdateForm
from parse.models import Data, Page


def parse_news(request):
    if not request.user.is_superuser:
        return redirect('admin:index')

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        try:
            parser.parse_parent('https://www.gazeta.ru/news/', quantity)
        except requests.exceptions.SSLError as e:
            return HttpResponseBadRequest("Max retries exceeded")

        return redirect('index')

    return HttpResponseNotAllowed('Method not allowed')


def index(request):
    datas = Data.objects.all().values('category', 'dictionary', 'quantity')
    return render(request, 'index.html', {'data': datas})


def pages(request):
    pages = Page.objects.all().values('link', 'title', 'category', 'parsed_at').order_by('parsed_at')
    paginator = Paginator(pages, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {'pages': page_obj})


def analysis(request):
    datas = Data.objects.all().values('category', 'dictionary', 'quantity')
    return render(request, 'analysis.html', {'data': datas})


def update(request):
    form = UpdateForm()
    return render(request, 'update.html', {'form': form})
