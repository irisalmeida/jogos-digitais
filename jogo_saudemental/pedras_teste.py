import pygame
import sys

# Cores e texto
BG_COLOR = (34, 40, 49)
TEXT_COLOR = (228, 241, 254)
FEEDBACK_COLOR = (255, 107, 107)
TIP_BG = (44, 62, 80)
TIP_TEXT = (236, 240, 241)

# Opções de resposta
options = [
    "Aplicou-se em algum grau, ou por pouco de tempo",
    "Aplicou-se em um grau considerável, ou por uma boa parte do tempo",
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

questions = [
    "1. Achei difícil me acalmar",
    "2. Senti minha boca seca",
    "3. Não consegui vivenciar nenhum sentimento positivo",
    "4. Tive dificuldade em respirar em alguns momentos (ex. respiração ofegante)",
    "5. Achei difícil ter iniciativa para fazer as coisas",
    "6. Tive a tendência de reagir de forma exagerada às situações",
    "7. Senti tremores (ex. nas mãos)",
    "8. Senti que estava sempre nervoso",
    "9. Preocupei-me com situações em que eu pudesse entrar em pânico e parecesse ridículo(a)",
    "10. Senti que não tinha nada a desejar",
    "11. Senti-me agitado",
    "12. Achei difícil relaxar",
    "13. Senti-me depressivo(a) e sem ânimo",
    "14. Fui intolerante com as coisas que me impediam de continuar",
    "15. Senti que ia entrar em pânico",
    "16. Não consegui me entusiasmar com nada",
    "17. Senti que não tinha valor como pessoa",
    "18. Senti que estava um pouco emotivo/sensível demais",
    "19. Sabia que meu coração estava alterado mesmo sem esforço físico",
    "20. Senti medo sem motivo",
    "21. Senti que a vida não tinha sentido"
]

tips = [
    "1. Pratique exercícios de respiração profunda diariamente.",
    "2. Tente técnicas de relaxamento muscular progressivo.",
    "3. Estabeleça uma rotina de sono regular.",
    "4. Converse com amigos ou familiares sobre seus sentimentos.",
    "5. Considere atividades físicas leves, como caminhadas.",
    "6. Experimente meditação ou mindfulness por 5 minutos.",
    "7. Escreva num diário suas emoções ao final do dia."
]

def init_pygame(width=800, height=600, title="Pedras Mágicas - Jornada Interior"):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    return screen, pygame.time.Clock()

def draw_wrapped_text(surface, text, x, y, font, color=TEXT_COLOR, max_width=300):
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
    if size:
        img = pygame.transform.scale(img, size)
    return img

def get_color_name(rgb):
    return {
        (255, 223, 0): "Amarelo",
        (0, 255, 0): "Verde",
        (0, 128, 255): "Azul",
        (255, 0, 0): "Vermelho"
    }.get(rgb, "Desconhecido")

def create_single_button(screen, font, text):
    w, h = 200, 50
    rect = pygame.Rect((screen.get_width()-w)//2, screen.get_height()-100, w, h)
    return rect, text

def fade(screen, clock, fade_in=True, speed=10):
    fade_surf = pygame.Surface(screen.get_size()).convert()
    for alpha in (range(255, -1, -speed) if fade_in else range(0, 256, speed)):
        fade_surf.fill(BG_COLOR)
        fade_surf.set_alpha(alpha)
        screen.blit(fade_surf, (0, 0))
        pygame.display.update()
        clock.tick(60)

def welcome_screen(screen, clock, font):
    bruxo_img = load_image("bruxo.png", size=(200, 300))
    title_font = pygame.font.SysFont('Arial', 32, bold=True)
    run = True
    while run:
        screen.fill(BG_COLOR)
        screen.blit(bruxo_img, ((screen.get_width() - bruxo_img.get_width()) // 2, 40))
        draw_wrapped_text(screen, "Descubra as Pedras do Seu Interior", 120, 360, title_font)
        intro = (
            "Você está prestes a entrar em uma jornada mágica de autoconhecimento.\n"
            "Cada pergunta revelará uma pedra mágica, representando uma parte de você.\n"
            "Clique na pedra que melhor representa como você se sentiu nos últimos dias."
        )
        draw_wrapped_text(screen, intro, 100, 410, font, max_width=600)
        start_btn = pygame.Rect((screen.get_width() - 220) // 2, 530, 220, 40)
        pygame.draw.rect(screen, (3, 218, 197), start_btn, border_radius=8)
        draw_wrapped_text(screen, "Iniciar Jornada", start_btn.x + 50, start_btn.y + 10, font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    run = False
        pygame.display.flip()
        clock.tick(60)

def main():
    screen, clock = init_pygame()
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

    colors = list(option_colors.values())
    labels = list(option_colors.keys())
    stones = []
    x = screen.get_width() // 2 - 100
    start_y = 150
    spacing = 100
    radius = 30
    for i, color in enumerate(colors):
        y = start_y + i * spacing
        stones.append({"center": (x, y), "radius": radius, "color": color, "label": labels[i]})

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
                                total = sum(score_map[a] for a in answers)
                                avg = total / len(questions)
                                feedback = "Preocupante" if avg >= 2 else "Não preocupante"
                                if feedback == "Preocupante":
                                    btn_show_tips = create_single_button(screen, font, "Ver Dicas")
                                else:
                                    btn_exit = create_single_button(screen, font, "Sair")
                            fade(screen, clock, fade_in=True)
                            break
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
                nome_cor = get_color_name(stone["color"])
                img = pedra_imagens[nome_cor]
                rect = img.get_rect(center=stone["center"])
                screen.blit(img, rect)
                draw_wrapped_text(screen, stone["label"], stone["center"][0] + 50, stone["center"][1] - 25, font, max_width=350)
        elif game_over and phase == 1:
            surf1 = font.render("Questionário concluído!", True, FEEDBACK_COLOR)
            surf2 = font.render(f"Resultado: {feedback}", True, FEEDBACK_COLOR)
            screen.blit(surf1, ((screen.get_width()-surf1.get_width())//2, 200))
            screen.blit(surf2, ((screen.get_width()-surf2.get_width())//2, 240))
            y_counter = 300
            for color, count in click_counter.items():
                txt = font.render(f"{color}: {count} vez(es)", True, TEXT_COLOR)
                screen.blit(txt, ((screen.get_width()-txt.get_width())//2, y_counter))
                y_counter += 30
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
