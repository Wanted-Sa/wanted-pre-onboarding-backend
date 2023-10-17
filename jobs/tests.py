from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from jobs.models import Company, Job, User


class JobListViewTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        for i in range(10):
            company = Company.objects.create(
                name=f"company{i}",
                country=f"country{i}",
                region=f"region{i}",
            )
            Job.objects.create(
                content=f"content{i}",
                position=f"position{i}",
                reward=f"reward{i}",
                tech_stack=f"tech_stack{i}",
                company=company,
            )

    def test_job_all_list_success(self):
        response = self.client.get(
            path=reverse("job_list"),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_job_search_list_success(self):
        response = self.client.get(
            path=reverse("job_list"),
            data={"search": "content1"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_job_search_list_not_found_suceess(self):
        response = self.client.get(
            path=reverse("job_list"),
            data={"search": "content11"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class JobCreateViewTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.company = Company.objects.create(
            name=f"company",
            country=f"country",
            region=f"region",
        )

    def test_job_create_success(self):
        data = {
            "content": "content",
            "position": "position",
            "reward": "reward",
            "tech_stack": "tech_stack",
        }
        response = self.client.post(path=reverse("job_create", kwargs={"company_id": self.company.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], data["content"])
        self.assertEqual(response.data["position"], data["position"])
        self.assertEqual(response.data["reward"], data["reward"])
        self.assertEqual(response.data["tech_stack"], data["tech_stack"])

    def test_job_create_company_not_found_fail(self):
        data = {
            "content": "content",
            "position": "position",
            "reward": "reward",
            "tech_stack": "tech_stack",
        }
        response = self.client.post(path=reverse("job_create", kwargs={"company_id": 2}), data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_job_create_blank_fail(self):
        data = {
            "content": "",
            "position": "",
            "reward": "",
            "tech_stack": "",
        }
        response = self.client.post(path=reverse("job_create", kwargs={"company_id": self.company.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_create_required_fail(self):
        data = {
            "content": "content",
            "position": "position",
            "reward": "reward",
        }
        response = self.client.post(path=reverse("job_create", kwargs={"company_id": self.company.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class JobDetailViewTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.company = Company.objects.create(
            name=f"company",
            country=f"country",
            region=f"region",
        )
        self.job = Job.objects.create(
            content=f"content",
            position=f"position",
            reward=f"reward",
            tech_stack=f"tech_stack",
            company=self.company,
        )

    def test_job_detail_get_success(self):
        response = self.client.get(
            path=reverse("job_detail", kwargs={"job_id": self.job.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], self.job.content)
        self.assertEqual(response.data["position"], self.job.position)
        self.assertEqual(response.data["reward"], self.job.reward)
        self.assertEqual(response.data["tech_stack"], self.job.tech_stack)
        self.assertEqual(response.data["company_name"], self.company.name)
        self.assertEqual(response.data["company_country"], self.company.country)
        self.assertEqual(response.data["company_region"], self.company.region)
        self.assertEqual(response.data["company_related_job"], [self.job.id])

    def test_job_detail_get_not_found_fail(self):
        response = self.client.get(
            path=reverse("job_detail", kwargs={"job_id": 3}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_job_detail_put_success(self):
        data = {
            "content": "content",
            "position": "position",
            "reward": "reward",
            "tech_stack": "tech_stack",
        }
        response = self.client.put(path=reverse("job_detail", kwargs={"job_id": self.job.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], data["content"])
        self.assertEqual(response.data["position"], data["position"])
        self.assertEqual(response.data["reward"], data["reward"])
        self.assertEqual(response.data["tech_stack"], data["tech_stack"])

    def test_job_detail_put_not_found_fail(self):
        data = {
            "content": "content",
            "position": "position",
            "reward": "reward",
            "tech_stack": "tech_stack",
        }
        response = self.client.put(path=reverse("job_detail", kwargs={"job_id": 3}), data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_job_detail_put_blank_fail(self):
        data = {
            "content": "",
            "position": "",
            "reward": "",
            "tech_stack": "",
        }
        response = self.client.put(path=reverse("job_detail", kwargs={"job_id": self.job.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_detail_put_required_fail(self):
        data = {
            "content": "content",
            "position": "position",
            "reward": "reward",
        }
        response = self.client.put(path=reverse("job_detail", kwargs={"job_id": self.job.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_detail_delete_success(self):
        response = self.client.delete(
            path=reverse("job_detail", kwargs={"job_id": self.job.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_job_detail_delete_not_found_fail(self):
        response = self.client.delete(
            path=reverse("job_detail", kwargs={"job_id": 3}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class JobRecruitViewTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.company = Company.objects.create(
            name=f"company",
            country=f"country",
            region=f"region",
        )
        self.job = Job.objects.create(
            content=f"content",
            position=f"position",
            reward=f"reward",
            tech_stack=f"tech_stack",
            company=self.company,
        )
        self.user = User.objects.create()

    def test_job_recruit_success(self):
        response = self.client.post(
            path=reverse("job_recruit", kwargs={"job_id": self.job.id, "user_id": self.user.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_job_recruit_job_not_found_fail(self):
        response = self.client.post(
            path=reverse("job_recruit", kwargs={"job_id": 3, "user_id": self.user.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_job_recreuit_user_not_found_fail(self):
        response = self.client.post(
            path=reverse("job_recruit", kwargs={"job_id": self.job.id, "user_id": 3}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_job_recruit_already_recruited_fail(self):
        self.job.user_job.add(self.user)
        response = self.client.post(
            path=reverse("job_recruit", kwargs={"job_id": self.job.id, "user_id": self.user.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
