import pygame
import sys
import os
import requests

# OpenAI API 키
OPENAI_API_KEY = ""

# Pygame 초기화
pygame.init()

# 창 설정
screen = pygame.display.set_mode((646, 394))
pygame.display.set_caption("Visual Novel Chat UI")

# 합성된 배경 이미지 로드
combined_image = pygame.image.load("Tabi.png")  # 이미지 파일 이름을 적절히 ss수정하세요.

# 폰트 설정
font_path = "c:\\Windows\\Fonts\\H2SA1M.TTF"  # 한글 폰트 파일 경로
font_character = pygame.font.Font(font_path, 40)  # 캐릭터 이름 폰트 설정
font_chat = pygame.font.Font(font_path, 18)  # 대화 내용 폰트 설정

user_text = ""
input_rect = pygame.Rect(100, 350, 440, 32)
color_active = pygame.Color("lightskyblue3")
color_passive = pygame.Color("gray15")
color = color_passive
active = False

# 전송 버튼
button_image = pygame.image.load("send_button.png")  # 전송 버튼 이미지 로드
button_image = pygame.transform.scale(button_image, (30, 30))  # 이미지 크기 조정
button_rect = button_image.get_rect(center=(570, 366))

# 대화 내용 저장
chat_history = []


# 캐릭터 이름 표시
def draw_character_name():
    sky_blue = (15, 206, 235)  # 스카이블루 색상 코드
    name_text = font_character.render("타비", True, sky_blue)  # 이름 텍스트 렌더
    name_rect = name_text.get_rect(
        left=int(screen.get_width() * 0.15), top=int(screen.get_height() * 0.53)
    )  # top 값을 조정하여 간격을 줄입니다.
    screen.blit(name_text, name_rect)  # 이름 그리기
    # 하얀색 선 그리기
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (100, name_rect.bottom + 5),
        (540, name_rect.bottom + 5),
        2,
    )


# 대화창
def draw_input_box():
    if active:
        color = color_active
    else:
        color = color_passive
    pygame.draw.rect(screen, color, input_rect, 2)
    text_surface = font_character.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))


# 대화 내용 출력
def draw_chat_history():
    start_y = 270  # 출력 시작 위치를 조정하여 입력 창 위에 표시
    # chat_history 리스트에서 표시할 대화의 개수만큼 추출합니다.
    recent_chats = chat_history[-4:]  # 최근 5개의 대화를 추출합니다.
    for i, message in enumerate(recent_chats):
        # 대화 내용을 출력할 사각형 영역을 생성합니다.
        chat_surface = pygame.Surface((436, 22))
        chat_surface.fill((15, 15, 45))  # 딥 블루 색상으로 채웁니다.
        screen.blit(
            chat_surface, (105, start_y)
        )  # 딥 블루 색상의 사각형을 화면에 표시합니다.

        text_surface = font_chat.render(message, True, (255, 255, 255))
        screen.blit(
            text_surface, (110, start_y + 2)
        )  # 대화 내용을 흰색으로 출력합니다.
        start_y += 24  # 새 메시지를 위로 추가 (위에서 아래로 출력)


# OpenAI API 요청 함수
def request_openai_api(input_text):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + OPENAI_API_KEY,
    }
    payload = {
        "model": "text-davinci-003",  # 선택한 모델에 따라 수정
        "prompt": input_text,
        "max_tokens": 50,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "Error: Unable to generate response."


# 게임 루프
while True:
    start_y = 270
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
            if button_rect.collidepoint(event.pos):  # 버튼 클릭 처리
                # 사용자 입력을 chat_history에 추가합니다.
                user_input = "You: " + user_text
                chat_history.append(user_input)
                # OpenAI API를 사용하여 응답을 생성하고 chat_history에 추가합니다.
                response = request_openai_api(user_text)
                chat_history.append(response)
                user_text = ""
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # 사용자 입력을 chat_history에 추가합니다.
                    user_input = "You: " + user_text
                    chat_history.append(user_input)
                    # OpenAI API를 사용하여 응답을 생성하고 chat_history에 추가합니다.
                    response = request_openai_api(user_text)
                    chat_history.append(response)
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 마우스 휠을 위로 스크롤하면
                if start_y < 270:
                    start_y += 20
            elif event.button == 5:  # 마우스 휠을 아래로 스크롤하면
                if start_y > 270 - len(chat_history) * 24:
                    start_y -= 20

    screen.blit(combined_image, (0, 0))  # 합성된 이미지를 화면에 표시
    draw_character_name()  # 캐릭터 이름 그리기
    draw_input_box()
    draw_chat_history()  # 대화 내용 출력
    screen.blit(button_image, button_rect)  # 버튼 그리기

    pygame.display.flip()
