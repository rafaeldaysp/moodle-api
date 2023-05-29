import requests
import json

class Moodle():
    def __init__(self, domain : str, username: str, password: str) -> None:
        self.domain = domain
        self.apiUrl = self.domain +'/webservice/rest/server.php?moodlewsrestformat=json'
        
        self.login(username=username, password=password)

    def __getToken(self, username : str, password : str) -> str:
        loginURL = self.domain + '/login/token.php?service=moodle_mobile_app'
        
        r = requests.post(loginURL, data={
            'username': username,
            'password': password
        })

        token = json.loads(r.content)
        token = token['token']
        return token

    def __getUserId(self, token : str) -> str:
        url = self.domain + '/webservice/rest/server.php?moodlewsrestformat=json'
        r = requests.post(url, data={
            'wstoken': token,
            'wsfunction': 'core_webservice_get_site_info'
        })
        data = json.loads(r.content)
        userId = data['userid']
        return userId
    
    def login(self, username: str, password: str) -> bool:
        try:
            self.__token = self.__getToken(username=username, password=password)
            self.__userId = self.__getUserId(token=self.__token)
            return True
        except:
            return False
    
    def getUserCourses(self) -> dict:
        payload = {
            'wstoken': self.__token,
            'userid': self.__userId,
            'wsfunction': 'core_enrol_get_users_courses'
        }
        r = requests.post(self.apiUrl, data=payload)
        userCourses = json.loads(r.content)
        return userCourses
    
    def __getQuizAttemptStatus(self, quizId : str, attemptId : str) -> bool:
        
        payload = {
            'wstoken': self.__token,
            'wsfunction': 'mod_quiz_get_attempt_access_information',
            'attemptid': attemptId,
            'quizid': quizId
        }
        r = requests.post(self.apiUrl, data=payload)
        isFinished = json.loads(r.content)['isfinished']
        return isFinished

    # In development... (This function would aim to display the answers that the user selected before submitting.)
    def __getAttemptSumamry(self, attemptId: str) -> dict:
        payload = {
            'wstoken': self.__token,
            'wsfunction': 'mod_quiz_get_attempt_summary',
            'attemptid': attemptId
        }
        
        r = requests.post(self.apiUrl, data=payload)
        return json.loads(r.content)
    
    # In development... ( This function would aim to display all the questions of a specific quiz for user)
    def __getQuiz(self, quizId, attemptId):
        payload = {
            'wstoken': self.__token,
            'wsfunction': 'mod_quiz_get_attempt_summary',
            'attemptid': attemptId
        }
    
    def getCourseQuizzes(self, courseId : str) -> dict:
        payload = {
            'wstoken': self.__token,
            'wsfunction': 'mod_quiz_get_quizzes_by_courses',
            'courseids[0]': courseId
        }
        r = requests.post(self.apiUrl, data=payload)
        quizzes = json.loads(r.content)['quizzes']
        return quizzes

    # Inicia a tentativa do quiz. Essa função não irá funcionar caso o usuário já tenha iniciado uma tentativa.
    def startQuiz(self, quizId : str) -> dict:
        payload = {
            'wstoken': self.__token,
            'wsfunction': 'mod_quiz_start_attempt',
            'quizid': quizId
        }
        r = requests.post(self.apiUrl, data=payload)
        # print(r.content)
        # if 'exception' in json.loads(r.content):
        #     payload['userid'] = self.__userId
        #     payload['wsfunction'] = 'mod_quiz_get_user_attempts'
        #     r = requests.post(self.apiUrl, data=payload)
        print(r.content)
        quiz = json.loads(r.content)
        self.quizAttempt = quiz['attempt']['id']
        self.uniqueQuizId = quiz['attempt']['uniqueid']
        
        return quiz

    # Aqui é a função do quiz./
    def answerQuestion(self, questionNumber : str, answer: int, isAttemptFinished : int = 0) -> dict:
        payload = {
            'wstoken': self.__token,
            'wsfunction': 'mod_quiz_process_attempt',
            'attemptid': self.quizAttempt,
            'data[0][name]' : f'q{self.uniqueQuizId}:{questionNumber}_:sequencecheck',
            'data[0][value]' : 1,  # começa em 1 e aumenta para cada vez que a questão é respondida
            'data[1][name]' : f'q{self.uniqueQuizId}:{questionNumber}_answer',
            'data[1][value]' : answer, # começa em 0 para a primeira opção. 1 significa a segunda opção, e assim por diante...
            'finishattempt': 0 # 0 para não finalizar, 1 para finalizar
        }
        
        r = requests.post(self.apiUrl, data=payload)
        print(r.content)
        return json.loads(r.content)

    def submitQuiz(self):
        payload = {
            'wstoken': self.__token,
            'wsfunction': 'mod_quiz_process_attempt',
            'attemptid': self.quizAttempt,
            'finishattempt': 1
        }
        
        r = requests.post(self.apiUrl, data=payload)
        return json.loads(r.content)
    
