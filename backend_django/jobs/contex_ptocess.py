# jobs/context_processors.py
from .models import Resume

def resume_status(request):
    """
    Adds `user_has_resume` to template context (True/False).
    """
    user = request.user
    has_resume = False
    if user.is_authenticated:
        has_resume = Resume.objects.filter(user=user).exists()
    return {"user_has_resume": has_resume}



    