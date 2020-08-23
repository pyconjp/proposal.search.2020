import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from search.models import Talk


class Command(BaseCommand):
    help = "Load talk data from specified csv file."

    def add_arguments(self, parser):
        parser.add_argument("csv_path")

    def handle(self, *args, **options):
        with open(options["csv_path"]) as f:
            reader = csv.DictReader(f)
            with transaction.atomic():
                talks = Talk.objects.all()
                talks.delete()

                for row in reader:
                    # トーク・招待講演以外はスキップする
                    if not row["no"]:
                        continue
                    Talk.objects.create(
                        sessionize_id=row["id"],
                        day=int(row["day"]),
                        no=int(row["no"]),
                        room=row["room"],
                        title=row["title"],
                        description=row["description"],
                        elevator_pitch=row["elevator_pitch"],
                        talk_format=row["talk_format"],
                        category=row["track"],
                        audience_python_level=row["audience_python_level"],
                        audience_domain_expertise=row["audience_expertise"],
                        speaking_language=row["lang_of_talk"],
                        slide_language=row["lang_of_slide"],
                        prerequisite_knowledge=row["prerequisite_knowledge"],
                        audience_take_away=row["audience_takeaway"],
                    )
        print("loading done!")
