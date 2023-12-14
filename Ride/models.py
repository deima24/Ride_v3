from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.


STATUS = ((0, "Draft"), (1, "Published"))

class Entry(models.Model):
    """
    Storing Entry data
    """

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    distance = models.IntegerField(help_text="Add the distance", default=0)
    start = models.TextField(blank=False)
    finish = models.TextField(blank=False)
    content = models.TextField()
    featured_image = CloudinaryField("image", default="placeholder")
    status = models.IntegerField(choices=STATUS, default=0)
    difficulty = models.CharField(
        max_length=10, null=True, blank=True, choices=diff
    )

    class Meta:
        ordering = ["-created_on"]

    def average_rating(self) -> float:
        return (
            Rating.objects.filter(entry=self).aggregate(Avg("rating"))[
                "rating__avg"
            ]
            or 0
        )

    def __str__(self):
        return f"{self.title}: {self.average_rating()}"
