from rest_framework import serializers

from .models import SkillSet as SkillSetModel
from .models import JobType as JobTypeModel
from .models import BusinessArea as BusinessAreaModel
from .models import Company as CompanyModel
from .models import JobPost as JobPostModel
from .models import JobPostSkillSet as JobPostSkillSetModel


class JobTypeSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = JobTypeModel
        fields = "__all__"


class BusinessAreaSeiralizer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAreaModel
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    business_area = BusinessAreaSeiralizer(many=True)

    class Meta:
        model = CompanyModel
        fields = ["id", "company", "business_area"]


class JobPostSerializer(serializers.ModelSerializer):
    job_type = JobTypeSeiralizer(many=True)
    company = CompanySerializer(many=True)

    class Meta:
        model = JobPostModel
        fields = [
            "id",
            "job_type",
            "company",
            "job_description",
            "salary",
            "created_at",
        ]


class SkillSetSerializer(serializers.ModelSerializer):
    job_posts = JobPostSerializer()

    class Meta:
        model = SkillSetModel
        fields = "__all__"


class JobPostSkillSetSerializer(serializers.ModelSerializer):
    job_type = JobTypeSeiralizer(many=True)
    skill_set = SkillSetSerializer(many=True)

    class Meta:
        model = JobPostSkillSetModel
        fields = "__all__"
