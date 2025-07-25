import pygame
import sys

# Cores e texto
BG_COLOR = (34, 40, 49)
TEXT_COLOR = (228, 241, 254)
FEEDBACK_COLOR = (255, 107, 107)
TIP_BG = (44, 62, 80)
TIP_TEXT = (236, 240, 241)

# Questões e opções
questions = [
    "1. Achei difícil me acalmar",
    "2. Senti minha boca seca",
    "3. Não consegui vivenciar nenhum sentimento positivo",
    "4. Tive dificuldade em respirar (ex: respiração ofegante)",
    "5. Achei difícil ter iniciativa para fazer as coisas",
    "6. Reagi de forma exagerada às situações",
    "7. Senti tremores (ex: nas mãos)",
    "8. Senti que estava sempre nervoso",
    "9. Tive medo de parecer ridículo(a) em público",
    "10. Senti que não tinha nada a desejar",
    "11. Senti-me agitado",
    "12. Achei difícil relaxar",
    "13. Senti-me sem ânimo",
    "14. Fui intolerante com dificuldades",
    "15. Tive sensação de pânico",
    "16. Não consegui me entusiasmar com nada",
    "17. Senti que não tinha valor",
    "18. Estava emotivo(a) demais",
    "19. Coração acelerado mesmo em repouso",
    "20. Senti medo sem motivo",
    "21. A vida parecia sem sentido"
]

options = [
    "Aplicou-se em algum grau, ou por pouco de tempo",
    "Aplicou-se em um grau considerável, ou por boa parte do tempo",
    "Aplicou-se muito, ou na maioria do tempo",
    "Não se aplicou de maneira alguma"
]
score_map = [1, 2, 3, 0]
option_colors = {
    options[0]: (255, 223, 0),
    options[1]: (0, 255, 0),
    options[2]: (0, 128, 255),
    options[3]: (255, 0, 0)
}
click_counter = {"Amarelo": 0, "Verde": 0, "Azul": 0, "Vermelho": 0}

tips = [
    "1. Respiração profunda ajuda a acalmar.",
    "2. Relaxamento muscular é eficaz.",
    "3. Durma bem e regularmente.",
    "4. Converse com alguém de confiança.",
    "5. Caminhadas leves são saudáveis.",
    "6. Experimente mindfulness por 5 minutos.",
    "7. Escreva em um diário suas emoções."
]

def draw_wrapped_text(surface, text, x, y, font, color=TEXT_COLOR, max_width=500):
    words = text.split()
    line = ''
    line_height = font.get_linesize()
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] > max_width:
            surface.blit(font.render(line.strip(), True, color), (x, y))
            y += line_height
            line = word + ' '
        else:
            line = test_line
    if line:
        surface.blit(font.render(line.strip(), True, color), (x, y))

def load_image(path, size=None):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size) if size else img

def fade(screen, clock, fade_in=True, speed=10):
    fade_surf = pygame.Surface(screen.get_size()).convert()
    for alpha in (range(255, -1, -speed) if fade_in else range(0, 256, speed)):
        fade_surf.fill(BG_COLOR)
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))
        pygame.display.update()
        clock.tick(60)

def get_color_name(rgb):
    return {
        (255, 223, 0): "Amarelo",
        (0, 255, 0): "Verde",
        (0, 128, 255): "Azul",
        (255, 0, 0): "Vermelho"
    }.get(rgb, "Desconhecido")

def create_single_button(screen, font, text):
    w, h = 200, 50
    rect = pygame.Rect((screen.get_width()-w)//2, screen.get_height()-80, w, h)
    return rect, text

def welcome_screen(screen, clock, font):
    title_font = pygame.font.SysFont('Arial', 30, bold=True)
    subtitle_font = pygame.font.SysFont('Arial', 22)
    bruxo_img = load_image("bruxo.png", size=(180, 250))

    run = True
    while run:
        screen.fill(BG_COLOR)
        screen.blit(bruxo_img, ((screen.get_width() - bruxo_img.get_width()) // 2, 30))
        draw_wrapped_text(screen, "Bem-vindo ao Teste das Pedras Mágicas", 100, 280, title_font)
        intro = (
            "Você está prestes a iniciar uma jornada mágica de autoconhecimento. "
            "Cada pergunta revelará uma pedra mágica representando uma parte de você. "
            "Clique na pedra que melhor representa como você se sentiu."
        )
        draw_wrapped_text(screen, intro, 80, 350, subtitle_font, max_width=640)
        start_btn = pygame.Rect((screen.get_width() - 220) // 2, 500, 220, 45)
        pygame.draw.rect(screen, (3, 218, 197), start_btn, border_radius=12)
        draw_wrapped_text(screen, "Iniciar Jornada", start_btn.x + 35, start_btn.y + 10, subtitle_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    run = False

        pygame.display.flip()
        clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 22)
    welcome_screen(screen, clock, font)

    current_q = 0
    answers = []
    running = True
    phase = 1
    game_over = False
    feedback = ""
    btn_show_tips = None
    btn_exit = None

    pedra_imagens = {
        "Amarelo": load_image("pedra_amarela.png", (60, 60)),
        "Verde": load_image("pedra_verde.png", (60, 60)),
        "Azul": load_image("pedra_azul.png", (60, 60)),
        "Vermelho": load_image("pedra_vermelha.png", (60, 60))
    }

    stones = []
    x = screen.get_width() // 2 - 100
    spacing = 100
    for i, (opt, color) in enumerate(option_colors.items()):
        stones.append({"center": (x, 150 + i * spacing), "radius": 30, "color": color, "label": opt})

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if phase == 1 and not game_over:
                    for stone in stones:
                        dx = event.pos[0] - stone["center"][0]
                        dy = event.pos[1] - stone["center"][1]
                        if dx * dx + dy * dy <= stone["radius"] ** 2:
                            fade(screen, clock, fade_in=False)
                            idx = options.index(stone["label"])
                            answers.append(idx)
                            click_counter[get_color_name(stone["color"])] += 1
                            current_q += 1
                            if current_q >= len(questions):
                                game_over = True
                                avg = sum(score_map[a] for a in answers) / len(questions)
                                feedback = "Preocupante" if avg >= 2 else "Não preocupante"
                                btn_show_tips = create_single_button(screen, font, "Ver Dicas") if feedback == "Preocupante" else create_single_button(screen, font, "Sair")
                            fade(screen, clock, fade_in=True)
                elif phase == 1 and game_over:
                    if feedback == "Preocupante" and btn_show_tips[0].collidepoint(event.pos):
                        phase = 2
                        fade(screen, clock, fade_in=False)
                        fade(screen, clock, fade_in=True)
                    elif feedback != "Preocupante" and btn_exit[0].collidepoint(event.pos):
                        running = False
                elif phase == 2 and btn_exit and btn_exit[0].collidepoint(event.pos):
                    running = False

        screen.fill(BG_COLOR if phase == 1 else TIP_BG)

        if phase == 1 and not game_over:
            draw_wrapped_text(screen, questions[current_q], 20, 20, font)
            for stone in stones:
                color_name = get_color_name(stone["color"])
                img = pedra_imagens[color_name]
                rect = img.get_rect(center=stone["center"])
                screen.blit(img, rect)
                draw_wrapped_text(screen, stone["label"], stone["center"][0] + 50, stone["center"][1] - 25, font, max_width=350)
        elif game_over and phase == 1:
            screen.blit(font.render("Questionário concluído!", True, FEEDBACK_COLOR), (250, 200))
            screen.blit(font.render(f"Resultado: {feedback}", True, FEEDBACK_COLOR), (250, 240))
            y = 300
            for cor, count in click_counter.items():
                screen.blit(font.render(f"{cor}: {count} vez(es)", True, TEXT_COLOR), (250, y))
                y += 30
            rect, text = btn_show_tips if feedback == "Preocupante" else btn_exit
            pygame.draw.rect(screen, (3, 218, 197), rect, border_radius=8)
            pygame.draw.rect(screen, TEXT_COLOR, rect, 2, border_radius=8)
            draw_wrapped_text(screen, text, rect.x + 30, rect.y + 10, font)
        elif phase == 2:
            draw_wrapped_text(screen, "Dicas para melhorar:", 20, 20, font, color=TIP_TEXT)
            y = 80
            for tip in tips:
                draw_wrapped_text(screen, tip, 40, y, font, color=TIP_TEXT)
                y += font.get_linesize() + 10
            if not btn_exit:
                btn_exit = create_single_button(screen, font, "Sair")
            rect, text = btn_exit
            pygame.draw.rect(screen, (3, 218, 197), rect, border_radius=8)
            pygame.draw.rect(screen, TEXT_COLOR, rect, 2, border_radius=8)
            draw_wrapped_text(screen, text, rect.x + 60, rect.y + 10, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
