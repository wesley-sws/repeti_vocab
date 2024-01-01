from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from datetime import date
from django.conf import settings
# ignore all on_delete=... for AppSynset foreign key as no entries from AppSynset will ever be deleted


# Synset Model - stores synsets with unique identifiers
class AppSynset(models.Model):
    synset_id = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    examples = models.TextField(blank=True)
    part_of_speech = models.CharField(max_length=50)

    def __str__(self):
        return self.synset_id
    
class CustomUser(AbstractUser):
    email_verified = models.BooleanField(default=False)

# UserList Model - tracks words each user is learning
class UserList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    synset = models.ForeignKey(AppSynset, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.synset.synset_id}"

# WordReview Model - tracks the spaced repetition data for each word for each user
class WordReview(models.Model):
    user_list_entry = models.ForeignKey(UserList, on_delete=models.CASCADE)
    easiness_factor = models.FloatField(default=2.5)
    repetition_number = models.IntegerField(default=0)
    review_date = models.DateField(null=True, blank=True)
    interval = models.IntegerField(default=0)

    def update_review(self, quality):
        # Incrementing the repetition number
        self.repetition_number += 1
        # Calculating the next review date
        if self.repetition_number == 1:
            self.interval = 1
        elif self.repetition_number == 2:
            self.interval = 6
        else:
            self.interval = round(self.interval * self.easiness_factor)
        # Adjusting the EF
        self.easiness_factor = max(1.3, self.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        self.next_review_date = self.review_date + datetime.timedelta(days=self.interval)
        self.save()

    def __str__(self):
        return f"{self.user_list_entry.user.username} - {self.user_list_entry.synset.synset_id}"

# MCQOption Model - stores incorrect MCQAnswers for each word synset pair
class MCQOption(models.Model):

    word = models.CharField(max_length=100)
    main_synset = models.ForeignKey(AppSynset, related_name='main_synset', on_delete=models.CASCADE)
    option_synset = models.ForeignKey(AppSynset, related_name='option_synset', on_delete=models.CASCADE)

    def __str__(self):
        return f"Word: {self.word} - Main Synset: {self.main_synset.synset_id} - Option Synset: {self.option_synset.synset_id}"
    
