from django.shortcuts import HttpResponseRedirect

def user_session_set(function):
    def wrap(request, *args, **kwargs):
    	if 'username' not in request.session:
    		return HttpResponseRedirect('/roads/login/')
    	return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap