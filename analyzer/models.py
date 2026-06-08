from django.contrib.auth.models import User
from django.db import models


class ResumeAnalysis(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    job_description = models.TextField()

    resume_text = models.TextField()

    match_score = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"Resume Score: {self.match_score}"