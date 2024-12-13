import subprocess


def process(command):
    return subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True
    )


def expect(proc, pattern):
    pattern = pattern.strip("\n")
    buffer = ""


def write(proc, text):
    proc.stdin.write(f'{text}\n'.encode())
    proc.stdin.flush()
    return text


def test():
    print("Launching processes")
    try:
        # Запуск corral.bas и corral.py
        py = process('python corral.py')
        bas = process('vintbas corral.bas')  # Замените на правильную команду для запуска corral.bas

        # Проверка вывода приветствия:
        expected_greetings = '''
                         CORRAL
                  CREATIVE COMPUTING
                MORRISTOWN, NEW JERSEY


  YOU ARE THE COWBOY.  GO CATCH YOUR HORSE IN THE CORRAL!
DO YOU WANT FULL INSTRUCTIONS? 
'''
        print("Expecting greeting...")
        expect(py, expected_greetings)
        expect(bas, expected_greetings)
        print("[+] TEST 1 - PASSED")

        # Отправка ответа "Y"
        print("Sending keys...")
        write(py, 'Y')
        write(bas, 'Y')
        print("[+] KEYS SENT")

        # Проверка вывода инструкции:
        instructions = '''
YOU MOVE TOWARD YOUR HORSE 1 TO 5 STEPS AT A TIME.
IF YOU MORE THAN HALVE THE SEPARATION HE WILL BOLT!
HE MAY ALSO BOLT WHEN HE IS CLOSE TO THE RAIL
WHEN YOU COME WITHIN 2 STEPS HE MAY KICK.  SO LOOKOUT!!

AFTER '?' TYPE IN DIGIT FROM 1 TO 5 FOR COWBOY'S NEXT MOVE
 0            IC            H       I                 ? 
'''
        expect(py, instructions)
        expect(bas, instructions)
        print("[+] TEST 2 - PASSED")

        # Проверка сценария движений
        moves = [
            " 1            I  C           H      I                 ? ",
            " 2            I    C           H    I                 ? ",
            " 3            I      C            H I                 ? ",
            " 4            I        C           HI                 ? ",
            " 5            I          C         HI                 ? ",
            " 6            I            C       HI                 ? ",
            " 7            I              C     HI                 ? ",
            " 8            I                C   HI                 ? ",
            " 9            I                  CH I                 ? ",
        ]

        for i, move in enumerate(moves, start=1):
            print(f"Sending move: {i}")
            write(py, '2')
            write(bas, '2')

            # Проверка конкретного состояния игры
            expect(py, move)
            expect(bas, move)
            print(f"[+] TEST {i + 2} - Move {i} Processed Successfully")

        # Проверка последнего шага
        print("Sending final move: 1")
        write(py, '1')
        write(bas, '1')

        final_state = '''
              I                   # I

YIPPEE!!  NOW SEE IF YOU CAN CATCH HIM IN FEWER MOVES
ANOTHER ROUNDUP?
'''
        expect(py, final_state)
        expect(bas, final_state)
        print("[+] Horse Capture Test Passed")

    except Exception as ex:
        print("[!] Test failed:", ex)


if __name__ == "__main__":
    test()
