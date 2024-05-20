import pygame
import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정 (환경 변수에서 가져오기)
openai.api_key = os.getenv("")


def generate_response(prompt):
    tabi_prompt = (
        f"안녕 뿡빵띠! 나는 아라하시 타비야. {prompt}에 대해 대답해 줄게. "
        "내 대답은 항상 밝고 에너지가 넘쳐야 해. 그리고 나의 기발한 표현도 잊지 말고 사용해야 해. "
        "예를 들어, '우와 정말 대단해!' 같은 표현을 사용해봐. 자, 시작해볼까?"
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=tabi_prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Arahashi Tabi Chatbot")

# 폰트 설정
font = pygame.font.Font(None, 36)

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 입력 상자 설정
input_box = pygame.Rect(100, 500, 600, 50)
color_inactive = pygame.Color("lightskyblue3")
color_active = pygame.Color("dodgerblue2")
color = color_inactive

active = False
text = ""
response = ""

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 입력 상자 클릭 여부 확인
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # Enter 키를 누르면 응답 생성
                    response = generate_response(text)
                    text = ""
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill(WHITE)

    # 텍스트 렌더링
    txt_surface = font.render(text, True, BLACK)
    response_surface = font.render(response, True, BLACK)

    # 입력 상자 크기 조정
    width = max(600, txt_surface.get_width() + 10)
    input_box.w = width

    # 텍스트와 입력 상자 그리기
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    screen.blit(response_surface, (100, 100))
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
