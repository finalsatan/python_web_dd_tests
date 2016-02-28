#!/usr/bin/env python3
# coding=utf-8

from django.db import models


class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
