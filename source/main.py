def instruction():
    print(" " * 26 + "CORRAL")
    print(" " * 20 + "CREATIVE COMPUTING")
    print(" " * 18 + "MORRISTOWN, NEW JERSEY")
    print("\n\n")
    print("  YOU ARE THE COWBOY.  GO CATCH YOUR HORSE IN THE CORRAL!")

    if input("DO YOU WANT FULL INSTRUCTIONS? ").strip().lower().startswith("n"):
        print("AFTER '?' TYPE IN DIGIT FROM 1 TO 5 FOR COWBOY'S NEXT MOVE")
        print()
    else:
        print("YOU MOVE TOWARD YOUR HORSE 1 TO 5 STEPS AT A TIME.")
        print("IF YOU MORE THAN HALVE THE SEPARATION HE WILL BOLT!")
        print("HE MAY ALSO BOLT WHEN HE IS CLOSE TO THE RAIL")
        print("WHEN YOU COME WITHIN 2 STEPS HE MAY KICK.  SO LOOKOUT!!")
        print()
        print("AFTER '?' TYPE IN DIGIT FROM 1 TO 5 FOR COWBOY'S NEXT MOVE")
        print()
def main():
    o=0

    DIM_A = [" "] * 21  # Empty corral
    S = [[0, 1, 2, 3, 3, 2, 2, 1, 0, -1], [1, 2, 3, 4, 5, 4, 3, 2, 1, 0]]

    C, L, K, H, N = 1, 1, 0, 0, 0  # Initialize variables
    R_sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Fixed sequence for R
    R_index = 0  # Index to iterate through R_sequence

    def random_event():
        nonlocal R_index
        R = R_sequence[R_index % len(R_sequence)]
        R_index += 1
        return S[0][R], S[1][R]

    while True:
        P, Q = random_event()
        if R_index % len(R_sequence) > 5:
            Q = -Q

        H = max(1, min(21, 13 + Q))  # Ensure H is within bounds
        T = 2 + P

        while True:
            DIM_A = [" "] * 21
            DIM_A[C - 1] = "C"
            DIM_A[H - 1] = "H"
            game_row = "".join(DIM_A)
            output = f" {N:<3}          I{game_row}I                "

            X = abs(H - C)
            L = 1 if H > C else -1

            if K > 0:
                if N > T:
                    print("\n  THOSE KICKS LANDED YOU IN THE HOSPITAL!")
                    print("  GET WELL SOON!!")
                    return
                K -= 1
                P, _ = random_event()
                H += L * (P + 1)
                H = max(1, min(21, H))  # Ensure H is within bounds
                continue

            N += 1
            if N > 100:
                print("\n  ENOUGH!! YOU'D DO BETTER AS CAMP COOK!")
                return

            if o==0:
                print(output + " ? ", end="")
            else:
                o=0

            try:
                D = int(input().strip())
            except ValueError:
                print("ILLEGAL MOVE. TRY AGAIN")
                continue

            if D < 1 or D > 5:
                print("ILLEGAL MOVE. TRY AGAIN")
                continue

            E = C + L * D
            if E < 1 or E > 21:
                print("ILLEGAL MOVE. TRY AGAIN")
                continue

            C = E
            P, Q = random_event()

            G = P
            H += L * G
            H = max(1, min(21, H))  # Ensure H is within bounds

            if X < 2 * D and D > 1:
                G = 9 + 2 * P
                H -= L * G
                L = -L
                H = max(1, min(21, H))

                DIM_A = [" "] * 21
                DIM_A[C - 1] = "C"
                DIM_A[H - 1] = "H"
                game_row = "".join(DIM_A)

                print(f"{N:<3}            I{game_row}I     BOLTED      ? ", end="")
                o=1
                continue

            if abs(H - C) > 2:
                continue

            if R_index % len(R_sequence) > 3:
                print(f"{N:<3}            I{game_row}I     KICKED      ? ")
                K = P + 2
                H -= 5 * L
                H = max(1, min(21, H))  # Ensure H is within bounds
                continue

            if H == C:
                for j in range(21):
                    DIM_A[j] = " "
                DIM_A[C - 1] = "#"
                game_row = "".join(DIM_A)
                output = f"              I{game_row}I"
                print(output)
                print("\nYIPPEE!!  NOW SEE IF YOU CAN CATCH HIM IN FEWER MOVES")
                print("\nANOTHER ROUNDUP? ", end="")
                a=input()
                if a=="Y":
                    main()
                else:
                    return


if __name__ == "__main__":
    instruction()
    main()
