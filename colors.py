
class Colors:
    dark_grey = (26, 31, 40)
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)
    black=(0,0,0)
    # Themes
    themes = {
        "dark": {
            "background": (44, 44, 127),
            "score_bg": (59, 85, 162),
            "text": white,
        },
        "light": {
            "background": black,
            "score_bg": dark_grey,
            "text": white,
            "score_next_text": white,
        },
    }

    active_background = themes["dark"]["background"]
    active_score_bg = themes["dark"]["score_bg"]
    active_text = themes["dark"]["text"]
    active_score_next_text = themes["dark"]["text"]

    @classmethod
    def set_theme(cls, theme):
        cls.active_background = cls.themes[theme]["background"]
        cls.active_score_bg = cls.themes[theme]["score_bg"]
        cls.active_text = cls.themes[theme]["text"]
        cls.active_score_next_text = cls.themes[theme].get("score_next_text", cls.themes[theme]["text"])

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]