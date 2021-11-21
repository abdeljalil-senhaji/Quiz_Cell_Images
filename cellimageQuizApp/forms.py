from django import forms
from .models import Answer, Image, Question
import random
from dal import autocomplete


class FormAnswer(forms.ModelForm):  # formulaire des réponses

    def __init__(self, *args, **kwargs):
        questionID = kwargs.pop('questionID')
        number_answer = kwargs.pop('number_answer')
        super(FormAnswer, self).__init__(*args, **kwargs)

        # tirer aléatoirement dans les réponses sachant que la question est déjà sélectionnée à partir du type de quizz
        all_id_answers = list(Answer.objects.values_list('id', flat=True).filter(question_id=questionID))
        random_id = random.sample(all_id_answers, number_answer)
        answers_for_form = Answer.objects.filter(id__in=random_id)  # id = [a list]

        self.trueAnswer = Answer.objects.get(id=random_id[0]).answer
        self.fields['answer'] = forms.ModelMultipleChoiceField(
            required=True,
            queryset=answers_for_form,
            widget=forms.RadioSelect)

    class Meta:
        model = Answer
        fields = ()

    def is_valid(self):
        if 'answer' in self.errors:
            del self._errors['answer']
        return self

    def returnTrueAnswer(self):  # conserver la bonne réponse à cocher
        return self.trueAnswer


#######################################################
##### Edit Image DB directly in admin interface #######
#######################################################


class FormImage(forms.ModelForm):  # Use the view in a Form widget
    class Meta:
        model = Image
        fields = '__all__'
        widgets = {
            'image_name': autocomplete.ListSelect2(url='images-autocomplete')
        }
