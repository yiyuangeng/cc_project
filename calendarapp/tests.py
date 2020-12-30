from django.test import TestCase,Client
import math
import re
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from app01 import models
from pprint import pprint
import json
import requests
import os
import datetime



from django.test import SimpleTestCase
from django.urls import reverse,resolve
from calendarapp.views import *




#test urls
class TestUrls(SimpleTestCase):
    def testSignin(self):
        url = reverse('calendarapp:signin')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,signin)

    
    def testRegister(self):
        url = reverse('calendarapp:signin')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,register)

    def testLogout(self):
        url = reverse('calendarapp:signin')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,logout)


    

