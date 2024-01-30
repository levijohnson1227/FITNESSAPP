import json
import pyrebase

with open('firebasekey.json') as f:
    firebase_config = json.load(f)

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()
auth = firebase.auth()
class FitnessTracker:
    
    def build_exercise_data(self, email, type, exercise_name, duration, calories):
        user_id = email.replace('.', '_dot_').replace('@', '_at_')

        user_ref = db.child('users').child(user_id)
        exercise_ref = user_ref.child('exercises').child(type)
        exercise_data = {
            'exercise_name': exercise_name,
            'duration': duration,
            'calories_burned': calories
        }
        exercise_ref.push(exercise_data)


    def update_exercise_data(self, email, type):
        user_id = email.replace('.', '_dot_').replace('@', '_at_')

        user_ref = db.child('users').child(user_id)
        exercise_ref = user_ref.child('exercises').child(type)
        exercises = exercise_ref.get()

        if exercises is not None and exercises.val() is not None:
            for exercise_id, exercise_data in exercises.val().items():
                # Bring in exercise information
                exercise_name = exercise_data.get('exercise_name')
                duration = exercise_data.get('duration')
                calories_burned = exercise_data.get('calories_burned')

                if exercise_name:
                    print(f"Exercise ID: {exercise_id}")
                    print(f"Exercise Name: {exercise_name}")
                    print(f"Duration: {duration}")
                    print(f"Calories Burned: {calories_burned}")
                    print()

            # Ask user for exercise name to update
            update_name = input("Enter the exercise name to update (or 'quit' to exit): ")

            while update_name.lower() != "quit":
                exercise_to_update = next(
                    (exercise_id for exercise_id, exercise_data in exercises.val().items()
                    if update_name.lower() in exercise_data.get('exercise_name').lower()))
                
                if exercise_to_update:
                    #update new duration and calories
                    new_duration = input("Enter new duration: ")
                    new_calories = input("Enter new calories burned:")

                    db.child('users').child(user_id).child('exercises').child(type).child(exercise_to_update).update({
                        'duration': new_duration,
                        'calories_burned': new_calories
                    })
                    print(f"Exercise '{update_name}' updated successfully!\n")
                else:
                    print(f"Exercise '{update_name}' not found.\n")

                update_name = input("Enter the exercise name to update (or 'quit' to exit): ")
        
        else:
            print("No exercises found matching that user and type.")

    def delete_exercise(self, email, type):

        user_id = email.replace('.', '_dot_').replace('@', '_at_')

        user_ref = db.child('users').child(user_id)
        exercise_ref = user_ref.child('exercises').child(type)
        exercises = exercise_ref.get()   

        if exercises is not None and exercises.val() is not None:
            #Show the user their current exercises
            print("Your Current Exercises:") 
            for exercise_id, exercise_data in exercises.val().items():
                exercise_name = exercise_data.get('exercise_name')
                print(f"{exercise_id}: {exercise_name}")

            delete_name = input("Enter the exercise name to delete (or 'quit' to exit): ")

            while delete_name.lower() != "quit":
                exercise_to_delete = next(
                    (exercise_id for exercise_id, exercise_data in exercises.val().items()
                    if delete_name.lower() in exercise_data.get('exercise_name').lower()))
                
                if exercise_to_delete:
                    db.child('users').child(user_id).child('exercises').child(type).child(exercise_to_delete).remove()
                else:
                    print(f"Exercise '{delete_name}' not found.\n")

                delete_name = input("Enter the exercise name to delete (or 'quit' to exit): ")

        else:
            print("No exercises found matching that user and type.")


                
        

        

class UserInteractions:
    #User Interactions
    print("Welcome to the Fitness Tracker!")
    print()
    print('Please select from one of the following: ')
    response=input('1. Sign up \n2. Login\n')
    accept = False
    #Sign_Up/Login
    if response == '1':
        email=input("Please provide an Email: ")
        password=input("Please provide a Password: ")
        conf_password=input('Please confirm your password: ')
        try:
            auth.create_user_with_email_and_password(email,password)
            print('User created successfully!')
            user_id = email
            accept = True
        except:
            ('Error with email or password')
    elif response =='2':
        email=input("Please enter your Email: ")
        password=input("Please enter your Password: ")
        try:
            auth.sign_in_with_email_and_password(email,password)
            print('Login Success!')
            user_id = email
            accept = True
            
        except:
            ('Invalid email or password')


#Submit exercise information
    if accept:
        #Build command interface
        print('Please select from the following options:')
        choice = input('1. Add Exercice \n2. Update Previous Exercise\n3. Remove Previous exercise\n4. Quit\n')
        while choice != "4":
            inner_loop = True

            while inner_loop:
                match choice:
                    #Submit exercise information
                    case "1":
                        tracker = FitnessTracker()
                        print('Please select what type of exercise you completed: ')
                        exercise= input('1. Cardio \n2. Weight Lifting\n3. Mobility\n4. Go back\n')
                        match exercise:
                            case '1':
                                email = user_id
                                type= "Cardio"
                                name=input('What was the exersice completed? ').lower()
                                duration=input('How long did you do the exercise for?(In minutes) ')
                                burned=input('How many calories were burned? ')
                            
                                tracker.build_exercise_data(email, type, name, duration, burned)
                            case '2':
                                email = user_id
                                type= "Weight Lifting"
                                name=input('What was the exersice completed? ').lower()
                                duration=input('How long did you do the exercise for?(In minutes) ')
                                burned=input('How many calories were burned? ')
                                
                                tracker.build_exercise_data(email, type, name, duration, burned)
                            case '3':
                                email = user_id
                                type= "Mobility"
                                name=input('What was the exersice completed? ').lower()
                                duration=input('How long did you do the exercise for?(In minutes) ')
                                burned=input('How many calories were burned? ')
                                
                                tracker.build_exercise_data(email, type, name, duration, burned)
                            case "4":
                                break
                    #Edit information           
                    case "2":
                        tracker = FitnessTracker()
                        print('What type of execise are you updating?')
                        q2exercise= input('1. Cardio \n2. Weight Lifting\n3. Mobility\n4. Go back\n')
                        match q2exercise:
                            case "1":
                                email = user_id
                                type = "Cardio"
                                tracker.update_exercise_data(email, type)
                            case "2":
                                email = user_id
                                type = "Weight Lifting"
                                tracker.update_exercise_data(email, type)
                            case "3":
                                email = user_id
                                type = "Mobility"
                                tracker.update_exercise_data(email, type)
                            case "4":
                                break
                    #Remove information
                    case "3":
                        tracker = FitnessTracker()
                        print('What type of execise do you want to remove?')
                        q3exercise= input('1. Cardio \n2. Weight Lifting\n3. Mobility\n4. Go back\n')
                        match q3exercise:
                            case "1":
                                email = user_id
                                type = "Cardio"
                                tracker.delete_exercise(email, type)
                            case "2":
                                email = user_id
                                type = "Weight Lifting"
                                tracker.delete_exercise(email, type)
                            case "3":
                                email = user_id
                                type = "Mobility"
                                tracker.delete_exercise(email, type)
                            case "4":
                                break
            choice = input('1. Add Exercice \n2. Update Previous Exercise\n3. Remove Previous exercise\n4. Quit\n')

        print('Thank you for using the fitness tracker! Have a wonderful day!')

                        










