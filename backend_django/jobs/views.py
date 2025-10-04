from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Job, Resume
from .forms import ResumeForm, RegisterForm
from .utils import parse_resume, get_recommendations_from_fastapi, fetch_jobs_from_remoteok
from django.shortcuts import render, get_object_or_404
from .models import Job
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, UserJobView


def home(request):
    jobs = Job.objects.all()
    return render(request, "jobs/home.html", {"jobs": jobs})



@login_required(login_url='login')
def upload_resume(request): 
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # if(UserWarning):
            #     return redirect("login")
            
            # 🔁 Delete existing resume (to avoid IntegrityError)
            Resume.objects.filter(user=request.user).delete()

            # ✅ Create new resume
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            # ✅ Extract text from uploaded resume
            resume_text = parse_resume(resume.file.path)
            resume.text = resume_text
            resume.save()

            # ✅ Fetch jobs if DB is empty
            if Job.objects.count() == 0:
                fetch_jobs_from_remoteok(limit=50)

            # ✅ Get recommendations
            jobs = Job.objects.all()
            recommendations = get_recommendations_from_fastapi(resume_text, jobs)

            # ✅ Store recommendations in session
            request.session["recommendations"] = recommendations

            # ✅ Redirect to recommendations page
            return redirect("recommendations")
    else:
        form = ResumeForm()

    return render(request, "jobs/upload_resume.html", {"form": form})



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "jobs/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "jobs/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")




from .models import Job
@login_required(login_url='login')
def profile(request):
    user = request.user
    return render(request, "jobs/profile.html", {"user": user})

@login_required(login_url='login')
def all_jobs(request):
    jobs = Job.objects.all()
    return render(request, "jobs/all_jobs.html", {"jobs": jobs})

@login_required
def recommendations(request):
    results = request.session.get("recommendations", [])
    jobs = Job.objects.all()
    return render(
        request,
        "jobs/recommendations.html",
        {
            "results": results,  # top 10 related jobs
            "jobs": jobs         # all jobs for "See More"
        }
    )



@login_required(login_url='login')
def profile(request):
    user = request.user
    
    # ✅ Get user's resume if uploaded
    resume = Resume.objects.filter(user=user).first()
    
    # ✅ Recently viewed jobs (limit 5)
    recent_views = UserJobView.objects.filter(user=user).order_by('-viewed_at')[:10]
    
    # ✅ Recommended jobs (limit 5)
    recommendations = Job.objects.all().order_by('-created_at')[:5]
    
    # ✅ Handle NULL or empty links safely
    for job in recommendations:
        if not job.link:
            job.link = "#"  # fallback safe placeholder

    context = {
        "user": user,
        "resume": resume,
        "recent_views": recent_views,
        "recommendations": recommendations,
    }

    return render(request, "jobs/profile.html", context)






from .models import UserJobView


@login_required(login_url='login')
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # ✅ Track user's job view — update timestamp if already viewed
    if request.user.is_authenticated:
        user_view, created = UserJobView.objects.get_or_create(
            user=request.user,
            job=job
        )
        if not created:
            # Update timestamp if the job was viewed again
            user_view.viewed_at = timezone.now()
            user_view.save(update_fields=['viewed_at'])

    return render(request, "jobs/job_detail.html", {"job": job})



def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # If link exists, redirect to it
    if job.link:
        return redirect(job.link)

    # Otherwise, redirect to a default apply page or message
    default_link = "https://remoteok.com/"  # ← You can change this to any site you want
    return redirect(default_link)

