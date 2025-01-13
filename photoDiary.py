from tkinter import *  # tkinter GUI 라이브러리 임포트
from tkcalendar import Calendar  # 달력 위젯을 위한 라이브러리
from tkinter.filedialog import asksaveasfilename  # 파일 저장을 위한 다이얼로그
from tkinter.colorchooser import askcolor  # 색상 선택을 위한 다이얼로그
from tkinter.simpledialog import askinteger  # 정수 입력을 위한 다이얼로그
from PIL import ImageGrab, Image, ImageDraw, ImageFont  # 이미지 처리 라이브러리 (Pillow)
import datetime  # 날짜와 시간 처리
import ctypes
import tkinter as tk


# 전역 변수 선언
x1, y1, x2, y2 = None, None, None, None  # 마우스 좌표 초기화 (선 그리기 위한 변수)
diary_window = None
penColor = 'black'  # 기본 펜 색상
penWidth = 5  # 기본 펜 두께
eraserWidth = 10  # 기본 지우개 두께
isEraserMode = False  # 지우개 모드 초기화
previousPenColor = penColor  # 펜 색상 저장
previousPenWidth = penWidth  # 펜 두께 저장
line_objects = []  # 선의 시작/끝 좌표와 색상, 두께 등을 저장할 리스트


#화면 색상 조정---------------------------------------------------------
bg1 = "lightsteelblue"  # 1번째 배경 : 날짜 있는 제일 윗 줄 프레임
btnC = "palevioletred"  # 날짜 버튼 색
fg1 = "black"  #날짜버튼 년월일 색
fg2 = "lavender"  #날짜버튼 00/0/0 날짜 색


titleC1 = "lemonchiffon"  # 2번째 프레임 : 그림판 제목
bg2 = "lightsteelblue"  # 3번째 프레임 : 그림판 배경
btnC2 = "slategray"  #펜지우개 버튼 색

titleC2 = "lemonchiffon"  # 4번째 프레임 : 메모장 제목
bg3 = "lightsteelblue"  # 5번째 프레임 : 메모장 배경

bg4 = "lightsteelblue"  # 6번째 프레임 : 오늘의 평가 배경

btnC3 = "cornflowerblue"  #파일저장하기 버튼
#-----------------------------------------------------------------------


# ===============================달력함수=================================================================
# 날짜 선택을 위한 달력 창 열기  #새로운 창을 생성하여 날짜를 선택할 수 있게 한다.
def open_calendar():
    global diary_window
    if isinstance(diary_window, Toplevel) and diary_window.winfo_exists():
        diary_window.destroy()
    
    root.withdraw()  # 기본 Tk윈도우 숨김(없으면, 그림일기장 뜰때, Tk라는 기본 윈도우가 같이 생성됨)
    calendar_window = Toplevel()  # 새로운 창 생성
    calendar_window.title("6조")  # 창 제목 설정
    calendar_window.geometry("400x310+500+200")  # 창 크기 설정

    # 달력 위젯 설정
    calendar = Calendar(calendar_window,
                    year=2024, month=12,
                    selectmode="day", date_pattern="yyyy-mm-dd",
                    font=("맑은 고딕", 18),
                    showweeknumbers=False,
                    background="lightblue",
                    borderwidth=2,
                    relief="solid")
    calendar.place(relx=0.5, rely=0.5, anchor=CENTER)  # 캘린더 위젯 위치 조정

    # 날짜 선택 버튼
    def on_date_select(event):
        selected_date = calendar.get_date()  # 달력에서 선택된 날짜를 가져옴
        # 날짜를 datetime 객체로 변환하여 요일 계산
        date_obj = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
        weekday = date_obj.strftime("%A")  # 요일을 영어로 계산 (예: 'Monday', 'Tuesday' 등)
        
        # 요일을 한글로 변환
        weekdays_korean = {
            "Monday": "월요일", "Tuesday": "화요일", "Wednesday": "수요일",
            "Thursday": "목요일", "Friday": "금요일", "Saturday": "토요일", "Sunday": "일요일"
        }
        korean_weekday = weekdays_korean.get(weekday, "알 수 없음")  # 한글 요일 가져오기

        # 선택된 날짜와 요일을 텍스트에 출력
        print(f"선택한 날짜: {selected_date} ({korean_weekday})")  # 콘솔에 출력

        # ta.insert(END, f"선택한 날짜: {selected_date} ({korean_weekday})\n")  # 텍스트 박스에 날짜 출력
        open_diary(selected_date, korean_weekday)  # 그림일기장 창 열기
        calendar_window.destroy()  # 달력 창 닫기

    # 달력의 일자버튼 클릭하면-> 그림 일기장 윈도우 창 열기
    calendar.bind("<<CalendarSelected>>", on_date_select)  # 날짜 선택 이벤트 바인딩

# ========================================================================================================



# ===============================그림일기장함수===========================================================
# 그림일기를 작성할 그림일기장 창 열기  #새로운 창을 생성하여 그림 일기를 그릴 수 있도록 한다.
def open_diary(selected_date, korean_weekday):
    global diary_window
    diary_window = Toplevel()  # 새로운 창 생성
    diary_window.title("그림일기장")  # 윈도우 제목 설정
    diary_window.geometry("600x710+500+8")  # 윈도우 크기와 위치 설정


    #-------------0번째 라인---------------------------------------------
    #설정 버튼
    mainMenu = Menu(diary_window)
    diary_window.config(menu=mainMenu)
    
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="그림일기 저장", command=lambda: saveDiary(selected_date))
    fileMenu.add_command(label="달력으로 돌아가기", command=open_calendar)

    #-------------1번째 라인---------------------------------------------
    #날짜와 날씨 버튼
    global date_frame
    global bg1, btnC, fg1, fg2
    date_frame = Frame(diary_window, bg = bg1)

    #년
    empty1_label = tk.Label(date_frame, bg = bg1, width=1, height=3)  #여백위한 레이블
    empty1_label.pack(side=tk.LEFT)

    year_label = tk.Label(date_frame, text=f"{selected_date.split('-')[0]}", width=5, height=2, borderwidth=1,
                          relief="raised", bg = btnC, fg = fg2, font = ("맑은 고딕",13,"bold"))
    nyeon_label = tk.Label(date_frame, text=f"년", width=4, height=2, borderwidth=1,
                            bg = btnC, fg = fg1, font = ("맑은 고딕",13,"bold"))
    year_label.pack(side=tk.LEFT, padx=1)
    nyeon_label.pack(side=tk.LEFT, padx=1)
    #월
    month_label1 = tk.Label(date_frame, text=f"{selected_date.split('-')[1]}", width=5, height=2, borderwidth=1,
                            relief="raised", bg = btnC, fg = fg2, font = ("맑은 고딕",13,"bold"))
    wol_label = tk.Label(date_frame, text=f"월", width=4, height=2, borderwidth=1,
                          bg = btnC, fg = fg1, font = ("맑은 고딕",13,"bold"))
    month_label1.pack(side=tk.LEFT, padx=1)
    wol_label.pack(side=tk.LEFT, padx=1)
    
    #일
    day_label = tk.Label(date_frame, text=f"{selected_date.split('-')[2]}", width=5, height=2, borderwidth=1,
                         relief="raised", bg = btnC, fg = fg2, font = ("맑은 고딕",13,"bold"))
    il_label = tk.Label(date_frame, text=f"일", width=4, height=2, borderwidth=1,
                         bg = btnC, fg = fg1, font = ("맑은 고딕",13,"bold"))
    day_label.pack(side=tk.LEFT, padx=1)
    il_label.pack(side=tk.LEFT, padx=1)
    #요일
    koreanDay_label = tk.Label(date_frame, text=f"{korean_weekday}", width=6, height=2, borderwidth=1,
                               relief="raised", bg = btnC, fg = fg2, font = ("맑은 고딕",13,"bold"))
    koreanDay_label.pack(side=tk.LEFT, padx=1)


    weather_button = tk.Button(date_frame, text="날씨", font=("맑은 고딕", 11), width=7, height=2)
    #@@@@@날씨 버튼 구현!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def weather_selection():
        def confirm_selection():
            selected_weather = weather_var.get()
            weather_window.destroy()  # 날씨 선택 창 닫기

            # 선택한 날씨 이미지 설정
            if selected_weather == "sun":
                selected_image = PhotoImage(file="sun2.png")
            elif selected_weather == "cloud":
                selected_image = PhotoImage(file="cloud2.png")
            elif selected_weather == "rain":
                selected_image = PhotoImage(file="rain2.png")
            else:
                selected_image = PhotoImage(file="snowy2.png")

            # 기존 날씨 이미지가 있으면 제거
            if hasattr(weather_button, 'image_label') and weather_button.image_label:
                weather_button.image_label.destroy()

            # 날씨 버튼 왼쪽에 이미지 추가
            image_label = Label(date_frame, image=selected_image, bg = "white")
            image_label.image = selected_image  # 이미지 참조 유지
            image_label.pack(side=tk.LEFT, padx=5)
            
            # 이미지 레이블 참조 저장
            weather_button.image_label = image_label


        # 날씨 선택 팝업 창 생성
        weather_window = Toplevel()
        weather_window.title("날씨")
        weather_window.geometry("300x600+800+15")

        # 라디오 버튼 값 저장 변수
        weather_var = StringVar(value="sun")

        # 버튼과 이미지를 포함하는 프레임 생성
        button_frame = Frame(weather_window)
        button_frame.pack(pady=0)

        # 맑음 라디오 버튼과 이미지
        sun_radio = Radiobutton(button_frame, text="맑음", variable=weather_var, value="sun")
        sun_radio.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        sun_image = PhotoImage(file="sun.png")
        sun_image_label = Label(button_frame, image=sun_image)
        sun_image_label.image = sun_image  # 이미지 참조 유지
        sun_image_label.grid(row=0, column=1, padx=5, pady=5)

        # 구름 라디오 버튼과 이미지
        cloud_radio = Radiobutton(button_frame, text="구름", variable=weather_var, value="cloud")
        cloud_radio.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        cloud_image = PhotoImage(file="cloud.PNG")
        cloud_image_label = Label(button_frame, image=cloud_image)
        cloud_image_label.image = cloud_image  # 이미지 참조 유지
        cloud_image_label.grid(row=1, column=1, padx=5, pady=5)

        # 비 라디오 버튼과 이미지
        rain_radio = Radiobutton(button_frame, text="비", variable=weather_var, value="rain")
        rain_radio.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        rain_image = PhotoImage(file="rain.PNG")
        rain_image_label = Label(button_frame, image=rain_image)
        rain_image_label.image = rain_image  # 이미지 참조 유지
        rain_image_label.grid(row=2, column=1, padx=5, pady=5)

        # 눈 라디오 버튼과 이미지
        snowy_radio = Radiobutton(button_frame, text="눈", variable=weather_var, value="snowy")
        snowy_radio.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        snowy_image = PhotoImage(file="snowy.PNG")
        snowy_image_label = Label(button_frame, image=snowy_image)
        snowy_image_label.image = snowy_image  # 이미지 참조 유지
        snowy_image_label.grid(row=3, column=1, padx=5, pady=5)


        # 확인 버튼
        confirm_button = Button(weather_window, text="확인", command=confirm_selection)
        confirm_button.pack(pady=10)

    # 날씨 버튼에 weather_selection 함수 연결
    weather_button.config(command=weather_selection)

    empty2_label = tk.Label(date_frame, bg = bg1, width=10, height=4)  #여백위한 레이블
    empty2_label.pack(side=tk.LEFT)
    weather_button.pack(side=tk.LEFT, padx=0)
    date_frame.pack(fill=tk.X)


    #-------------[그림판]-------------------------------------------------
    #-------------2번째 라인 : 도구메뉴------------------------------------
    
    #그림판 메뉴 프레임
    global titleC1, bg2, btnC2
    draw_frame = tk.Frame(diary_window, bg = bg2)
    title_label = tk.Label(draw_frame, text="그림판", font=("맑은 고딕", 13, "bold"), bg = titleC1, width = 700)
    title_label.pack(padx=3)
    
    # 펜 버튼
    pen_button = Button(draw_frame, text="펜", command=enablePen, bg = btnC2, fg = "white")
    pen_button.pack(side=tk.LEFT, padx=10, pady=10)

    # 펜 색상 선택 버튼
    color_button = Button(draw_frame, text="선 색상 선택", command=getColor)
    color_button.pack(side=tk.LEFT, padx=0, pady=10)

    # 펜 두께 설정 버튼
    width_button = Button(draw_frame, text="선 두께 설정", command=getWidth)
    width_button.pack(side=tk.LEFT, padx=10, pady=10)

    # 지우개 두께 설정 버튼
    eraser_width_button = Button(draw_frame, text="지우개 두께 설정", command=getEraserWidth)
    eraser_width_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # 지우개 버튼
    eraser_button = Button(draw_frame, text="지우개", command=enableEraser, bg = btnC2, fg = "white")
    eraser_button.pack(side=tk.RIGHT, padx=0, pady=0)

    draw_frame.pack(fill=tk.X, pady=0)
    
    #-------------3번째 라인 : 캔버스 -------------------------------------
    #그림판
    global canvas
    canvas_frame = Frame(diary_window, bg = bg2)
    canvas = Canvas(canvas_frame, bg="white", width=520, height=250)
    canvas.pack(padx=10, pady=0)
    empty3_label = tk.Label(canvas_frame, bg = bg2, height=1)  #여백위한 레이블
    empty3_label.pack()
    
    canvas_frame.pack(fill=tk.X,pady=0)
    

    
    # 마우스 클릭 시 실행되는 함수
# 클릭한 위치를 선의 시작 좌표로 설정
    def mouseClick(event):
        global x1, y1, x2, y2 # 전역 변수 선언
        x1 = event.x  # 마우스 클릭 시의 x 좌표
        y1 = event.y  # 마우스 클릭 시의 y 좌표

# 마우스를 놓을 때 호출되는 함수
# 드래그한 위치를 선의 끝 좌표로 설정하고 선을 그림
    def mouseDrop(event):
        global x1, y1, penWidth, penColor, eraserWidth, isEraserMode
        x2 = event.x  # 마우스를 놓는 시점의 x 좌표
        y2 = event.y  # 마우스를 놓는 시점의 y 좌표
        # 선을 그리기 전에, 이전에 그린 선을 저장한 후 새로운 선을 그려야 함
        if x1 and y1:  # 처음 클릭한 좌표가 있을 경우에만 선을 그림
            if isEraserMode:
                canvas.create_line(x1, y1, x2, y2, width=eraserWidth, fill="white")
                # 선 정보 저장 (지우개 모드일 경우에도 저장)
                line_objects.append((x1, y1, x2, y2, "white", eraserWidth))
            else:
                canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)
                # 선 정보 저장 (펜 모드일 경우 색상과 두께 저장)
                line_objects.append((x1, y1, x2, y2, penColor, penWidth))
        x1, y1 = x2, y2  # 현재 위치를 이전 위치로 갱신하여 계속 드래그를 시작할 수 있도록 함
        

    # 마우스 이벤트 바인딩
    canvas.bind("<Button-1>", mouseClick)  # 마우스 왼쪽 클릭
    canvas.bind("<B1-Motion>", mouseDrop)  # 마우스 드래그
    
    #-------------[메모장]-------------------------------------------------
    #-------------4번째 라인---------------------------------------------
    #메모장
    global ta
    global bg3, titleC2
    memo_frame = tk.Frame(diary_window, bg = bg3)
    memo_label = tk.Label(memo_frame, text="메모장", font=("맑은 고딕", 13, "bold"), bg = titleC2, width = 700)
    memo_label.pack(padx = 3)
    ta = Text(memo_frame, height=10, width=74)
    ta.pack(pady=10)
    
    memo_frame.pack(fill=tk.X, pady=0)

    #-------------5번째 라인---------------------------------------------
    #오늘의 평가 & 도장 선택 버튼
    global bg4
    evaluation_frame = tk.Frame(diary_window, bg = bg4)
    evaluation_label = tk.Label(evaluation_frame, text="오늘의 평가", font=("맑은 고딕", 13), width = 10 ,height=2)
    evaluation_label.pack(side=tk.LEFT, padx=5)
    stamp_button = tk.Button(evaluation_frame, text="도장 선택", width=10, height=2)
    #@@@@@도장선택 버튼 구현!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def open_stamp_selection():
        
        def confirm_selection():
            selected_stamp = stamp_var.get()
            stamp_window.destroy()  # 도장 선택 창 닫기

            # 선택한 도장 이미지 설정
            if selected_stamp == "good":
                selected_image = PhotoImage(file="good2.png")
            else:
                selected_image = PhotoImage(file="bad2.png")

            # 기존 평가 이미지가 있으면 제거
            if hasattr(evaluation_label, 'image_label') and evaluation_label.image_label:
                evaluation_label.image_label.destroy()

            # 날씨 버튼 왼쪽에 이미지 추가
            image_label = Label(evaluation_frame, image=selected_image)
            image_label.image = selected_image  # 이미지 참조 유지
            image_label.pack(side=tk.LEFT, padx=5)

            # 이미지 레이블 참조 저장
            evaluation_label.image_label = image_label

        # 도장 선택 팝업 창 생성
        stamp_window = Toplevel()
        stamp_window.title("도장 선택")
        stamp_window.geometry("300x700+900+50")

        # 라디오 버튼 값 저장 변수
        stamp_var = StringVar(value="good")

        # "참! 잘했어요" 라디오 버튼과 이미지
        good_radio = Radiobutton(stamp_window, text="참! 잘했어요", variable=stamp_var, value="good")
        good_radio.pack(anchor="w", pady=5)

        good_image = PhotoImage(file="good.png")
        good_image_label = Label(stamp_window, image=good_image)
        good_image_label.image = good_image  # 이미지가 가비지 컬렉션으로 사라지지 않도록 참조 유지
        good_image_label.pack(pady=5)

        # "분발하세요" 라디오 버튼과 이미지
        bad_radio = Radiobutton(stamp_window, text="분발하세요", variable=stamp_var, value="bad")
        bad_radio.pack(anchor="w", pady=5)

        bad_image = PhotoImage(file="bad.PNG")
        bad_image_label = Label(stamp_window, image=bad_image)
        bad_image_label.image = bad_image  # 이미지 참조 유지
        bad_image_label.pack(pady=7)

        # 확인 버튼
        confirm_button = Button(stamp_window, text="확인", command=confirm_selection)
        confirm_button.pack(pady=10)


    # 도장 선택 버튼
    stamp_button.config(command=open_stamp_selection)

    
    stamp_button.pack(side=tk.RIGHT, padx=10, pady = 10)
    evaluation_frame.pack(fill=tk.X, pady=0)

    # 구분선
    separator5 = Canvas(diary_window, height=1, bg="black", highlightthickness=0)
    separator5.pack(fill=X, pady=0)
    
    #-------------마지막 라인---------------------------------------------
    #저장 버튼
    global btnC3
    save_button = Button(diary_window, text="파일로 저장하기", command=lambda: saveDiary(selected_date),
                         width=20, height=2, bg = btnC3)
    save_button.pack(pady=10)
    


# ========================================================================================================



# ===============================그림일기장 보조함수========================================================
# 선 색상 선택 함수
def getColor():
    global penColor, previousPenColor
    color = askcolor()  # 색상 선택 다이얼로그 열기
    previousPenColor = penColor  # 현재 색상을 저장
    penColor = color[1]  # 선택된 색상을 penColor 변수에 저장


# 선 두께 결정 함수
def getWidth():
    global penWidth, previousPenWidth# 전역 변수 선언
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요", minvalue=1, maxvalue=10)
    # 선의 두께를 1~10 사이의 정수로 입력받음
    previousPenWidth = penWidth  # 현재 두께를 저장

def getEraserWidth():
    global eraserWidth
    eraserWidth = askinteger("지우개 두께", "지우개 두께(1~10)를 입력하세요", minvalue=1, maxvalue=10)

def enableEraser():
    global isEraserMode, previousPenColor, previousPenWidth
    if not isEraserMode:  # 지우개 모드가 아닐 때만 저장
        previousPenColor = penColor
        previousPenWidth = penWidth
    isEraserMode = True

def enablePen():
    global isEraserMode, penColor, penWidth
    isEraserMode = False
    penColor = previousPenColor  # 저장된 색상 복원
    penWidth = previousPenWidth  # 저장된 두께 복원

# 그림일기 저장 함수
def saveDiary(selected_date):
 
    # 캡처할 영역 정보 가져오기 (tkinter의 실제 좌표)
    x1 = date_frame.winfo_rootx()
    y1 = date_frame.winfo_rooty()
    x2 = x1 + 600
    y2 = y1 + 660


    # 프레임 영역 캡처
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))


    # 파일 저장 다이얼로그 열기
    file_path = asksaveasfilename(initialfile = f"{selected_date}.png",
                                  defaultextension=".png",
                                  filetypes=[("PNG Files", "*.png")])


    if file_path:
        screenshot.save(file_path)  # 캡처한 이미지 저장
        print("파일 저장 완료:", file_path)
        
# ========================================================================================================


# 실행 메인 코드
if __name__ == "__main__":

    root = Tk()  # 숨겨질 기본 Tk 윈도우

    #화면 해상도에 따라 변화하는 값 조정
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()  # DPI 모드 활성화
    screen_scale = user32.GetDpiForSystem() / 96
    

    open_calendar()
    
    root.mainloop()
