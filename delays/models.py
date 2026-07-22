from django.db import models
from masters.models import Shop, Equipment, SubEquipment, Agency


class Delay(models.Model):

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    subequipment = models.ForeignKey(SubEquipment, on_delete=models.CASCADE)

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

    delay_from = models.DateTimeField()

    delay_upto = models.DateTimeField()

    delay_duration = models.DurationField()

    delay_desc = models.TextField()

    entered_by = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
    max_length=20,
    choices=[
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected")
    ],
    default="Pending"
)
    remarks = models.TextField(
    blank=True,
    default=""
)
    def __str__(self):
        return self.delay_desc
class DelayHistory(models.Model):

    delay = models.ForeignKey(
        Delay,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=100
    )

    user = models.CharField(
        max_length=50
    )

    remarks = models.TextField(
        blank=True,
        default=""
    )

    action_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.delay.id} - {self.action}"