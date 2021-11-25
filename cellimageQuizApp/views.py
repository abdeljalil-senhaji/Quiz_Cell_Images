# from django.shortcuts import render
# Create your views here.

from random import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer, Image, Profile
from django.shortcuts import redirect, render
from .forms import form1
from .models import Image
# explore :
from django_filters import FilterSet, ModelChoiceFilter
import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
# Autocomplate :
from dal import autocomplete


# ******************* Information quiz *********************#

def information(request):
    return render(request, "information.html")


# *********************** create compte *************************#

def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})


# ******************** CONNECTED/DECONNECTED ***********************#

def index(request):
    if request.user.is_authenticated:
        return render(request, "registration/registered.html",
                      {"profile_user": Profile.objects.get(user_id=request.user.id)})
    else:
        return render(request, "registration/unregistered.html")


# ******************** Images explore  ********************#

# Django-filter : fournit un moyen simple de filtrer un ensemble de requêtes en fonction des paramètres fournis par l'utilisateur.
# Django-table2 :Une application pour créer des tableaux HTML

class FiltrationTableImages(FilterSet):
    image_name = ModelChoiceFilter(queryset=Image.objects.values_list('image_name', flat=True).distinct())
    microscopy = ModelChoiceFilter(queryset=Image.objects.values_list('microscopy', flat=True).distinct())

    class Meta:
        model = Image
        fields = ['id', 'image_name', 'description', 'microscopy', 'cell_type', 'component', 'doi', 'organism']


class ImagesAddInTable(tables.Table):
    class Meta:
        model = Image

    Image = tables.TemplateColumn(
        '<a href="/static/images/{{ record.image_name }}.jpg"><img src="/static/images/{{ record.image_name }}.jpg" width="80" height="80"></a>')


class FilteredImagesListView(SingleTableMixin, FilterView):
    table_class = ImagesAddInTable
    model = Image
    template_name = 'exploreimages.html'
    filterset_class = FiltrationTableImages


# *************************** START THE QUIZ ****************************** #


# getImages methode pour la filtration des images component et microscopy :
def getImages(id_trueAnswer, choiceCategory):
    Good_Answer = Answer.objects.get(id=id_trueAnswer).answer
    NbreImage = int(Question.objects.filter(category=choiceCategory).values()[0]["n_image"])
    if choiceCategory == "component":
        return Image.objects.filter(component=Good_Answer).order_by('?')[0:NbreImage]
    elif choiceCategory == "microscopy":
        return Image.objects.filter(microscopy=Good_Answer).order_by('?')[0:NbreImage]


class TrueAnswer:
    def __init__(self):
        self.IDtrueAnswer = None
    def setIDTrueAnswer(self, IDtrueAnswer):
        self.IDtrueAnswer = IDtrueAnswer
    def getIDTrueAnswer(self):
        return self.IDtrueAnswer
classGoodAnswer = TrueAnswer()

class currentImages:
    def __init__(self):
        self.images = None
    def setImages(self, images):
        self.images = images
    def getImages(self):
        return self.images
classImages = currentImages()

# la methode play quizz pour
def playquizz(request, choiceCategory):
    QuestionId = []
    id_questions = Question.objects.filter(category=choiceCategory)
    for i in range(len(id_questions)):
        QuestionId.append(id_questions.values()[i]["id"])
    questionIDcurrent = QuestionId[0]
    nmbAnswer = int(Question.objects.filter(id=questionIDcurrent).values()[0]["n_answer"])

    # ************** Add LOGIC FORM TO RESPONSE ***********#

    if request.method == "POST":  # envoie des données au serveur
        form = form1(request.POST, questionID=questionIDcurrent, number_answer=nmbAnswer)
        images = classImages.getImages()

        if form.is_valid():
            id_answer_submitted = int(form.data['answer'])
            id_current_user = request.user.id
            profile_currently = Profile.objects.get(user_id=id_current_user)
            id_trueAnswer = classGoodAnswer.getIDTrueAnswer()
            classGoodAnswer.setIDTrueAnswer(id_trueAnswer)
            # ******************** si les données sont valider en calcule le score *******************#
            if id_trueAnswer == id_answer_submitted:  # reponse true
                profile_currently.total_score += Question.objects.get(category=choiceCategory).points
                profile_currently.save()
                if choiceCategory == "component":
                    profile_currently.component_score += Question.objects.get(category=choiceCategory).points
                    profile_currently.save()
                elif choiceCategory == "microscopy":
                    profile_currently.microscopy_score += Question.objects.get(category=choiceCategory).points
                    profile_currently.save()
                user_answer = True

            else:  # reponse false
                profile_currently.total_score -= Question.objects.get(category=choiceCategory).points
                profile_currently.save()
                if choiceCategory == "component":
                    profile_currently.component_score -= Question.objects.get(category=choiceCategory).points
                    profile_currently.save()
                elif choiceCategory == "microscopy":
                    profile_currently.microscopy_score -= Question.objects.get(category=choiceCategory).points
                    profile_currently.save()
                user_answer = False
            form = form1(questionID=questionIDcurrent, number_answer=nmbAnswer)
            Good_Answer = form.returnTrueAnswer()
            id_trueAnswer = Answer.objects.get(answer=Good_Answer).id
            return render(request, "TwoQuiz.html", {"profile_user": Profile.objects.get(user_id=request.user.id),
                                                    "questions": Question.objects.filter(category=choiceCategory,
                                                                                         id=questionIDcurrent),
                                                    "images": getImages(id_trueAnswer, choiceCategory), 'form': form,
                                                    'successful_submit': True, 'user_answer': user_answer,
                                                    'true_answer': Answer.objects.get(id=id_trueAnswer).answer,
                                                    'answer_definition': Answer.objects.get(
                                                        id=id_trueAnswer).definition,
                                                    'categorycurrently': choiceCategory, 'images_currently': images})
    else:
        form = form1(questionID=questionIDcurrent, number_answer=nmbAnswer)
        Good_Answer = form.returnTrueAnswer()
        id_trueAnswer = Answer.objects.get(answer=Good_Answer).id
        classGoodAnswer.setIDTrueAnswer(id_trueAnswer)
        images = getImages(id_trueAnswer, choiceCategory)
        classImages.setImages(images)
        return render(request, "OneQuiz.html",
                      {"profile_user": Profile.objects.get(user_id=request.user.id),
                       "questions": Question.objects.filter(category=choiceCategory, id=questionIDcurrent),
                       "images": images,
                       'form': form,
                       'true_answer': Answer.objects.get(id=id_trueAnswer).answer,
                       'answer_definition': Answer.objects.get(id=id_trueAnswer).definition,
                       'categorycurrently': choiceCategory})


# ***************  Autocomplete :*********************

class Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Image.objects.none()
        qs = Image.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
