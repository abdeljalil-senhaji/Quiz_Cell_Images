# from django.shortcuts import render

# Create your views here.
from random import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Answer, Image, Profile
from django.shortcuts import redirect, render
from .forms import FormAnswer
from .models import Image
# explore :
from django_filters import FilterSet, ModelChoiceFilter
import django_tables2 as tables
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from dal import autocomplete



#***************  Autocomplete :*********************

class ImagesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Image.objects.none()
        qs = Image.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

#******************* Information quiz *********************#

def information(request):
    return render(request, "information.html")


#*********************** create compte *************************#

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


#*********** CONNECTED/DECONNECTED ************#

def index(request):
    if request.user.is_authenticated:
        return render(request, "registration/registered.html",
                      {"profile_user": Profile.objects.get(user_id=request.user.id)})
    else:
        return render(request, "registration/unregistered.html")


#******************** Images explore  ********************#

# Django-filter :
# fournit un moyen simple de filtrer un ensemble de requêtes en fonction des paramètres fournis par l'utilisateur.

# Django-table2 :Une application pour créer des tableaux HTML

from django_filters import FilterSet, ModelChoiceFilter
import django_tables2 as tables



class ImageFilter(FilterSet):
    # autocompletion
    image_name = ModelChoiceFilter(queryset=Image.objects.values_list('image_name', flat=True).distinct())
    microscopy = ModelChoiceFilter(queryset=Image.objects.values_list('microscopy', flat=True).distinct())

    class Meta:
        model = Image
        fields = ['id', 'image_name', 'description', 'microscopy', 'cell_type', 'component', 'doi', 'organism']


class ImageTable(tables.Table):
    class Meta:
        model = Image

    Image = tables.TemplateColumn(
        '<a href="/static/images/{{ record.image_name }}.jpg"><img src="/static/images/{{ record.image_name }}.jpg" width="80" height="80"></a>')


class FilteredImagesListView(SingleTableMixin, FilterView):
    table_class = ImageTable
    model = Image
    template_name = 'exploreimages.html'
    filterset_class = ImageFilter


#*************************** Quiz ******************************#


# getImages methode pour la filtration des images component et microscopy :
def getImages(id_trueAnswer, choiceCategory):
    trueAnswer = Answer.objects.get(id=id_trueAnswer).answer
    nb_images = int(Question.objects.filter(category=choiceCategory).values()[0]["n_image"])
    if choiceCategory == "component":
        return Image.objects.filter(component=trueAnswer).order_by('?')[0:nb_images]
    elif choiceCategory == "microscopy":
        return Image.objects.filter(microscopy=trueAnswer).order_by('?')[0:nb_images]


class TrueAnswer:
    def __init__(self):
        self.IDtrueAnswer = None

    def setIDTrueAnswer(self, IDtrueAnswer):
        self.IDtrueAnswer = IDtrueAnswer

    def getIDTrueAnswer(self):
        return self.IDtrueAnswer


classTrueAnswer = TrueAnswer()  # l'avoir en variable globale


class currentImages:
    def __init__(self):
        self.images = None

    def setImages(self, images):
        self.images = images

    def getImages(self):
        return self.images


classCurrentImages = currentImages()  # l'avoir en variable globale


# --------------------------------------------------------------------------------

# la methode play quizz pour
def playquizz(request, choiceCategory):
    # choiceCategory: le type de quizz
    # case of a classic quizz:

    choiceCategorySave = ["microscopy", "component"]
    # supremer l'element choisCategory
    del choiceCategorySave[choiceCategorySave.index(choiceCategory)]
    # a supprimer apres
    if choiceCategory == "classic":
        choiceCategory = random.choice(["microscopy", "component"])  # choice pour affichir soit microscopy ou component

    # Select the question of this category
    list_idQuestions = []
    id_questions = Question.objects.filter(category=choiceCategory)
    for i in range(len(id_questions)):
        list_idQuestions.append(id_questions.values()[i]["id"])
    questionIDcurrent = list_idQuestions[0]  # une question ID = une seule catégorie, donc catégorie sous-entendu

    # Number of choices of answer to display
    nb_answer = int(Question.objects.filter(id=questionIDcurrent).values()[0]["n_answer"])

    #### FORM TO RESPONSE ###

    if request.method == "POST":
        form = FormAnswer(request.POST, questionID=questionIDcurrent, number_answer=nb_answer)

        # conserver les images actuelles:
        images = classCurrentImages.getImages()

        if form.is_valid():  # procéder à la validation et renvoyer une valeur booléenne indiquant si les données sont valides
            id_answer_submitted = int(form.data['answer'])
            # Retrieve Profile DB of the gamer
            id_current_user = request.user.id  # user id of the gamer
            profile_currently = Profile.objects.get(user_id=id_current_user)

            id_trueAnswer = classTrueAnswer.getIDTrueAnswer()

            ####################### calculate score ################################################################

            if id_trueAnswer == id_answer_submitted:  # User responde correctly
                profile_currently.total_score += Question.objects.get(category=choiceCategory).points  # change field
                profile_currently.save()  # this will update only
                if choiceCategory == "component":
                    profile_currently.component_score += Question.objects.get(
                        category=choiceCategory).points  # change field
                    profile_currently.save()  # this will update only
                elif choiceCategory == "microscopy":
                    profile_currently.microscopy_score += Question.objects.get(
                        category=choiceCategory).points  # change field
                    profile_currently.save()  # this will update only
                user_answer = True

            else:  # User is wrong
                profile_currently.total_score -= Question.objects.get(category=choiceCategory).points  # change field
                profile_currently.save()  # this will update only
                if choiceCategory == "component":
                    profile_currently.component_score -= Question.objects.get(
                        category=choiceCategory).points  # change field
                    profile_currently.save()  # this will update only
                elif choiceCategory == "microscopy":
                    profile_currently.microscopy_score -= Question.objects.get(
                        category=choiceCategory).points  # change field
                    profile_currently.save()  # this will update only
                user_answer = False

            ################################################################################################

            # New form for the following question
            form = FormAnswer(questionID=questionIDcurrent, number_answer=nb_answer)  # on fait d'abord le formulaire
            trueAnswer = form.returnTrueAnswer()
            id_trueAnswer = Answer.objects.get(answer=trueAnswer).id

            classTrueAnswer.setIDTrueAnswer(id_trueAnswer)

            return render(request, "TwoQuiz.html", {"profile_user": Profile.objects.get(user_id=request.user.id),
                                                    "questions": Question.objects.filter(category=choiceCategory,
                                                                                         id=questionIDcurrent),
                                                    "images": getImages(id_trueAnswer, choiceCategory), 'form': form,
                                                    'successful_submit': True, 'user_answer': user_answer,
                                                    'true_answer': Answer.objects.get(id=id_trueAnswer).answer,
                                                    'answer_definition': Answer.objects.get(
                                                        id=id_trueAnswer).definition,
                                                    'otherCategories': choiceCategorySave,
                                                    'category_currently': choiceCategory, 'images_currently': images})


    # pour la 1ère soumission:
    else:
        # 1ère formulaire
        form = FormAnswer(questionID=questionIDcurrent, number_answer=nb_answer)  # on fait d'abord le formulaire
        trueAnswer = form.returnTrueAnswer()
        id_trueAnswer = Answer.objects.get(answer=trueAnswer).id
        classTrueAnswer.setIDTrueAnswer(id_trueAnswer)

        # save currently images
        images = getImages(id_trueAnswer, choiceCategory)
        classCurrentImages.setImages(images)

        return render(request, "OneQuiz.html",
                      {"profile_user": Profile.objects.get(user_id=request.user.id),
                       "questions": Question.objects.filter(category=choiceCategory, id=questionIDcurrent),
                       "images": images,
                       'form': form,
                       'true_answer': Answer.objects.get(id=id_trueAnswer).answer,
                       'answer_definition': Answer.objects.get(id=id_trueAnswer).definition,
                       'otherCategories': choiceCategorySave,
                       'category_currently': choiceCategory})
