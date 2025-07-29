import pygame
import sys

# Inicialização do Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Cores do tema
BG_COLOR = (34, 40, 49)
TEXT_COLOR = (228, 241, 254)
FEEDBACK_COLOR = (255, 107, 107)
TIP_BG = (44, 62, 80)
TIP_TEXT = (236, 240, 241)

# Fonte padrão
FONT = pygame.font.SysFont('Arial', 24)


def load_image(path, size=None):
    """Carrega imagem e redimensiona se necessário."""
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    return img


def draw_wrapped_text(surface, text, x, y, font, color=TEXT_COLOR, wrap_width=700):
    """Renderiza texto com quebra de linha automática até wrap_width e respeita '\n'."""
    y_offset = 0
    for paragraph in text.split('\n'):
        # wrap cada parágrafo
        words = paragraph.split(' ')
        line = ''
        for word in words:
            test = f"{line} {word}".strip()
            if font.size(test)[0] <= wrap_width:
                line = test
            else:
                surface.blit(font.render(line, True, color), (x, y + y_offset))
                y_offset += font.get_linesize()
                line = word
        surface.blit(font.render(line, True, color), (x, y + y_offset))
        y_offset += font.get_linesize()
        y_offset += font.get_linesize() // 2



def welcome_screen(screen, clock, font):
    """Exibe tela de boas-vindas com imagem do bruxo."""
    title_font = pygame.font.SysFont('Arial', 36, bold=True)
    subtitle_font = pygame.font.SysFont('Arial', 22)
    bruxo_img = load_image('bruxo.png', size=(180, 250))
    intro_lines = [
        "Bem-vindo ao Teste das Pedras Mágicas!",
        "Clique na opção que melhor traduz",
        "seus sentimentos e descubra seu perfil."
    ]
    while True:
        screen.fill(BG_COLOR)
        img_x = (SCREEN_WIDTH - bruxo_img.get_width()) // 2
        screen.blit(bruxo_img, (img_x, 30))
        for i, line in enumerate(intro_lines):
            screen.blit(
                subtitle_font.render(line, True, TIP_TEXT),
                (50, 300 + i * subtitle_font.get_linesize())
            )
        prompt = "Pressione ENTER para iniciar"
        render = subtitle_font.render(prompt, True, TIP_TEXT)
        rect = render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        pygame.draw.rect(screen, TIP_BG, rect.inflate(20, 10), border_radius=5)
        screen.blit(render, rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        pygame.display.flip()
        clock.tick(30)


class Button:
    """Botão genérico para cliques."""
    def __init__(self, rect, text, callback, font, color=TIP_BG, text_color=TEXT_COLOR):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        txt = self.font.render(self.text, True, self.text_color)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()


class AssessmentPhase:
    """Fase de apresentação de perguntas e coleta de respostas."""
    def __init__(self, screen, title, questions, categories, recommendations):
        self.screen = screen
        self.title = title
        self.questions = questions
        self.categories = categories
        self.recommendations = recommendations
        self.index = 0
        self.score = 0
        self.options = ['0', '1', '2', '3', '4']
        self.buttons = []
        self._create_option_buttons()

    def _create_option_buttons(self):
        self.buttons.clear()
        w, h, gap = 80, 40, 100
        x0, y0 = 100, SCREEN_HEIGHT - 100
        for i, opt in enumerate(self.options):
            btn = Button(
                (x0 + i * gap, y0, w, h),
                opt,
                callback=lambda v=i: self._select(v),
                font=FONT
            )
            self.buttons.append(btn)

    def _select(self, val):
        self.score += val
        self.index += 1
        if self.index >= len(self.questions):
            self._finish()
        else:
            self._create_option_buttons()

    def _finish(self):
        category = next(
            (n for n, (low, high) in self.categories.items() if low <= self.score <= high),
            'NORMAL'
        )
        rec_text = self.recommendations.get(category, '')
        PhaseManager.instance.next_step(
            result_title=f"{self.title}: {category}",
            result_text=rec_text
        )

    def draw(self):
        self.screen.fill(BG_COLOR)
        draw_wrapped_text(self.screen, f"Avaliação de {self.title}", 50, 20, FONT)
        draw_wrapped_text(self.screen, self.questions[self.index], 50, 80, FONT)
        for btn in self.buttons:
            btn.draw(self.screen)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)


class ResultPhase:
    """Fase de exibição do resultado e recomendações."""
    def __init__(self, screen, title, text):
        self.screen = screen
        self.title = title
        self.text = text

    def draw(self):
        self.screen.fill(TIP_BG)
        draw_wrapped_text(self.screen, self.title, 50, 50, FONT, color=FEEDBACK_COLOR)
        draw_wrapped_text(self.screen, self.text, 50, 100, FONT)
        prompt = "Pressione ENTER para continuar..."
        self.screen.blit(FONT.render(prompt, True, TIP_TEXT), (50, SCREEN_HEIGHT - 50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            PhaseManager.instance.next_step()


class ThankYouPhase:
    """Fase final de agradecimento."""
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        self.screen.fill(BG_COLOR)
        lines = [
            "Obrigado por participar!",
            "Lembre-se sempre de buscar o apoio de um adulto,",
            "psicólogo, professor, amigos ou familiares.",
            "",
            "Pressione ENTER para sair."
        ]
        for i, line in enumerate(lines):
            color = TEXT_COLOR if line else TEXT_COLOR
            FONT_SMALL = pygame.font.SysFont('Arial', 22)
            self.screen.blit(FONT_SMALL.render(line, True, color),
                             (50, 200 + i * (FONT_SMALL.get_linesize()+5)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pygame.quit()
            sys.exit()


class PhaseManager:
    """Gerencia a sequência de fases: Depressão, Ansiedade e Estresse."""
    instance = None

    def __init__(self, screen):
        PhaseManager.instance = self
        self.screen = screen

        # Configuração Depressão
        depression_questions = [
            "Você se sentiu para baixo, deprimido ou sem esperança nas últimas duas semanas?",
            "Você teve pouco interesse ou prazer em fazer as coisas?",
            "Você teve dificuldade para dormir ou dormiu demais?",
            "Você se sentiu cansado ou com pouca energia?",
            "Você teve pouco apetite ou comeu em excesso?"
        ]
        depression_cats = {
            'NORMAL': (0, 4),
            'LEVE': (5, 9),
            'MODERADO': (10, 14),
            'SEVERO': (15, 19),
            'EXTREMAMENTE SEVERO': (20, 27)
        }
        depression_recs = {
            'NORMAL': (
                "- Nenhuma intervenção imediata necessária.\n"
                "- Continuar monitorando bem-estar emocional.\n"
                "- Prática criativa: artesanato, música, esporte leve."
            ),
            'LEVE': (
                "- Autoconhecimento: monitorar humor e sintomas.\n"
                "- Hábitos Saudáveis: exercícios, dieta e sono.\n"
                "- Gerenciamento do Estresse: mindfulness e respiração.\n"
                "- Suporte Social: amigos e familiares.\n"
                "- Prática criativa: artesanato, música, esporte leve."
            ),
            'MODERADO': (
                "- Tratamento Multidisciplinar: avaliação psiquiátrica e psicoterapia e/ou medicamentos.\n"
                "- Suporte Psicossocial: encorajamento e apoio emocional.\n"
                "- Hábitos Saudáveis: exercícios, dieta equilibrada e relaxamento.\n"
                "- Acompanhamento Regular: consultas para monitorar e ajustar tratamento.\n"
                "- Prática criativa: artesanato, música, esporte leve."
            ),
            'SEVERO': (
                "- Tratamento Psiquiátrico Urgente: avaliação imediata e possível hospitalização.\n"
                "- Terapia Intensiva (TCC): desenvolver habilidades de enfrentamento.\n"
                "- Medicação Antidepressiva: ISRS ou outros sob supervisão.\n"
                "- Suporte Psicossocial: apoio contínuo da rede de relacionamento.\n"
                "- Monitoramento Contínuo: consultas frequentes para ajustes.\n"
                "- Prática criativa: artesanato, música, esporte leve."
            ),
            'EXTREMAMENTE SEVERO': (
                "- Intervenção Psiquiátrica Urgente: avaliação imediata e internação se necessário.\n"
                "- Terapia Intensiva e Monitoramento 24/7: suporte contínuo.\n"
                "- Medicação Antidepressiva e Antipsicótica: supervisão médica.\n"
                "- Suporte Psicossocial Intensivo: apoio emocional intenso.\n"
                "- Intervenção de Crise: plano de segurança para ideação suicida.\n"
                "- Prática criativa: artesanato, música, esporte leve."
            )
        }

        # Configuração Ansiedade
        anxiety_questions = [
            "Você se sentiu nervoso, ansioso ou no limite?",
            "Você não conseguiu parar ou controlar suas preocupações?",
            "Você teve dificuldade para relaxar?",
            "Você se sentiu inquieto ou agitado?",
            "Você teve dificuldade de concentração?"
        ]
        anxiety_cats = depression_cats
        anxiety_recs = {
            'NORMAL': (
                "- Manter hábitos saudáveis: exercícios e sono.\n"
                "- Mindfulness e respiração.\n"
                "- Hobbies para relaxar.\n"
                "- Gestão de tempo.\n"
                "- Consultas periódicas."
            ),
            'LEVE': (
                "- Autocuidado: exercícios, dieta e sono.\n"
                "- Mindfulness ou meditação.\n"
                "- Psicoterapia breve.\n"
                "- Planejamento de tempo.\n"
                "- Autoavaliação e consultas."
            ),
            'MODERADO': (
                "- Psicoterapia (TCC): sessões regulares.\n"
                "- Relaxamento: yoga e meditação.\n"
                "- Atividade Física: alívio de sintomas.\n"
                "- Suporte Social: grupos e amigos.\n"
                "- Monitoramento: ajustes periódicos."
            ),
            'SEVERO': (
                "- Intervenção Especializada: psicólogo e psiquiatra.\n"
                "- Medicação: ansiolíticos ou antidepressivos.\n"
                "- Técnicas Avançadas: biofeedback e meditação guiada.\n"
                "- Suporte Social: grupos de apoio.\n"
                "- Monitoramento Contínuo: acompanhamento aprofundado."
            ),
            'EXTREMAMENTE SEVERO': (
                "- Intervenção Psiquiátrica Imediata: consulta urgente e medicação.\n"
                "- Psicoterapia Intensiva: TCC ou semelhante.\n"
                "- Técnicas Avançadas: biofeedback e meditação guiada.\n"
                "- Rede de Apoio: suporte emocional contínuo.\n"
                "- Monitoramento e Ajuste: revisões constantes."
            )
        }

        # Configuração Estresse
        stress_questions = [
            "Você se sentiu estressado ou irritado?",
            "Você teve dificuldade para relaxar ou acalmar a mente?",
            "Você se sentiu sobrecarregado pelas responsabilidades?",
            "Você teve problemas para dormir por causa do estresse?",
            "Você sentiu sintomas físicos relacionados ao estresse, como dores de cabeça ou tensão muscular?"
        ]
        stress_cats = depression_cats
        stress_recs = {
            'NORMAL': (
                "- Manutenção de Hábitos Saudáveis: exercícios, alimentação balanceada e sono adequado.\n"
                "- Relaxamento: mindfulness, respiração ou meditação.\n"
                "- Lazer: hobbies e atividades recreativas.\n"
                "- Monitoramento de Estresse: gerenciamento de tempo e planejamento.\n"
                "- Apoio Social: rede de suporte sólida.\n"
                "- Consultas Periódicas: check-ups regulares."
            ),
            'LEVE': (
                "- Autocuidado: rotina de exercícios, alimentação e sono.\n"
                "- Relaxamento: mindfulness e meditação.\n"
                "- Psicoterapia breve: aconselhamento.\n"
                "- Planejamento de tempo: gerenciamento de estresse.\n"
                "- Monitoramento: autoavaliação regular."
            ),
            'MODERADO': (
                "- Psicoterapia (TCC): sessões regulares.\n"
                "- Relaxamento: yoga e meditação.\n"
                "- Atividade Física: alívio de sintomas.\n"
                "- Suporte Social: grupos e amigos.\n"
                "- Gerenciamento de Estresse: técnicas estruturadas.\n"
                "- Monitoramento: avaliações periódicas."
            ),
            'SEVERO': (
                "- Intervenção Psiquiátrica Imediata: consulta urgente e possível medicação.\n"
                "- Psicoterapia intensiva: TCC intensivo.\n"
                "- Técnicas Avançadas: biofeedback e programas estruturados.\n"
                "- Suporte Social e Familiar: envolvimento da rede de apoio.\n"
                "- Monitoramento Contínuo: ajustes frequentes."
            ),
            'EXTREMAMENTE SEVERO': (
                "- Intervenção Psiquiátrica Urgente: avaliação imediata e medicação.\n"
                "- Psicoterapia Intensiva: TCC ou ACT intensivos.\n"
                "- Técnicas Avançadas: meditação guiada e biofeedback.\n"
                "- Rede de Apoio: suporte emocional contínuo.\n"
                "- Acompanhamento Médico Regular: revisão de plano de tratamento."
            )
        }

        # Lista de avaliações
        self.assessments = [
            {'title': 'Depressão', 'questions': depression_questions, 'categories': depression_cats, 'recommendations': depression_recs},
            {'title': 'Ansiedade', 'questions': anxiety_questions, 'categories': anxiety_cats, 'recommendations': anxiety_recs},
            {'title': 'Estresse',   'questions': stress_questions,   'categories': stress_cats,   'recommendations': stress_recs}
        ]
        self.current = 0
        self.phase = None

    def start(self):
        self._start_assessment()

    def _start_assessment(self):
        data = self.assessments[self.current]
        self.phase = AssessmentPhase(
            self.screen,
            data['title'],
            data['questions'],
            data['categories'],
            data['recommendations']
        )

    def next_step(self, result_title=None, result_text=None):
        if result_title:
            self.phase = ResultPhase(self.screen, result_title, result_text)
        else:
            self.current += 1
            if self.current < len(self.assessments):
                self._start_assessment()
            else:
                self.phase = ThankYouPhase(self.screen)

    def draw(self):
        self.phase.draw()

    def handle_event(self, event):
        self.phase.handle_event(event)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo de Apoio Psicológico")
    clock = pygame.time.Clock()
    welcome_screen(screen, clock, FONT)
    manager = PhaseManager(screen)
    manager.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            manager.handle_event(event)
        manager.draw()
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
