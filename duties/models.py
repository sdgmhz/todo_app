from django.db import models

from django.urls import reverse



class Duty(models.Model):
    '''
    Todo objects model
    '''
    DONE_STATUS_CHOICES = (
        ('don', 'Done'),
        ('not', 'Not done')
    )
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    done_status = models.CharField(choices=DONE_STATUS_CHOICES, max_length=3)
    deadline_date = models.DateField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id])


