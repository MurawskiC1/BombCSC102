import random

class Question:
    def __init__(self, question, options, correct_answer):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer

    def shuffle_options(self):
        # If correct answer is already in options, remove it temporarily
        if self.correct_answer in self.options:
            self.options.remove(self.correct_answer)
        # Include the correct answer in the options before shuffling
        options_with_correct_answer = self.options + [self.correct_answer]
        # Shuffle the options randomly
        random.shuffle(options_with_correct_answer)
        # Update the options attribute with the shuffled list
        self.options = options_with_correct_answer

    def display_question(self):
        print(self.question)
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option}")

    def get_correct_answer(self):
        # Search for the index of the correct answer in the options
        correct_index = self.options.index(self.correct_answer)
        # Return the index + 1 (to match user input numbering)
        return correct_index + 1

def main():
    # Example questions
    q1 = Question("What is the capital of France?", ["Berlin", "Paris", "London", "Madrid"], "Paris")
    q2 = Question("Which planet is the fourth going from the sun?", ["Earth", "Mars", "Venus", "Jupiter"], "Mars")
    q3 = Question("What is the largest mammal?", ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], "Blue Whale")
    q4 = Question("Which one of these presidents wasn't shot in office?", ["Lincoln", "Roosevelt", "Garfield"], "Adams")
    q5 = Question("Choose one of the following doors, only one can you survive", [" A bear that just ate cocaine", " Three velociraptor that hasn't eaten in three days", "Batman with a killing rule"], "A tiger that hasn't eaten in five weeks")
    q6 = Question(" What is the capital of Russia?", [ "St.Petersburg","Berlin","Kursk"], " Moscow")
    q7 = Question(" How many offical sports teams does University of Tampa have?", ["17", "26", "13"], "20")
    q8 = Question(" University of Tampa as of now has what percentage acceptance rate ?", ["48%", "56%", "58%"], "54%")
    q9 = Question( " Which of these presidents was seventh US president?", [" Theodore Roosevelt", " Abraham Lincoln", " Henry Ford"], "Andrew Jackson")
    q10 = Question(" If I gave you the binary represensation of 00101001 what is the value ?", [ " 36", "56", "48"], "41")
 

    # List of questions
    questions = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]

    while questions:
        # Randomly select a question
        selected_question = random.choice(questions)

        # Shuffle the options for the selected question
        selected_question.shuffle_options()

        # Display the question and options
        selected_question.display_question()

        # Get user input for the answer
        user_answer_index = int(input("Enter the number corresponding to your answer: "))

        # Validate the answer
        correct_answer = selected_question.get_correct_answer()
        if user_answer_index == correct_answer:
            print("Correct!\n")
            # End the loop if the answer is correct
            break
        else:
           print(f"Incorrect.Now you have to answer another question")
     
#The correct answer is: {selected_question.correct_answer}\n")
    print("Congratulations! You answered the last question correctly.")

if __name__ == "__main__":
    main()