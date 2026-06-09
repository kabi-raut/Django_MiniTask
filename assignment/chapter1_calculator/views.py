from django.shortcuts import render
import random


def index(request):
    """Display calculator and number guessing game menu"""
    return render(request, 'chapter1_calculator/index.html')


def calculator_page(request):
    """Display calculator interface"""
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1', 0))
            num2 = float(request.POST.get('num2', 0))
            operation = request.POST.get('operation', '')

            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = num1 / num2
            elif operation == 'power':
                result = num1 ** num2
            elif operation == 'modulo':
                if num2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = num1 % num2
        except ValueError:
            result = "Error: Invalid input"

    return render(request, 'chapter1_calculator/calculator.html', {'result': result})


def guessing_game(request):
    """Number guessing game"""
    message = None
    game_won = False

    if request.method == 'POST':
        try:
            secret_number = int(request.session.get('secret_number', random.randint(1, 100)))
            request.session['secret_number'] = secret_number

            guess = int(request.POST.get('guess', 0))

            if guess == secret_number:
                message = f"🎉 Congratulations! You guessed it right! The number was {secret_number}"
                game_won = True
                del request.session['secret_number']
            elif guess < secret_number:
                message = f"Too low! Try a higher number."
            else:
                message = f"Too high! Try a lower number."
        except ValueError:
            message = "Please enter a valid number"
    else:
        # Initialize game
        request.session['secret_number'] = random.randint(1, 100)

    return render(request, 'chapter1_calculator/guessing_game.html', {
        'message': message,
        'game_won': game_won
    })


def reset_game(request):
    """Reset guessing game"""
    if 'secret_number' in request.session:
        del request.session['secret_number']
    return render(request, 'chapter1_calculator/guessing_game.html', {
        'message': None,
        'game_won': False
    })
