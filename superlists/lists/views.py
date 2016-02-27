#!/usr/bin/env python3
# coding=utf-8


from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return render(request, 'home.html')
