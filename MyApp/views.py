from django.shortcuts import render
from .models import TestModel

def test_view(request):
    tests = TestModel.objects.all()
    return render(request, 'MyApp/test_template.html', {'tests': tests})
