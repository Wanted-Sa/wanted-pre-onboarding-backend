from rest_framework import serializers

from jobs.models import Job


class JobListSerializer(serializers.ModelSerializer):
    job_id = serializers.IntegerField(source="id")
    company_name = serializers.CharField(source="company.name")
    company_country = serializers.CharField(source="company.country")
    company_region = serializers.CharField(source="company.region")

    class Meta:
        model = Job
        fields = (
            "job_id",
            "company_name",
            "company_country",
            "company_region",
            "content",
            "position",
            "reward",
            "tech_stack",
        )


class JobDetailSerialzier(serializers.ModelSerializer):
    job_id = serializers.IntegerField(source="id")
    company_name = serializers.CharField(source="company.name")
    company_country = serializers.CharField(source="company.country")
    company_region = serializers.CharField(source="company.region")
    company_related_job = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            "job_id",
            "company_name",
            "company_country",
            "company_region",
            "content",
            "position",
            "reward",
            "tech_stack",
            "company_related_job",
        )

    def get_company_related_job(self, obj):
        return [job.id for job in obj.company.job_set.all()]


class JobUpdateSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "content",
            "position",
            "reward",
            "tech_stack",
        )


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "content",
            "position",
            "reward",
            "tech_stack",
            "company_id",
        )
