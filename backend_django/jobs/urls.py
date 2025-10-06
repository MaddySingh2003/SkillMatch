from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("resume/<int:resume_id>/", views.view_resume, name="view_resume"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("upload_resume/", views.upload_resume, name="upload_resume"),
    path("recomandations/",views.recommendations,name='recommendations'),
    path("all_jobs/", views.all_jobs, name="all_jobs"),
    path("profile/", views.profile, name="profile"),
    path("job/<int:job_id>/", views.job_detail, name="job_detail"),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('load-more-jobs/', views.load_more_jobs, name='load_more_jobs'),
]
