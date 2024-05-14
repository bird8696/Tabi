import pygame
import sys

# Pygame 초기화
pygame.init()

# 창 설정
screen = pygame.display.set_mode((646, 394))
pygame.display.set_caption("Visual Novel Chat UI")

# 합성된 배경 이미지 로드
combined_image = pygame.image.load("Tabi.png")  # 이미지 파일 이름을 적절히 수정하세요.

# 입력 텍스트 설정
base_font = pygame.font.Font(None, 32)  # 기본 시스템 폰트 사용

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
    name_font = pygame.font.Font("malgun.ttf", 36)  # 윈도우 기본 한글 폰트 사용
    sky_blue = (15, 206, 235)  # 스카이블루 색상 코드
    name_text = name_font.render("타비", True, sky_blue)  # 이름 텍스트 렌더
    name_rect = name_text.get_rect(
        left=int(screen.get_width() * 0.15), top=int(screen.get_height() * 0.55)
    )
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
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))


# 대화 내용 출력
def draw_chat_history():
    start_y = 300  # 출력 시작 위치를 조정하여 입력 창 위에 표시
    for message in chat_history[-5:]:  # 최근 5개의 메시지만 보여줌
        text_surface = base_font.render(message, True, (255, 255, 255))
        screen.blit(text_surface, (105, start_y))
        start_y -= 32  # 새 메시지를 위로 추가 (위에서 아래로 출력)


# 게임 루프
while True:
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
                chat_history.append("You: " + user_text)  # 사용자 입력 저장
                chat_history.append("뿡빵띠")  # 임시 답장
                user_text = ""
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    chat_history.append("You: " + user_text)
                    chat_history.append("뿡빵띠")
                    user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    screen.blit(combined_image, (0, 0))  # 합성된 이미지를 화면에 표시
    draw_character_name()  # 캐릭터 이름 그리기
    draw_input_box()
    draw_chat_history()  # 대화 내용 출력
    screen.blit(button_image, button_rect)  # 버튼 그리기

    pygame.display.flip()
