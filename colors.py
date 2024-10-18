class Colors: 
        dark_grey = (26, 31, 40)
        green = (47, 230, 23)
        red = (232, 18, 18)
        orange = (226, 116, 17)
        gray = (200, 200, 200)
        yellow = (237, 234, 4)
        magenta = (166, 0, 247)
        cyan = (21, 204, 209)
        dark_green = (20, 95, 20)
        blue = (13, 64, 225)
        dark_blue = (44, 44, 127)
        light_blue = (59, 85, 162)
        white = (225, 225, 225)

        @classmethod
        def get_cell_colors(cls):
                return [cls.dark_grey, cls.green, cls.magenta, cls.gray, cls.orange, cls.yellow, cls.blue, cls.cyan, cls.dark_green, cls.red]
        