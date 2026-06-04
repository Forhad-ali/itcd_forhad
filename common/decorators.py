from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='login')
        def _wrapped_view(request, *args, **kwargs):
            user_role = getattr(request.user, "role", None)

            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)

            return redirect('dashboard')

        return _wrapped_view
    return decorator