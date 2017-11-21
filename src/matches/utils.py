from questions.models import UserAnswer,Question
from decimal import *
from django.db.models import Q



def get_match(user_a,user_b):
	q1 = Q(useranswer__user=user_a)
	q2 = Q(useranswer__user=user_b)
	question_set = Question.objects.filter(q1 | q2).distinct()
	questions_in_common =0
	b_points = 0
	b_total_points = 0
	a_points = 0
	a_total_points = 0
	

	for question in question_set:
		try:
			a = UserAnswer.objects.get(user=user_a,question=question)
		except:
			a = None
		try:
			b = UserAnswer.objects.get(user=user_b,question=question)
		except:
			b = None
  		
		if(a and b):
			questions_in_common +=1
			print "a their and b my"
			print a.their_answer,b.my_answer
			if a.their_answer == b.my_answer:
				print "in first"
				b_points += a.their_points
			b_total_points += a.their_points
			print "b their and a my answer"
			print b.their_answer,a.my_answer
			if b.their_answer == a.my_answer:
				print "in second"
				a_points += b.their_points
			a_total_points += b.their_points
	print a_points,a_total_points,b_points,b_total_points

	if(questions_in_common > 0):
		a_decimal = a_points/Decimal(a_total_points)
		b_decimal = b_points/Decimal(b_total_points)
		print a_decimal,b_decimal
		if a_decimal == 0:
			a_decimal = 0.000001
		if b_decimal == 0:
			b_decimal = 0.000001
		print Decimal(a_decimal) * Decimal(b_decimal)
		match_percentage = (Decimal(a_decimal) * Decimal(b_decimal))**(1/Decimal(questions_in_common))
		return match_percentage,questions_in_common
	else:
		return 0.0,0


def get_points(user_a,user_b):
	print "in get_points"
	a_answers = UserAnswer.objects.filter(user=user_a)
	b_answers = UserAnswer.objects.filter(user=user_b)
	a_total_awarded = 0
	a_points_possible = 0
	percent =0
	num_question = 0
	for a in a_answers:
		for b in b_answers:
			if a.question.id == b.question.id:
				num_question+=1
				a_pref = a.their_answer
				b_answer = b.my_answer
				#print a_pref
				#print b_answer
				if a_pref == b_answer:
					'''awards points for correct answer'''
					#print "points awarded " + str(a_total_awarded)
					a_total_awarded+=a.their_points
				'''assigning total points'''
				a_points_possible+=a.their_points
			# sys.stdout.write("{} has awarded {} points out of {} to {}".format(
			# a.user.username,a_total_awarded,a_points_possible,b.user.username) + "\n")
	#print a_total_awarded,a_points_possible
	if percent == 0:
		percent = 0.00001
		
	percent = a_total_awarded/Decimal(a_points_possible)

	return percent,num_question


# def get_match(user_a,user_b):
# 	a = get_points(user_a,user_b)
# 	b = get_points(user_b,user_a)
# 	print a
# 	print b
# 	number_of_questions = b[1]
# 	match_decimal = (Decimal(a[0])*Decimal(b[0]))**(1/Decimal(b[1]))
# 	return match_decimal,number_of_questions



#match_percentage = "{.2f} ".format((Decimal(a[0])*Decimal(b[0])) **(1/Decimal(b[1])))
#print match_percentage