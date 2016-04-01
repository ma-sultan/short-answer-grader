''' This program trains a ridge regression model from the training examples in
    the directory "Sample Train Data" '''

from featureExtraction import *
import ridgeModel


def read_questions():

    train_dir = 'Sample Train Data'    
    questions_file = train_dir + '/questions'

    questions = {}
    f = open(questions_file, 'rb')
    for line in f:
        line = line.strip()
        question_num = line.split(' ')[0]
        question_text = ' '.join(line.split(' ')[1:])
        questions[question_num] = question_text
    f.close()

    return questions


def read_reference_answers():

    train_dir = 'Sample Train Data'    
    ref_answers_file = train_dir + '/reference answers'

    ref_answers = {}
    f = open(ref_answers_file, 'rb')
    for line in f:
        line = line.strip()
        answer_num = line.split(' ')[0]
        answer_text = ' '.join(line.split(' ')[1:])
        ref_answers[answer_num] = answer_text
    f.close()

    return ref_answers


def read_student_responses(question_num):

    train_dir = 'Sample Train Data'    
    student_responses_file = \
                    train_dir + '/student responses ' + str(question_num)
    
    student_responses = []
    f = open(student_responses_file, 'rb')
    for line in f:
        line = line.strip()
        response_num = line.split(' ')[0]
        response_text = ' '.join(line.split(' ')[1:])
        student_responses.append(response_text)
    f.close()
        
    return student_responses


def read_scores(question_num):

    train_dir = 'Sample Train Data'    
    scores_file = train_dir + '/scores ' + str(question_num)
    
    scores = []
    f = open(scores_file, 'rb')
    for line in f:
        line = line.strip()
        score = float(line)
        scores.append(score)
    f.close()
        
    return scores


def read_train_data():
    
    train_data = {}    
    
    questions = read_questions()
    ref_answers = read_reference_answers()
    
    for question_num in questions:
        
        student_responses = read_student_responses(question_num)
        scores = read_scores(question_num)
        
        train_data[question_num] = (questions[question_num],
                                    ref_answers[question_num],
                                    student_responses,
                                    scores)

    return train_data
    

def extract_features(question, ref_answer, student_response):
    
    sim_alignment, cov_alignment, parse_results = \
                            sts_alignment(ref_answer, student_response)
    
    q_demoted_sim_alignment, q_demoted_cov_alignment, _ = \
                            sts_alignment(ref_answer, student_response,
                                          parse_results,
                                          question)

    sim_cvm = sts_cvm(ref_answer, student_response, parse_results)
    
    q_demoted_sim_cvm = sts_cvm(ref_answer, student_response,
                                parse_results,
                                question)
    
    lr = length_ratio(ref_answer, student_response, parse_results)    


    feature_vector = (sim_alignment, cov_alignment,
                      q_demoted_sim_alignment, q_demoted_cov_alignment,
                      sim_cvm,
                      q_demoted_sim_cvm,
                      lr)
    
    return feature_vector
    

def construct_train_examples(train_data):

    train_examples = []
    
    train_data = read_train_data()
    
    n = 0
    
    for question_num in train_data:
        data_for_this_question = train_data[question_num]
        question = data_for_this_question[0]
        ref_answer = data_for_this_question[1]
        student_answers = data_for_this_question[2]
        scores = data_for_this_question[3]
        for i in xrange(len(student_answers)):
            features = extract_features(question, ref_answer,
                                        student_answers[i])
            score = scores[i]
            train_examples.append((features, score))
            
            n += 1
            print n,

    return train_examples
    
    
def train_grader(train_examples):
    
    model = ridgeModel.train_model([item[0] for item in train_examples],
                                   [item[1] for item in train_examples])
                                   
    return model
    

def grade(question, ref_answer, student_response, grader):
              
    features = extract_features(question, ref_answer, student_response)
    
    score = ridgeModel.predict(grader, [features])[0]
    
    return score
    
    



print 'reading train data from files...'
train_data = read_train_data()
print 'done.'
print

print 'extracting features and constructing training examples...'
train_examples = construct_train_examples(train_data)
print 'done.'
print

print 'training the grading model...'
grader = train_grader(train_examples)
print 'done.'
print

question = "What is a variable?"
ref_answer = "A location in memory that can store a value."
student_response = "In programming, a structure that holds data and is " + \
                   "uniquely named by the programmer. It holds the data " + \
                   "assigned to it until a new value is assigned or the " + \
                   "program is finished."

score = grade(question, ref_answer, student_response, grader)
print score