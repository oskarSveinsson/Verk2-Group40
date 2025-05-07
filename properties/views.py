from django.http import HttpResponse

def index(request):
    return HttpResponse(f"Response from {request.path}")

def get_properties_by_id(request, id):
    return HttpResponse(f"Response from {request.path} with id {id}")
