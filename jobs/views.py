from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.models import Company, Job, User
from jobs.serializers import JobCreateSerializer, JobDetailSerialzier, JobListSerializer, JobUpdateSerialzier


class JobListView(APIView):
    permission_classes = (AllowAny,)

    def get_filtered_jobs(self, search):
        search_fields = [
            "content__contains",
            "position__contains",
            "reward__contains",
            "tech_stack__contains",
            "company__name__contains",
            "company__country__contains",
            "company__region__contains",
        ]

        qs = Q()
        for field in search_fields:
            qs |= Q(**{field: search})

        return Job.objects.select_related("company").filter(qs)

    def get(self, request):
        search = request.query_params.get("search", "")
        jobs = self.get_filtered_jobs(search)
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)


class JobCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, company_id):
        company = get_object_or_404(Company, pk=company_id)
        serializer = JobCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        serializer = JobDetailSerialzier(job)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        serializer = JobUpdateSerialzier(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_id):
        job = get_object_or_404(Job, pk=job_id)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobRecruitView(APIView):
    permission_classes = (AllowAny,)

    def is_user_already_recruited(self, job, user):
        return job.user_job.filter(id=user.id).exists()

    def recruit_user_for_job(self, user, job):
        user.job_set.add(job)

    def post(self, request, job_id, user_id):
        job = get_object_or_404(Job, pk=job_id)
        user = get_object_or_404(User, pk=user_id)

        if self.is_user_already_recruited(job, user):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.recruit_user_for_job(user, job)
        context = {
            "user_id": user.id,
            "job_id": job.id,
        }
        return Response(context, status=status.HTTP_200_OK)
