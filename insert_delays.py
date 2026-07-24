from datetime import timedelta
from django.utils import timezone

from masters.models import Shop, Equipment, SubEquipment, Agency
from delays.models import Delay


def add_delay(shop_code, eq_code, sub_code, agency_name, desc, mins):

    shop = Shop.objects.get(shop_code=shop_code)

    equipment = Equipment.objects.get(
        shop=shop,
        eqpt_code=eq_code
    )

    subequipment = SubEquipment.objects.get(
        equipment=equipment,
        sub_eqpt_code=sub_code
    )

    agency, created = Agency.objects.get_or_create(
        agency_name=agency_name
    )

    Delay.objects.create(
        shop=shop,
        equipment=equipment,
        subequipment=subequipment,
        agency=agency,
        delay_from=timezone.now(),
        delay_upto=timezone.now() + timedelta(minutes=mins),
        delay_duration=timedelta(minutes=mins),
        delay_desc=desc,
        entered_by="admin",
        status="Pending",
        remarks=""
    )


data = [

    ("1", "CT-1", "CHP",
     "Mechanical Maintenance",
     "Crusher conveyor breakdown", 60),

    ("1", "GPL-1", "GPL",
     "Electrical",
     "Power supply failure", 45),

    ("2", "OT-5", "OCR",
     "Mechanical Maintenance",
     "Oven maintenance issue", 120),

    ("2", "LOCP", "LOCP",
     "Electrical",
     "Locomotive control fault", 75),

    ("3", "BATTERY-5", "BATTERY",
     "Electrical",
     "Battery charging problem", 50),

    ("4", "RMB", "RMB",
     "Mechanical Maintenance",
     "Rolling mill breakdown", 150),

    ("5", "PCM", "PCM",
     "Instrumentation",
     "Pressure monitoring issue", 90),

    ("6", "CCM-1", "CCD",
     "Instrumentation",
     "Continuous casting sensor failure", 110),

    ("7", "BAR MILL", "BAR MILL",
     "Production",
     "Bar mill equipment delay", 80),

    ("10", "BOILER-1", "BOILER-1",
     "Mechanical Maintenance",
     "Boiler maintenance delay", 180),

]


for row in data:
    add_delay(*row)


print("10 Delay records inserted successfully")
print("Total Delays:", Delay.objects.count())