
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    current_question = get_question_by_id(current_question_id)
    if not current_question:
        return False, "Invalid question ID."
    if not current_question.is_valid_answer(answer):
        return False, "Invalid answer. Please try again."
    if 'answers' not in session:
        session['answers'] = {}
    session['answers'][current_question_id] = answer
    session.modified = True
    return True, "Your answer has been recorded!"
def get_question_by_id(question_id):
    from yourapp.models import Question
    try:
        return Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return None

# Assuming PYTHON_QUESTION_LIST is a list of dictionaries or objects with 'id' and 'question' keys/attributes
PYTHON_QUESTION_LIST = [
    {"id": 1, "question": "What is Python?"},
    {"id": 2, "question": "Explain the difference between list and tuple in Python."},
    {"id": 3, "question": "What is a dictionary in Python?"},
    # Add more questions as needed
]

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    current_index = -1
    for index, question in enumerate(PYTHON_QUESTION_LIST):
        if question['id'] == current_question_id:
            current_index = index
            break
    if current_index == -1:
        return "Invalid current question ID", -1
    next_index = current_index + 1
    if next_index < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_index]
        return next_question['question'], next_question['id']
    else:
        return "You have completed the quiz!", -1
current_question_id = 2
next_question, next_question_id = get_next_question(current_question_id)
print(next_question, next_question_id)


def generate_final_response(session):
    if 'answers' not in session or not session['answers']:
        return "No answers provided. Please complete the quiz first."
    user_answers = session['answers']
    score = 0
    total_questions = len(PYTHON_QUESTION_LIST)
    for question in PYTHON_QUESTION_LIST:
        question_id = question['id']
        correct_answer = question['correct_answer']
        if question_id in user_answers and user_answers[question_id].strip().lower() == correct_answer.strip().lower():
            score += 1
    response = f"Quiz completed! Your score: {score}/{total_questions}.\n"
    for question in PYTHON_QUESTION_LIST:
        question_id = question['id']
        correct_answer = question['correct_answer']
        user_answer = user_answers.get(question_id, "No answer provided")

        response += f"\nQuestion: {question['question']}\n"
        response += f"Your answer: {user_answer}\n"
        response += f"Correct answer: {correct_answer}\n"

    return response


session = {
    'answers': {
        1: "A programming language",
        2: "Lists are mutable, tuples are immutable",
        3: "A collection of key-value pairs"
    }
}
final_response = generate_final_response(session)
print(final_response)

