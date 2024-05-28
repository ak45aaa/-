import tkinter
import cv2
import numpy as np
from paddleocr import PaddleOCR

ocr_ = PaddleOCR()
image = cv2.imread('True_answer.jpg') # 답지
T_answer = ocr_.ocr(image)
true_answer = sum(T_answer, [])
answer_data = [data[1] for data in true_answer]

def mapping_answer(answer):
    A = []
    P = []
    for i in range(len(answer)):
        if i % 2 == 0:
            P.append(answer[i][0])
        else:
            A.append(answer[i][0])
            
    mapped_dict = dict(zip(P, A))
    return mapped_dict
            
map_dict = mapping_answer(answer_data)

window = tkinter.Tk()
window.title('Problem Awareness and Scoring AI Model')
window.geometry('640x400+100+100')
window.resizable(True, True)

label = tkinter.Label(window, text='문제 번호를 입력해주세요', width=20, height=3, fg='blue', relief='flat')
label.pack()

def make_bounding_box(problem):
    M_index = 0
    m_index = 100000
    M_column = 0
    m_column = 100000
    
    for i in range(len(problem)):
        if problem[i][0] > M_index:
            M_index = problem[i][0]
        if problem[i][0] < m_index:
            m_index = problem[i][0]
        if problem[i][1] > M_column:
            M_column = problem[i][1]
        if problem[i][1] < m_column:
            m_column = problem[i][1]
            
    return M_index+10, m_index, M_column, m_column

def checking_problem_answer(ProblemNumber):
    image1 = cv2.imread('image/personal_answer.jpg') # 문항이 체크되어있는 이미지
    image2 = cv2.imread('image/original.jpg') # 비교할 원본이미지
    
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    diff = cv2.absdiff(gray1, gray2)
    
    _, diff_thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    non_zero_indices = np.argwhere(diff_thresh != 0)
    non_zero_indices_list = [tuple(index) for index in non_zero_indices]
    
    num_list = []
    for temp in range(len(non_zero_indices_list)):
        if temp == 0:
            continue
        elif abs(non_zero_indices_list[temp][0] - non_zero_indices_list[temp-1][0]) > 100 or abs(non_zero_indices_list[temp][1] - non_zero_indices_list[temp-1][1]) > 100:
            num_list.append(temp)
        else:
            continue
              
    problem_2 = non_zero_indices_list[:num_list[0]]
    problem_3 = non_zero_indices_list[num_list[0]:num_list[1]]
    problem_1 = non_zero_indices_list[num_list[1]:]
    problems = [problem_1, problem_2, problem_3]
    
    M_idx, m_idx, M_col, m_col = make_bounding_box(problems[int(entry.get())-1])
    
    ocr = PaddleOCR()
    test = gray2[m_idx:M_idx, m_col:M_col]
    result = ocr.ocr(test)
    
    circle_num = ['①','②','③','④','⑤']
    for data in result[0]:
        if data[1][0] in circle_num:
            personal_answer = data[1][0]
            
    if map_dict[entry.get()] == personal_answer:
        label.config(text='{}번의 정답은 {}번 이고 사용자가 체크한 답은 {}번 입니다. 정답입니다!'.format(int(entry.get()), map_dict[entry.get()], personal_answer))
    else:
        label.config(text='{}번의 정답은 {}번 이고 사용자가 체크한 답은 {}번 입니다. 틀렸습니다.'.format(int(entry.get()), map_dict[entry.get()], personal_answer))
    
    
entry = tkinter.Entry(window)
entry.bind('<Return>', checking_problem_answer)
entry.pack()

label = tkinter.Label(window)
label.pack()

window.mainloop()