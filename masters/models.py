from django.db import models


class Shop(models.Model):
    shop_code = models.CharField(max_length=20, unique=True)
    shop_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.shop_desc


class Equipment(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    eqpt_code = models.CharField(max_length=20)
    eqpt_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.eqpt_desc


class SubEquipment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    sub_eqpt_code = models.CharField(max_length=20)
    sub_eqpt_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.sub_eqpt_desc


class Agency(models.Model):
    agency_name = models.CharField(max_length=100)

    def __str__(self):
        return self.agency_name