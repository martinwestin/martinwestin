stages = [ """
     ------------
    |           |
    |           O
    |          \\|/
    |           |
    |          / \\
    --
    """, 
    """
     ------------
    |           |
    |           O
    |          \\|/
    |           |
    |         
    --
    """, 
    """
     ------------
    |           |
    |           O
    |          \\|
    |           
    |          
    --
    """,
    """
     ------------
    |           |
    |           O
    |           |
    |           
    |          
    --
    """, 
    """
     ------------
    |           |
    |           O
    |           
    |           
    |          
    --
    """, 
    """
     ------------
    |           |
    |           
    |           
    |           
    |          
    --
    """
]

def play(word):
    word = word.upper()
    guesses = 6
    guessed = False
    under_scores = "_"*len(word)
    right_letters = []
    guessed_letters = []
    while not guessed:
        guess = input("Enter letter: ").upper()
        if len(guess) != 0:
            if guess not in list(map(lambda x: x[0], guessed_letters)):
                for i in range(len(word)):
                    right_letters.append([word[i], i]) if word[i] == guess else None
                    under_scores = "".join(list(map(lambda x: x if [i for i in word].index(x) in list(map(lambda x: x[1], right_letters)) else "_", [i for i in word])))
                
                if guess in word:
                    print("Correct")
                else:
                    print("Wrong")
                    guesses -= 1
                    if guesses == 0:
                        print(stages[guesses], "\n", "Out of guesses")
                        break
                
                print(stages[guesses]) if guesses < 6 else None
                print(under_scores)
                guessed_letters.append(guess) if guess not in guessed_letters else None

            else:
                print("You have already guessed that letter.")
            
            guessed = True if len(right_letters) == len(word) else False
        else:
            print("Invalid input")
    
    else:
        print(f'You guessed the word "{word}"')

if __name__ == "__main__":
    play("word")
