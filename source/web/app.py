from flask import Flask, render_template, request
import sys
from multiprocessing import Process
from time import sleep
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import corral  # Подключение вашей игры "CORRAL"

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        # Получение ввода от пользователя через веб-интерфейс
        user_input = request.form.get('user_input')
        if user_input:
            write_f('input.txt', user_input)
            sleep(1)  # Небольшая пауза для обработки

    if not os.path.exists('print.txt'):
        write_f('print.txt', '')

    # Чтение текущего вывода игры
    game_output = read_f('print.txt')
    return render_template('play.html', text=game_output)

def background_worker():
    """
    Фоновый процесс для запуска игры.
    """
    def input_handler(prompt=""):  # Сделаем `prompt` необязательным
        write_f('print.txt', prompt + '\n')
        while True:
            sleep(1)
            if os.path.exists('input.txt'):
                user_input = read_f('input.txt')
                os.remove('input.txt')
                return user_input

    if os.path.exists('input.txt'):
        os.remove('input.txt')
    if os.path.exists('print.txt'):
        os.remove('print.txt')

    def custom_print(*args, end='\n'):
        message = ' '.join(map(str, args)) + end
        write_f('print.txt', message)

    corral.input = input_handler  # Указываем, что `input` должен использовать `prompt`
    corral.print = custom_print

    corral.instruction()  # Вызов инструкций перед началом игры
    corral.main()

def read_f(file):
    sleep(0.5)
    with open(file, 'r') as f:
        return f.read()

def write_f(file, text):
    with open(file, 'a') as f:
        f.write(text)

if __name__ == '__main__':
    if not os.path.exists('print.txt'):
        write_f('print.txt', '')

    process = Process(target=background_worker)
    process.start()

    app.run(debug=True)
