import json
import nltk

nltk.download('punkt')

def find_start_index(context, answer):
    context_tokens = nltk.word_tokenize(context)
    answer_tokens = nltk.word_tokenize(answer)

    # Join tokens to form strings for counting characters
    context_text = ' '.join(context_tokens)
    answer_text = ' '.join(answer_tokens)

    # Find the starting index of the answer in the context
    start_index = context_text.find(answer_text)
    
    return start_index if start_index != -1 else -1

def generate_squad_format(context, qa_pairs):
    squad_data = [
        {
            "context": context,
            "qas": qa_pairs
        }
    ]
    return squad_data

# Taking input for context
user_context = input("Enter the context: ")

qa_pairs = []
while True:
    user_question = input("Enter the question or type 'no' if there are no more questions: ")
    if user_question.lower() == 'no':
        break

    user_answer = input("Enter the answer: ")

    # Find the starting index of the answer in the context
    answer_start = find_start_index(user_context, user_answer)
    if answer_start == -1:
        print("Answer not found in the context.")
        continue

    # Construct the QA pair for the original question
    qa_pair = {
        "id": str(len(qa_pairs) + 1),
        "is_impossible": False,
        "question": user_question,
        "answers": [
            {
                "text": user_answer,
                "answer_start": answer_start
            }
        ]
    }

    qa_pairs.append(qa_pair)

    paraphrased_questions = []  # Store paraphrased questions for this answer
    while True:
        add_paraphrased = input("Do you want to enter a paraphrased question (yes/no)? ")
        if add_paraphrased.lower() == 'no':
            break

        paraphrased_question = input("Enter the paraphrased question: ")
        paraphrased_questions.append({
            "id": str(len(paraphrased_questions) + 1),
            "is_impossible": False,
            "question": paraphrased_question,
            "answers": [
                {
                    "text": user_answer,
                    "answer_start": answer_start
                }
            ]
        })

    qa_pairs.extend(paraphrased_questions)  # Extend with paraphrased questions

# Generate SQuAD-like JSON format based on the inputs
generated_data = generate_squad_format(user_context, qa_pairs)

# Write the generated_data to a file named 'generated_squad.json'
with open('generated_squad.json', 'w') as json_file:
    json.dump(generated_data, json_file, indent=2)
