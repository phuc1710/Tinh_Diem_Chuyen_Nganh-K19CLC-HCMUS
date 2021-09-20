from tkinter import *
from tkinter import messagebox
import math

# Main window intialization
root = Tk()
root.title("Tính điểm xét tuyển CLC K2019")

# Main window screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(
    "960x540+"
    + str(int((screen_width - 960) / 2))
    + "+"
    + str(int((screen_height - 540) / 2))
)
icon = PhotoImage(file="logo_hcmus.png")
root.iconphoto(False, icon)
root.resizable(False, False)

# Main window background config
root.configure(bg="white")

# Set of subject names, credits and scores
subject_names_and_credits = [
    ["Nhập môn công nghệ thông tin", 4],
    ["Nhập môn lập trình", 4],
    ["Toán rời rạc", 4],
    ["Kỹ thuật lập trình", 4],
    ["Vi tích phân 1", 4],
    ["Vật lý đại cương 1 (Cơ - Nhiệt)", 4],
    ["Phương pháp lập trình hướng đối tượng", 4],
    ["Vi tích phân 2", 4],
    ["Đại số tuyến tính", 4],
    ["Cấu trúc dữ liệu và giải thuật", 4],
    ["Hệ thống máy tính", 2],
    ["Toán học tổ hợp", 4],
    ["Cơ sở dữ liệu", 4],
    ["Mạng máy tính", 4],
    ["Xác suất thống kê", 4],
    ["Hệ điều hành", 4],
    ["Nhập môn công nghệ phần mềm", 4],
    ["Vật lý đại cương 2", 4],
    ["Cơ sở trí tuệ nhân tạo", 4],
    ["Toán ứng dụng và thống kê", 4],
]
subject_score_entries = []
subject_scores = []


def get_subject_scores_from_entries():
    subject_scores.clear()
    for i in range(len(subject_score_entries)):
        if subject_score_entries[i].get() == "":
            subject_scores.append(0)
        else:
            try:
                subject_scores.append(float(subject_score_entries[i].get()))
            except ValueError:
                messagebox.showinfo(
                    title="Cảnh báo!!", message="Điểm phải từ 0 đến 10."
                )
                return False
    return True


def insert_scores_from_file():
    with open("score.txt", "r") as f:
        score_str = f.read()
    score_lst_from_file = score_str.split(",")

    return score_lst_from_file


def calculate_and_save(event=None):
    total_score = 0
    total_fixed_credits = 78
    total_earned_credits = 0
    total_earned_it_credits = 0
    it_subject = [1, 3, 6, 9, 10, 12, 13, 15, 16, 18]
    get_score_bool = get_subject_scores_from_entries()
    if get_score_bool == False:
        return
    for i in range(len(subject_scores)):
        if subject_scores[i] < 0.0 or subject_scores[i] > 10:
            messagebox.showinfo(title="Cảnh báo!!",
                                message="Điểm phải từ 0 đến 10.")
            return
        total_earned_credits += (
            subject_names_and_credits[i][1] if subject_scores[i] >= 5 else 0
        )
        total_earned_it_credits += (
            subject_names_and_credits[i][1]
            if i in it_subject and subject_scores[i] != 0
            else 0
        )
        total_score += (
            subject_scores[i] * subject_names_and_credits[i][1]
            if subject_scores[i] >= 5
            else 0
        )
    result_78_lb.config(
        text="Điểm xét tuyển (tổng số 78 tín chỉ): "
        + "%.2f" % round(total_score / total_fixed_credits, 2)
    )
    result_74_lb.config(
        text="Điểm xét tuyển (tổng số 74 tín chỉ): "
        + "%.2f" % round(total_score / (total_fixed_credits - 4), 2)
    )
    result_cre_lb.config(
        text="Điểm xét tuyển (tổng số tín chỉ đã tích lũy): "
        + "%.2f" % round(total_score / total_earned_credits, 2)
        if total_earned_credits > 0
        else "Điểm xét tuyển (tổng số tín chỉ đã tích lũy): 0.00"
    )
    cre_it_lb.config(
        text="Tổng số tín chỉ chuyên ngành đã tích lũy: "
        + str(total_earned_it_credits)
        + "/38"
    )
    cre_lb.config(
        text="Tổng số tín chỉ đã tích lũy: " +
        str(total_earned_credits) + "/78"
    )
    # Save score to text file
    with open("score.txt", "w") as f:
        f.write(",".join([str(score) for score in subject_scores]))


# Padding label
padding_lb = Label(root, bg="white", bd=0).grid(
    column=0, row=0, columnspan=4, sticky="news"
)

# Label and corresponding entry
subjects_count = len(subject_names_and_credits)
score_from_file = insert_scores_from_file()
for i in range(subjects_count):
    subject_lb = Label(
        root, text=subject_names_and_credits[i][0], bg="white", bd=0)
    subject_et = Entry(root, width=10)
    subject_et.bind("<Return>", calculate_and_save)
    if i < math.floor(subjects_count / 2):
        subject_lb.grid(column=0, row=i + 1, pady=5, padx=70, sticky="w")
        subject_et.grid(column=1, row=i + 1, pady=5, padx=30, sticky="w")
        if i == 0:
            subject_et.focus()
    else:
        subject_lb.grid(
            column=2,
            row=math.floor(i - subjects_count / 2) + 1,
            pady=5,
            padx=50,
            sticky="w",
        )
        subject_et.grid(
            column=3,
            row=math.floor(i - subjects_count / 2) + 1,
            pady=5,
            padx=70,
            sticky="w",
        )
    subject_score_entries.append(subject_et)
    if score_from_file:
        if score_from_file[i] != "0.0" and score_from_file[i] != "0":
            subject_et.insert(0, score_from_file[i])


# Button to submit and calculate
submit_bt = Button(
    root, text="Tính điểm xét tuyển & lưu điểm vào file", command=calculate_and_save
)
submit_bt.grid(
    column=0,
    row=math.floor(subjects_count / 2) + 1,
    columnspan=4,
    pady=10,
    ipady=5,
    ipadx=200,
)

# Label for displaying the result
result_78_lb = Label(root, text="", bg="white")
result_78_lb.grid(column=0, row=math.floor(
    subjects_count / 2) + 2, padx=20, sticky="w")
result_74_lb = Label(root, text="", bg="white")
result_74_lb.grid(column=0, row=math.floor(
    subjects_count / 2) + 3, padx=20, sticky="w")
result_cre_lb = Label(root, text="", bg="white")
result_cre_lb.grid(
    column=0, row=math.floor(subjects_count / 2) + 4, padx=20, sticky="w"
)
cre_it_lb = Label(root, text="", bg="white")
cre_it_lb.grid(column=0, row=math.floor(
    subjects_count / 2) + 5, padx=20, sticky="w")
cre_lb = Label(root, text="", bg="white")
cre_lb.grid(column=0, row=math.floor(
    subjects_count / 2) + 6, padx=20, sticky="w")

info_lb = Label(root, text="ver 1.0.1 by phuc1710", bg="white")
info_lb.grid(row=math.floor(subjects_count / 2) +
             7, columnspan=4, pady=50, sticky="e")

root.mainloop()
