from django.urls import path

from jobs.views import JobCreateView, JobDetailView, JobListView, JobRecruitView

urlpatterns = [
    path("", JobListView.as_view(), name="job_list"),
    path("<int:company_id>/", JobCreateView.as_view(), name="job_create"),
    path("details/<int:job_id>/", JobDetailView.as_view(), name="job_detail"),
    path("recruit/<int:job_id>/users/<int:user_id>/", JobRecruitView.as_view(), name="job_recruit"),
]
