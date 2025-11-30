from django.db import models

# staffmgmt/models.py
from django.db import models

class ShiftRecord(models.Model):
    hospital = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    shift_date = models.DateField()
    shift_slot = models.CharField(max_length=20)  # e.g., "morning", "evening", "night"
    scheduled_staff = models.IntegerField()       # number of staff planned for shift
    present_staff = models.IntegerField()         # number actually present
    patient_count = models.IntegerField(default=0)
    avg_patient_acuity = models.FloatField(default=0.0)  # 0..1 scale maybe
    emergencies_count = models.IntegerField(default=0)
    leaves_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)




# Create your models here.
from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')

    def __str__(self):
        return f"{self.staff.name} - {self.date}"

