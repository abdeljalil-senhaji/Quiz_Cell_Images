from django import forms
from .models import Answer
import random


# formulaire des réponses pour la quiz

# Create the form class.
class form1(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        questionID = kwargs.pop('questionID')
        number_answer = kwargs.pop('number_answer')
        super(form1, self).__init__(*args, **kwargs)
        all_id_answers = list(Answer.objects.values_list('id', flat=True).filter(question_id=questionID))
        random_id = random.sample(all_id_answers, number_answer)
        answers_for_form = Answer.objects.filter(id__in=random_id)
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

    def returnTrueAnswer(self):
        return self.trueAnswer
