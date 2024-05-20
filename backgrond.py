from PIL import Image, ImageDraw, ImageFont
import pygame
import sys

# 이미지 파일 경로
combined_image_path = 'C:\\Users\\user\\Desktop\\Tabi\\Tabi.png'

# 이미지 로드
combined = Image.open(combined_image_path).convert('RGBA')

# 텍스트 추가를 위한 드로우 객체 생성
draw = ImageDraw.Draw(combined)

# 폰트 설정
font_path = "c:\\Windows\\Fonts\\H2SA1M.TTF"  # 한글 폰트 파일 경로
font_size = 30
character_name_font_size = 40  # 캐릭터 닉네임 폰트 사이즈
font = ImageFont.truetype(font_path, font_size)
character_name_font = ImageFont.truetype(font_path, character_name_font_size)

# 텍스트 위치 및 내용
character_name = "타비"
input_text = "my input"
output_text = "-> output text"

# 텍스트 위치 설정
character_name_position = (25, combined.height - 230)
input_text_position = (50, combined.height - 150)
output_text_position = (50, combined.height - 100)

# 텍스트 색상
text_color = "blue"

# 텍스트 추가
draw.text(character_name_position, character_name, font=character_name_font, fill=text_color)
draw.text(input_text_position, input_text, font=font, fill=text_color)
draw.text(output_text_position, output_text, font=font, fill=text_color)

# 테두리 박스 설정
box_x0, box_y0 = 20, combined.height - 180
box_x1, box_y1 = combined.width - 20, combined.height - 20

# 테두리 박스 그리기
draw.rectangle([box_x0, box_y0, box_x1, box_y1], outline="blue", width=5)

# PIL 이미지를 Pygame 이미지로 변환
mode = combined.mode
size = combined.size
data = combined.tobytes()

pygame_image = pygame.image.fromstring(data, size, mode)

# Pygame 초기화 및 화면 설정
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Image with UI")

# Pygame 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면에 이미지 그리기
    screen.blit(pygame_image, (0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()
