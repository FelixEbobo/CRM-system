from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('Home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_roles=tuple()):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.groups.all()[0].name in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed to view this")
        return wrapper_func
    return decorator