import re

from django.db import models


day_no_to_start_map = {
    (1, 1): "11:50",
    (1, 2): "13:45",
    (1, 3): "14:50",
    (1, 4): "16:00",
    (1, 5): "16:50",
    (1, 6): "18:00",
    (2, 1): "11:50",
    (2, 2): "14:00",
    (2, 3): "14:50",
    (2, 4): "16:00",
    (2, 5): "16:30",
}


class Talk(models.Model):
    class Room(models.TextChoices):
        PYCONJP = "#pyconjp"
        PYCONJP_1 = "#pyconjp_1"
        PYCONJP_2 = "#pyconjp_2"
        PYCONJP_3 = "#pyconjp_3"
        PYCONJP_4 = "#pyconjp_4"
        PYCONJP_5 = "#pyconjp_5"

    class TalkFormat(models.TextChoices):
        TALK_45MIN = "Talk(45min)"
        TALK_30MIN = "Talk(30min)"
        TALK_15MIN = "Talk(15min)"
        HANDSON_SESSION = "Hands-on session(45min)"

    class TalkCategory(models.TextChoices):
        PYTHON_CORE = "Python core"
        TIPS_PYTHON_DEVELOPMENT = "Tips of development with Python"
        WEB_PROGRAMMING = "Web programming (including web frameworks)"
        DATA_AND_ML = "Data Science / Machine Learning"
        SYSTEM_ADMINISTRATION = "System administration"
        CASE_STUDIES = (
            "Case studies (excluding web programming or machine learning)"
        )
        EMBEDDING = "Embedding python in hardware"
        GUI_GAMES = "GUI and games"
        NETWORK_PROGRAMMING = "Network programming"
        FINTECH = "Fintech"
        EDUCATION = "Python in education"
        COMMUNITY = "Community building related to Python"
        OTHERS = (
            "Anything else basically which doesn’t fall into the types "
            "of topics above"
        )

    class AudienceLevel(models.TextChoices):
        BEGINNER = "Beginner"
        INTERMEDIATE = "Intermediate"
        ADVANCED = "Advanced"
        EXPERT = "Expert"

    class DomainExpertise(models.TextChoices):
        NOVICE = "0%"
        PRACTITIONER = "50%"
        PROFESSIONAL = "100%"

    class SpeakingLanguage(models.TextChoices):
        JAPANESE = "ja", "Japanese"
        ENGLISH = "en", "English"

    class SlideLanguage(models.TextChoices):
        JAPANESE = "ja", "Japanese only"
        ENGLISH = "en", "English only"
        BOTH = "bo", "Both"

    sessionize_id = models.PositiveIntegerField("SessionizeにおけるID")
    day = models.PositiveIntegerField("トークする日（◯日目）")
    no = models.PositiveIntegerField("トーク時間帯の番号")
    room = models.CharField("トークのトラック", max_length=10, choices=Room.choices)
    title = models.CharField("トークのタイトル", max_length=100)
    description = models.TextField("詳細（タイムライン）")
    elevator_pitch = models.TextField("概要（エレベータピッチ）")
    talk_format = models.CharField(
        "トークの持ち時間", max_length=23, choices=TalkFormat.choices
    )
    category = models.CharField(
        "トークのカテゴリ", max_length=73, choices=TalkCategory.choices
    )
    audience_python_level = models.CharField(
        "聴衆に求めるPythonのレベル", max_length=12, choices=AudienceLevel.choices
    )
    audience_domain_expertise = models.CharField(
        "聴衆に求めるトークの分野の知識レベル", max_length=4, choices=DomainExpertise.choices
    )
    speaking_language = models.CharField(
        "発表の言語", max_length=2, choices=SpeakingLanguage.choices
    )
    slide_language = models.CharField(
        "スライドの言語", max_length=2, choices=SlideLanguage.choices
    )
    prerequisite_knowledge = models.TextField("聴衆に求める前提知識")
    audience_take_away = models.TextField("聴衆が持ち帰ることができるもの")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sessionize_id} {self.day}日目 {self.title}"

    def start_at(self):
        return day_no_to_start_map[(self.day, self.no)]

    def duration(self):
        matched_durations = re.findall(r"\((.*min)\)", self.talk_format)
        return matched_durations[0]
