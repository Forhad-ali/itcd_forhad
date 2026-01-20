from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator to restrict access to users with certain roles.
    Assumes User model has a `role` field (char field).
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                messages.error(request, "You must log in first.")
                return redirect('login')  # your login URL name
            if hasattr(user, 'role'):
                if user.role.lower() in [r.lower() for r in allowed_roles]:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, "You do not have permission to access this page.")
                    return redirect('home')  # your home/dashboard URL
            else:
                messages.error(request, "User has no role assigned.")
                return redirect('home')
        return _wrapped_view
    return decorator
