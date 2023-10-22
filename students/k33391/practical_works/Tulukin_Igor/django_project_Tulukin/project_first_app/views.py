from django.shortcuts import render
from project_first_app.models import Owner
from django.http import Http404
from django.shortcuts import render


def detail(request, owner_id):
    try:
        print('---------------', owner_id)
        p = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {
        'owner': p})
