from django.db import models
from distutils.command.upload import upload
from django.contrib.auth.models import User


# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    phonenumber=models.CharField(max_length=15)
    desc=models.TextField()

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    # Сoach model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)  # User who sends the message
    receiver = models.CharField(max_length=50, default="AI Trainer")  # AI Trainer as the default receiver, can be modified for scalability
    message = models.TextField()  # Message content
    response = models.TextField(blank=True)  # AI's response
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the message was sent

    def __str__(self):
        return f"{self.sender.username} to {self.receiver} on {self.timestamp}"

    class Meta:
        ordering = ['timestamp']  # To ensure messages are ordered by timestamp (oldest first)

    
class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    day_of_week = models.CharField(max_length=20)
    time = models.TimeField()
    calories = models.IntegerField()
    proteins = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.time}"
    
class WorkoutSet(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    reps = models.IntegerField()
    sets = models.IntegerField()
    day_of_week = models.CharField(
        max_length=10, 
        choices=DAYS_OF_WEEK,
        default='Monday' 
    )
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create history record
        ExerciseHistory.objects.create(
            user=self.user,
            exercise_name=self.exercise_name,
            weight=self.weight,
            reps=self.reps,
            sets=self.sets
        )

    class Meta:
        ordering = ['day_of_week', '-date']

class ExerciseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    reps = models.IntegerField()
    sets = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    personal_record = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        # Check if this is a new PR
        previous_max = ExerciseHistory.objects.filter(
            user=self.user,
            exercise_name=self.exercise_name,
            weight__gt=self.weight
        ).exists()
        
        self.personal_record = not previous_max
        super().save(*args, **kwargs)