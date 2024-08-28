import csv
import datetime
from django.utils import timezone

from polls.models import Question, Choice

def run():
    print("=== Polls Loader")

    Choice.objects.all().delete()
    Question.objects.all().delete()
    print("=== Objects deleted")

    fhand = open('scripts/dj4e_batch.csv')
    reader = csv.reader(fhand)
    next(reader)

    for row in reader:
        print(row)

        question_text = row[0]

        question = Question(question_text=question_text, pub_date=timezone.now())
        question.save()
        print(f"Quesiton created: {question_text}")

        for choice_text in row[1:]:
            choice = Choice(question=question, choice_text=choice_text, votes=0)
            choice.save()
            print(f"Choice create: {choice_text}")


    print("=== Load Compelete")

