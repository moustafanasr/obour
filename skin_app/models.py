from django.db import models

class SkinDiseaseModel(models.Model):
    name = models.CharField(
        verbose_name="Disease Name",
        max_length=100,
    )
    definition = models.TextField(
        verbose_name="Disease Definition",
    )
    reason = models.TextField(
        verbose_name="Disease Reason",
    )
    solution = models.TextField(
        verbose_name="Disease Solutions",
    )
    def __str__(self):
        return self.name