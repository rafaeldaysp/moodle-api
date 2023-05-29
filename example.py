"""
    
Example code that initiates a session in Moodle and answers a quiz.

"""
from moodle import Moodle

##################### REQUIRED #####################
### Requirements to start a session ###

DOMAIN = 'yourInstituteDomain'
USERNAME = 'yourUserName'
PASSWORD = 'yourPassword'

####################################################

moodle = Moodle(domain=DOMAIN, username=USERNAME, password=PASSWORD)

moodle.startQuiz('30877') # Starts a quiz that you have access

moodle.answerQuestion(questionNumber='1', answer=1) # Question 1, value 1. (1 = True and 0 = False for True or False questions).
moodle.answerQuestion(questionNumber='2', answer=0) # Question 2, Alternative 0 (starting from 0. Answer=0 refers to the first alternative).
moodle.answerQuestion(questionNumber='3', answer=2) # Question 3, Alternative 2 (starting from 0. Answer=2 refers to the third alternative).
moodle.answerQuestion(questionNumber='4', answer=3) # Question 4, Alternative 3 (starting from 0. Answer=3 refers to the fourth alternative).

moodle.submitQuiz()