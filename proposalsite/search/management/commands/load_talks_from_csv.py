import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from search.models import Talk


class Command(BaseCommand):
    help = "Load talk data from specified csv file."

    def add_arguments(self, parser):
        parser.add_argument("csv_path")

    def handle(self, *args, **options):
        # The input value from the CSV file is equal to one of the labels.
        # Convert it to a value to be stored in the DB.
        speak_language_converter = {
            label: value for value, label in Talk.SpeakingLanguage.choices
        }
        slide_language_converter = {
            label: value for value, label in Talk.SlideLanguage.choices
        }

        with open(options["csv_path"]) as f:
            reader = csv.DictReader(f)
            with transaction.atomic():
                talks = Talk.objects.all()
                talks.delete()

                for row in reader:
                    # Skip all but the talks / invited talks.
                    if not row["no"]:
                        continue
                    Talk.objects.create(
                        sessionize_id=row["id"],
                        day=row["day"],
                        no=row["no"],
                        room=row["room"],
                        title=row["title"],
                        description=row["description"],
                        elevator_pitch=row["elevator_pitch"],
                        talk_format=row["talk_format"],
                        category=row["track"],
                        audience_python_level=row["audience_python_level"],
                        audience_domain_expertise=row["audience_expertise"],
                        speaking_language=speak_language_converter[
                            row["lang_of_talk"]
                        ],
                        slide_language=slide_language_converter[
                            row["lang_of_slide"]
                        ],
                        prerequisite_knowledge=row["prerequisite_knowledge"],
                        audience_take_away=row["audience_takeaway"],
                    )
        print("loading done!")
