import csv
import os.path
from django.core.management.base import BaseCommand
# from django.http import HttpResponse

from cellimageQuizApp.models import Question, Answer, Image


# class Command(BaseCommand):


def importData():
    # CSV file path name and Read files
    my_path = os.path.abspath(os.path.dirname(__file__))
    path_Q = os.path.join(my_path, "./data_app/table_questions.csv")
    path_A = os.path.join(my_path, "./data_app/table_answers.csv")
    path_I = os.path.join(my_path, "./data_app/table_images.csv")
    # Read files :
    reader_Q = csv.reader(open(path_Q, encoding='utf-8'), delimiter='\t', quotechar='"')
    next(reader_Q)  # Remove the first line (header)
    for row in reader_Q:  # Parse files
        question = Question()
        question.question = row[1]
        question.category = row[2]
        question.imageField = row[3]
        question.points = row[4]
        question.n_answer = row[5]
        question.n_image = row[6]
        question.save()
    reader_A = csv.reader(open(path_A, encoding='utf-8'), delimiter='\t', quotechar='"')
    next(reader_A)
    for row in reader_A:
        answer = Answer()
        answer.question_id = row[1]
        answer.answer = row[2]
        answer.definition = row[3]
        answer.save()
    reader_I = csv.reader(open(path_I, encoding='utf-8'), delimiter='\t', quotechar='"')
    next(reader_I)
    for row in reader_I:
        image = Image()
        image.image_name = row[1]
        image.description = row[2]
        image.microscopy = row[3]
        image.cell_type = row[4]
        image.component = row[5]
        image.doi = row[6]
        image.organism = row[7]
        image.save()

    # return HttpResponse("<p>All table is imported.</p>")
