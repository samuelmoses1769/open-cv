import cv2
import mediapipe as mp
import time
from tkinter import *
import numpy as np
import xlsxwriter

class handDetector:
    def __init__(self):
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands()
        self.mpdraw = mp.solutions.drawing_utils
        self.tips = [4, 8, 12, 16, 20]
        self.names = ["Thumb", "Index", "Middle", "Ring", "Small"]
        self.list = []
        self.label = ""
        self.prev_fingers = [0, 0, 0, 0, 0]

    def finddetector(self, frame, draw=True):
        self.frame = cv2.flip(frame, 1)
        self.img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(self.img)
        if self.result.multi_hand_landmarks:
            for handlms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(
                        self.frame, handlms, self.mphands.HAND_CONNECTIONS,
                        landmark_drawing_spec=self.mpdraw.DrawingSpec(color=(0, 0, 255)),
                        connection_drawing_spec=self.mpdraw.DrawingSpec(color=(0, 255, 0))
                    )
        return self.frame

    def findlocation(self, img, draw=True):
        self.list = []
        if self.result.multi_hand_landmarks:
            for handlms, handedness in zip(self.result.multi_hand_landmarks, self.result.multi_handedness):
                self.label = handedness.classification[0].label
                for id, lm in enumerate(handlms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.list.append([id, cx, cy])
                    if draw:
                        cv2.circle(self.frame, (cx, cy), 5, (255, 0, 255), -1)
        return self.list

    def finger(self):
        self.fingers = []
        if len(self.list) != 0:
            for i in self.tips:
                if i == 4:
                    if self.label == "Right":
                        if self.list[i][1] < self.list[i - 1][1]:
                            self.fingers.append(1)
                        else:
                            self.fingers.append(0)
                    else:
                        if self.list[i][1] > self.list[i - 1][1]:
                            self.fingers.append(1)
                        else:
                            self.fingers.append(0)
                else:
                    if self.list[i][2] < self.list[i - 2][2]:
                        self.fingers.append(1)
                    else:
                        self.fingers.append(0)
        return self.fingers, self.label

def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]

    return None

def on_click(row, col):
    global player, winner, data
    if buttons[row][col]["text"] == "" and winner is None:
        buttons[row][col]["text"] = player
        board[row][col] = player
        data.append({
            "Hand": current_label,
            "Thumb": current_fingers[0],
            "Index": current_fingers[1],
            "Middle": current_fingers[2],
            "Ring": current_fingers[3],
            "Small": current_fingers[4]
        })
        win = check_winner()
        if win:
            result_label.config(text=f"Player {win} wins!")
        elif all(board[i][j] != "" for i in range(3) for j in range(3)):
            result_label.config(text="It's a tie!")
        else:
            player = "O" if player == "X" else "X"
            result_label.config(text=f"Player {player}'s turn")

def map_fingers_to_cell(fingers, label):
    """Map the number of raised fingers to a specific Tic-Tac-Toe cell."""
    if label == "Left":
        if fingers == [0, 1, 0, 0, 0]:
            return 0, 0  # Top-left (1)
        elif fingers == [0, 1, 1, 0, 0]:
            return 0, 1  # Top-middle (2)
        elif fingers == [0, 1, 1, 1, 0]:
            return 0, 2  # Top-right (3)
        elif fingers == [0, 1, 1, 1, 1]:
            return 1, 0  # Middle-left (4)
        elif fingers == [1, 1, 1, 1, 1]:
            return 1, 1  # Center (5)
    elif label == "Right":
        if fingers == [0, 1, 0, 0, 0]:
            return 1, 2  # Middle-right (6)
        elif fingers == [0, 1, 1, 0, 0]:
            return 2, 0  # Bottom-left (7)
        elif fingers == [0, 1, 1, 1, 0]:
            return 2, 1  # Bottom-middle (8)
        elif fingers == [0, 1, 1, 1, 1]:
            return 2, 2  # Bottom-right (9)
    return None, None  # Invalid gesture

def video_loop():
    global frame, ctime, ptime, current_fingers, current_label

    success, frame = cap.read()
    if success:
        frame = detector.finddetector(frame)
        list = detector.findlocation(frame, draw=False)

        if len(list) != 0:
            current_fingers, current_label = detector.finger()
            row, col = map_fingers_to_cell(current_fingers, current_label)
            if row is not None and col is not None:
                on_click(row, col)

        # Display the frame
        cv2.imshow("Hand Tracking", frame)

    window.after(10, video_loop)

def save_to_excel():
    workbook = xlsxwriter.Workbook("TicTacToeHandGestures.xlsx")
    worksheet = workbook.add_worksheet("GesturesLog")

    # Write headers
    worksheet.write(0, 0, "Hand")
    worksheet.write(0, 1, "Thumb")
    worksheet.write(0, 2, "Index")
    worksheet.write(0, 3, "Middle")
    worksheet.write(0, 4, "Ring")
    worksheet.write(0, 5, "Small")

    # Write data
    for index, entry in enumerate(data):
        worksheet.write(index + 1, 0, entry["Hand"])
        worksheet.write(index + 1, 1, entry["Thumb"])
        worksheet.write(index + 1, 2, entry["Index"])
        worksheet.write(index + 1, 3, entry["Middle"])
        worksheet.write(index + 1, 4, entry["Ring"])
        worksheet.write(index + 1, 5, entry["Small"])

    workbook.close()

# Initialize the Tic-Tac-Toe game
window = Tk()
window.title("Tic-Tac-Toe")

player = "X"
winner = None
board = [["" for _ in range(3)] for _ in range(3)]
data = []
current_fingers = []
current_label = ""

buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = Button(window, text="", font=('normal', 40), width=5, height=2,
                               command=lambda i=i, j=j: on_click(i, j))
        buttons[i][j].grid(row=i, column=j)

result_label = Label(window, text=f"Player {player}'s turn", font=('normal', 20))
result_label.grid(row=3, column=0, columnspan=3)

# Initialize MediaPipe hand detection and OpenCV
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 740)
detector = handDetector()

# Start video loop for hand tracking
video_loop()

# Run the Tkinter main loop
window.protocol("WM_DELETE_WINDOW", lambda: [save_to_excel(), window.destroy()])
window.mainloop()

# Release the video capture
cap.release()
cv2.destroyAllWindows
