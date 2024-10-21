import mediapipe as mp
import cv2
import time
import random

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def calculate_game_state(player_move):
    moves = ["Rock", "Paper", "Scissors"]
    computer_move = random.choice(moves)
    
    if player_move == computer_move:
        return 0, computer_move
    elif (player_move == "Rock" and computer_move == "Scissors") or (player_move == "Paper" and computer_move == "Rock") or (player_move == "Scissors" and computer_move == "Paper"):
        return 1, computer_move
    return -1, computer_move

def start_video():
    capture = cv2.VideoCapture(0)
    timer_started, hold_to_play = False, False
    countdown = 3
    result = ""

    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
        while True:
            if timer_started:
                if countdown <= 0:
                    hold_to_play = True
                    timer_started = False
                else:
                    time.sleep(1)
                    countdown -= 1
            
            ret, frame = capture.read()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    index_finger = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
                    middle_finger = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
                    ring_finger = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
                    pinky = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y

                    if not index_finger and not middle_finger and not ring_finger and not pinky:
                        move = "Rock"
                    elif index_finger and middle_finger and ring_finger and pinky:
                        move = "Paper"
                    elif index_finger and middle_finger and not ring_finger and not pinky:
                        move = "Scissors"

                if hold_to_play:
                    hold_to_play = False
                    won, comp_move = calculate_game_state(move)
                    if won == 1:
                        result = f"You win! You: {move}, Computer: {comp_move}"
                        result_color = (0, 255, 0)
                    elif won == -1:
                        result = f"You lose! You: {move}, Computer: {comp_move}"
                        result_color = (0, 0, 255)
                    else:
                        result = f"Draw! You: {move}, Computer: {comp_move}"
                        result_color = (0, 255, 255)

            label_text = "START!" if not hold_to_play else "PLAY!"
            if timer_started:
                label_text = f"{countdown}"

            if result != "":
                cv2.putText(frame, result, (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, result_color, 2)

            cv2.putText(frame, label_text, (150, 50), cv2.FONT_HERSHEY_COMPLEX, 1, 2)
            cv2.imshow('Rock Paper Scissors!', frame)

            key = cv2.waitKey(1)
            if key == 32:
                timer_started, countdown = True, 3
            elif key == 27:
                break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_video()