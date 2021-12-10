import random

######################## Rules ###############################
#       if guess outside range return "OUT OF BOUNDS!"       #
#       if guess within 10 range return "WARM!"              # 
#       if guess LESS THAN prev guess return "WARMER!"       #  
#       if guess GREATER THAN prev guess return "COLDER!"    # 
######################## END OF RULES ########################

def guess_number(lower, upper):
    return random.randint(lower, upper)


lower, upper = input("Enter number guess range: ").split()
guess_num = guess_number(int(lower),int(upper))
guess_count = 1
user_num = 0
prev_guess = 0

while user_num!=guess_num:

    user_num = int(input("Enter your {} guess: ".format(guess_count)))
    if abs(user_num-guess_num)<=10 and prev_guess==0:
        print("WARM!")
        prev_guess = user_num
    elif abs(user_num-guess_num)>10 and prev_guess==0:
        print("COLD!")
        prev_guess = user_num
    elif abs(user_num-guess_num) < abs(prev_guess-guess_num):
        if user_num==guess_num:
            print("Well Done! You guessed right in {} tries.".format(guess_count))
            break
        print("WARMER!")
        prev_guess = user_num
    elif abs(user_num-guess_num) > abs(prev_guess-guess_num):
        print("COLDER!")
        prev_guess = user_num
    guess_count+=1


