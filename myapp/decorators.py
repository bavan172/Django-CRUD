from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated: #after user authenticated ,he cannot go back
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func        
#allowed_users give role based permissions to access the application
def allowed_users(allowed=[]):
    def decorator(view_func):
        def wrapper(request ,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name # getting name of group which the user falls in

            if group in allowed:
                return view_func(request, *args, **kwargs)    
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper
    return decorator        


def admin_only(view_func):
    def wrapper_func(request,*args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name # getting name of group which the user falls in
        
        if group == 'customer':
            return redirect('user-page')
        
        if group == 'admin':    
            return view_func(request, *args, **kwargs)
