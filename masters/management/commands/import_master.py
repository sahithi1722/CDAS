import pandas as pd

from django.core.management.base import BaseCommand
from masters.models import Shop, Equipment, SubEquipment


class Command(BaseCommand):
    help = "Import Master Data"

    def handle(self, *args, **kwargs):
        df = pd.read_excel("master_data.xlsx", engine="openpyxl")
        for _, row in df.iterrows():

            shop, _ = Shop.objects.get_or_create(
                shop_code=str(row["SHOP_CODE"]).strip(),
                defaults={
                    "shop_desc": str(row["SHOP_DESC"]).strip()
                }
            )

            equipment, _ = Equipment.objects.get_or_create(
                shop=shop,
                eqpt_code=str(row["EQPT_CODE"]).strip(),
                defaults={
                    "eqpt_desc": str(row["EQPT_CODE"]).strip()
                }
            )

            sub = str(row["SUB_EQPT_CODE"]).strip()

            if sub and sub.lower() != "nan":
                SubEquipment.objects.get_or_create(
                    equipment=equipment,
                    sub_eqpt_code=sub,
                    defaults={
                        "sub_eqpt_desc": sub
                    }
                )

        self.stdout.write(
            self.style.SUCCESS("Master Data Imported Successfully")
        )