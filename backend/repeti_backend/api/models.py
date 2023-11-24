from django.db import models
from django.contrib.auth.models import User
import datetime

# Synset Model - stores synsets with unique identifiers
class Synset(models.Model):
    synset_id = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    examples = models.TextField(blank=True)
    part_of_speech = models.CharField(max_length=50)

    def __str__(self):
        return self.synset_id

# UserList Model - tracks words each user is learning
class UserList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    synset = models.ForeignKey(Synset, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.synset.synset_id}"

# WordReview Model - tracks the spaced repetition data for each word for each user
class WordReview(models.Model):
    user_list_entry = models.ForeignKey(UserList, on_delete=models.CASCADE)
    easiness_factor = models.FloatField(default=2.5)
    repetition_number = models.IntegerField(default=0)
    next_review_date = models.DateField(null=True, blank=True)
    last_reviewed = models.DateField(null=True, blank=True)

    def update_review(self, quality):
        # Adjusting the EF
        self.easiness_factor = max(1.3, self.easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

        # Incrementing the repetition number
        self.repetition_number += 1

        # Calculating the next review date
        if self.repetition_number == 1:
            next_review_interval = 1
        elif self.repetition_number == 2:
            next_review_interval = 6
        else:
            next_review_interval = (self.repetition_number - 1) * self.easiness_factor

        self.next_review_date = self.last_reviewed + datetime.timedelta(days=next_review_interval)
        self.save()

    def __str__(self):
        return f"{self.user_list_entry.user.username} - {self.user_list_entry.synset.synset_id}"
    
class MCQOption(models.Model):

    word = models.CharField(max_length=100)
    main_synset = models.ForeignKey(Synset, related_name='main_synset', on_delete=models.CASCADE)
    option_synset = models.ForeignKey(Synset, related_name='option_synset', on_delete=models.CASCADE)

    def __str__(self):
        return f"Word: {self.word} - Main Synset: {self.main_synset.synset_id} - Option Synset: {self.option_synset.synset_id}"