from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from .models import Question,Answer,UserAnswer
from .forms import UserResponseForm
# Create your views here.

def single(request,id):

	queryset = Question.objects.all().order_by('-timestamp') #.filter(full_name__iexact="Justin")
	instance = get_object_or_404(Question,id=id)
	try:
		user_answer = UserAnswer.objects.get(question=instance,user=request.user)
	except UserAnswer.DoesNotExist:
		user_answer = UserAnswer()
	except UserAnswer.MultipleObjectsReturned:
		user_answer = UserAnswer.objects.filter(question=instance,user=request.user)[0]
	except:
		user_answer = UserAnswer()

	if request.user.is_authenticated():
		form = UserResponseForm(request.POST or None)
		if form.is_valid():
			print "in form valid"
			print form.cleaned_data
			question_id = form.cleaned_data.get('question_id')
			answer_id = form.cleaned_data.get('answer_id')
			their_answer_id = form.cleaned_data.get('their_answer_id')
			my_answer_importance = form.cleaned_data.get('importance_level')
			their_answer_importance = form.cleaned_data.get('their_importance_level')
			question_instance =Question.objects.get(id=question_id)
			answer_instance = Answer.objects.get(id=answer_id)
			#print question_instance,answer_instance
			next_q = Question.objects.all().order_by("?").first()

			user_answer.user = request.user
			user_answer.question = question_instance
			user_answer.my_answer = Answer.objects.get(id=answer_id)
			user_answer.my_answer_importance = my_answer_importance

			if their_answer_id != -1:
				user_answer.their_answer = Answer.objects.get(id=their_answer_id)
				user_answer.their_answer_importance = their_answer_importance
			else:
				user_answer.their_answer = None
				user_answer.their_answer_importance = "Not Important"
			
			user_answer.save()
			return redirect('question_single',id=next_q.id)

		
		context = {
			"form": form,
			"instance":instance,
			"user_answer":user_answer
			#"queryset": queryset
		}
		return render(request, "questions/single.html", context)
	else:
		raise Http404


def home(request):

	if request.user.is_authenticated():
		form = UserResponseForm(request.POST or None)
		if form.is_valid():
			print "in form valid"
			print form.cleaned_data
			question_id = form.cleaned_data.get('question_id')
			answer_id = form.cleaned_data.get('answer_id')
			question_instance =Question.objects.get(id=question_id)
			answer_instance = Answer.objects.get(id=answer_id)
			print question_instance,answer_instance
		queryset = Question.objects.all().order_by('-timestamp') #.filter(full_name__iexact="Justin")
		instance = queryset[0]
		context = {
			"form": form,
			"instance":instance
			#"queryset": queryset
		}
		return render(request, "questions/home.html", context)
	else:
		raise Http404