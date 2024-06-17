import json
import os
import tkinter as tk
from tkinter import colorchooser as clch

import customtkinter as ctk
import pyocr
import pyocr.builders
from PIL import Image, ImageColor, ImageEnhance

# インストールしたTesseract-OCRのpath)
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR"
TESSDATA_PATH = r"C:\Program Files\Tesseract-OCR\tessdata"


IMAGE_DIR = os.path.join(os.path.dirname(__file__), "icon")
FORMULA_DIR = os.path.join(os.path.dirname(__file__), "formula")
OPTION_DIR = os.path.join(os.path.dirname(__file__), "option.json")


WINDOW_WIDTH = 300
WINDOW_HEIGHT = 402

GEOME = f"{WINDOW_WIDTH + 3}x{WINDOW_HEIGHT}"

FRAME_TITLE = 20
FRAME_CALC_HEIGHT = 100
FRAME_BUTTON_HEIGHT = 275

THEME_COLOR = "#181818"
TITLE_COLOR = "#212121"
BORDER_COLOR = "#dddddd"

NUM_COLOR = "#212121"
NUM_HOVER_COLOR = "#313131"

COM_COLOR = "#345678"
COM_HOVER_COLOR = "#456789"

BUTTONTEXT_COLOR = "#dddddd"

TRANSPARENT_COLOR = "#444444"

SYM = ["+", "-", "*", "/"]


class Calculator(ctk.CTk):
    def __init__(self, master=None):
        super().__init__(
            master,
        )
        self.geometry(GEOME)
        self.resizable(width=False, height=False)
        self.wm_overrideredirect(True)
        self.configure(fg_color=TRANSPARENT_COLOR)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", TRANSPARENT_COLOR)

        self.start_x = None
        self.start_y = None

        self.calc_num = ""
        self.calc_mem = ""

        self.option_flag = 0
        self.rgb_code = []

        self.dj = {
            "color": {
                "theme": THEME_COLOR,
                "title": TITLE_COLOR,
                "border": BORDER_COLOR,
                "button_text": BUTTONTEXT_COLOR,
                "number": {"fg": NUM_COLOR, "hover": NUM_HOVER_COLOR},
                "command": {"fg": COM_COLOR, "hover": COM_HOVER_COLOR},
            }
        }

        self.load_option()
        self.set_ctkform()
        self.set_main_window()
        self.set_sub_window()
        self.window_drag()

    def load_option(self):
        if not os.path.isfile(OPTION_DIR):
            with open(OPTION_DIR, "w") as f:
                json.dump(self.dj, f, indent=2)
        else:
            with open(OPTION_DIR) as f:
                self.dj = json.load(f)

    def set_ctkform(self):
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    def set_main_window(self):
        self.main_frame = ctk.CTkFrame(
            self,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            corner_radius=6,
            fg_color=self.dj["color"]["title"],
            border_color=self.dj["color"]["border"],
            border_width=1,
        )
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(expand=True, fill=ctk.BOTH)

        self.set_title_bar()
        self.set_display_frame()
        self.set_option()
        self.set_ans_formula()
        self.set_button()

    def set_title_bar(self):
        img_cl = ctk.CTkImage(
            dark_image=Image.open(os.path.join(IMAGE_DIR, r"xmark.png")), size=(10, 10)
        )
        img_op = ctk.CTkImage(
            dark_image=Image.open(os.path.join(IMAGE_DIR, r"option.png")), size=(10, 10)
        )

        self.title_bar = ctk.CTkFrame(
            self.main_frame,
            width=WINDOW_WIDTH,
            height=FRAME_TITLE,
            fg_color="transparent",
            corner_radius=6,
        )
        self.title_bar.pack(padx=(0, 2.9), pady=(1, 0), anchor=ctk.E)

        self.close_button = ctk.CTkButton(
            self.title_bar,
            width=20,
            height=FRAME_TITLE + 1,
            text="",
            image=img_cl,
            corner_radius=2,
            fg_color=self.dj["color"]["title"],
            hover_color="#dd0000",
            command=self.quit,
            # background_corner_colors=["#dd0000", "#dd0000", "#dd0000", "#dd0000"],
        )
        self.close_button.pack(side=ctk.RIGHT)

        self.option_button = ctk.CTkButton(
            self.title_bar,
            width=25,
            height=FRAME_TITLE + 1,
            text="",
            image=img_op,
            corner_radius=2,
            fg_color=self.dj["color"]["title"],
            hover_color="#323232",
            command=self.option_raise,
        )
        self.option_button.pack(side=ctk.RIGHT, pady=(0, 0), padx=(0, 0), ipadx=1)

        self.dif_button = ctk.CTkSwitch(
            self.title_bar,
            width=30,
            height=FRAME_TITLE,
            switch_height=14,
            switch_width=30,
            corner_radius=100,
            text="",
            button_color="#999999",
            button_hover_color="#999999",
            progress_color=self.dj["color"]["command"]["fg"],
            command=self.switch_event,
        )
        self.dif_button.pack(side=ctk.RIGHT, pady=(2, 0))

        # self.mini_button = ctk.CTkButton(
        #     self.title_bar,
        #     width=30,
        #     height=20,
        #     text="",
        #     image=img,
        #     corner_radius=0,
        #     fg_color="#000000",
        #     hover_color="#010101",
        #     command=self.withdraw,
        # )
        # self.mini_button.pack(side=ctk.RIGHT)
        # self.mini_button.configure(anchor=ctk.CENTER)

    # title_bar
    def option_raise(self):
        if self.option_flag == 0:
            self.frame_option.place(x=1, y=(FRAME_TITLE + 3))
            self.option_flag = 1
        else:
            self.frame_option.place_forget()
            self.option_flag = 0

    # title_bar
    def switch_event(self):
        self.switch_value = self.dif_button.get()
        if self.switch_value == 1:
            self.sub_app.deiconify()
        else:
            self.sub_app.withdraw()

    # main_window frameの配置
    def set_display_frame(self):
        self.frame_calc = ctk.CTkFrame(
            self.main_frame,
            width=WINDOW_WIDTH,
            height=FRAME_CALC_HEIGHT,
            fg_color=self.dj["color"]["theme"],
        )
        self.frame_calc.pack()

        self.frame_but = ctk.CTkFrame(
            self.main_frame,
            width=WINDOW_WIDTH,
            height=FRAME_BUTTON_HEIGHT,
            fg_color=self.dj["color"]["theme"],
            corner_radius=10,
        )
        self.frame_but.pack()

    # main_window  計算式表示、解答表示の配置
    def set_ans_formula(self):
        self.calc_var = ctk.StringVar()
        self.ans_var = ctk.StringVar()

        self.calc_label = ctk.CTkLabel(
            self.frame_calc,
            height=30,
            width=WINDOW_WIDTH - 1,
            font=(
                "Arial",
                15,
            ),
            fg_color=self.dj["color"]["theme"],
            text_color="#cccccc",
            textvariable=self.calc_var,
            wraplength=WINDOW_WIDTH,
        )
        self.calc_label.pack()
        self.calc_label.configure(anchor="e")

        self.ans_label = ctk.CTkLabel(
            self.frame_calc,
            height=70,
            width=WINDOW_WIDTH,
            font=(
                "Arial",
                24,
            ),
            fg_color=self.dj["color"]["theme"],
            text_color="#dddddd",
            textvariable=self.ans_var,
        )
        self.ans_label.pack()
        self.ans_label.configure(anchor="e")

    # main_window  ボタンの配置
    def set_button(self):
        BUT = [
            {
                "⇐": {
                    "fg": self.dj["color"]["command"]["fg"],
                    "hover": self.dj["color"]["command"]["hover"],
                },
                "": {
                    "fg": self.dj["color"]["command"]["fg"],
                    "hover": self.dj["color"]["command"]["hover"],
                },
                "C": {
                    "fg": self.dj["color"]["command"]["fg"],
                    "hover": self.dj["color"]["command"]["hover"],
                },
                "/": {
                    "fg": self.dj["color"]["command"]["fg"],
                    "hover": self.dj["color"]["command"]["hover"],
                },
            },
            {
                "7": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "8": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "9": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "*": {
                    "fg": self.dj["color"]["command"]["fg"],
                    "hover": self.dj["color"]["command"]["hover"],
                },
            },
            {
                "4": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "5": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "6": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "-": {
                    "fg": self.dj["color"]["command"]["fg"],
                    "hover": self.dj["color"]["command"]["hover"],
                },
            },
            {
                "1": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "2": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "3": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "+": {
                    "fg": self.dj["color"]["command"]["fg"],
                    "hover": self.dj["color"]["command"]["hover"],
                },
            },
            {
                "00": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "0": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                ".": {
                    "fg": self.dj["color"]["number"]["fg"],
                    "hover": self.dj["color"]["number"]["hover"],
                },
                "=": {
                    "fg": self.dj["color"]["command"]["fg"],
                    "hover": self.dj["color"]["command"]["hover"],
                },
            },
        ]
        for button_row, row in enumerate(BUT, 1):
            for button_column, num in enumerate(row.items()):
                self.calc_button = ctk.CTkButton(
                    self.frame_but,
                    width=int(WINDOW_WIDTH / 4) - 1,
                    height=55,
                    corner_radius=5,
                    fg_color=num[1]["fg"],
                    hover_color=num[1]["hover"],
                    text=num[0],
                    text_color=self.dj["color"]["button_text"],
                )

                self.calc_button.bind(
                    "<Button-1>",
                    lambda event, txt=num[0]: self.on_button_click(txt),
                )
                self.calc_button.grid(row=button_row, column=button_column)

    # main_window  ボタンクリック
    def on_button_click(self, txt):
        calc_num_clear = ""
        # print("Button :", txt)

        if txt == "=":
            if self.calc_num == "":
                self.calc_num = ""
            elif self.calc_num[-1] in SYM:
                self.calc_num = self.calc_num[:-1]
                self.ans_var.set(eval(self.calc_num))
                self.calc_mem = str(eval(self.calc_num))
            else:
                self.ans_var.set(eval(self.calc_num))
                self.calc_mem = str(eval(self.calc_num))

        elif txt == "C":
            self.calc_num = ""
            self.calc_mem = ""
            self.ans_var.set(self.calc_num)

        elif txt == "⇐":
            self.calc_num = self.calc_num[:-1]
            self.calc_mem = ""
            self.ans_var.set(calc_num_clear)

        elif txt == ".":
            if self.calc_num == "":
                self.calc_num += "0."
            elif self.calc_num[-1] == ".":
                self.calc_num = self.calc_num[:-1] + txt

            elif self.calc_num[-1] in SYM:
                self.calc_num = self.calc_num[:-1] + txt
            else:
                self.calc_num = self.calc_num + txt
                try:
                    eval(self.calc_num)
                except:
                    self.calc_num = self.calc_num[:-1]

        # 上記のボタン以外のとき
        elif txt in SYM:
            if self.calc_num == "":
                self.calc_num = ""
            elif self.calc_num[-1] == ".":
                self.calc_num = self.calc_num[:-1] + txt
            elif self.calc_num[-1] in SYM:
                if self.calc_mem != "":
                    self.calc_num = self.calc_mem + txt
                    self.calc_mem = ""
                else:
                    self.calc_num = self.calc_num[:-1] + txt
            else:
                if self.calc_mem != "":
                    self.calc_num = self.calc_mem + txt
                    self.calc_mem = ""
                else:
                    self.calc_num += txt

        else:
            self.calc_num += txt

        # print(self.calc_num)
        self.calc_var.set(self.calc_num)

    def start_drag(self, event):
        self.start_x = event.x_root - self.winfo_x()
        self.start_y = event.y_root - self.winfo_y()

    def stop_drag(self, event):
        self.start_x = None
        self.start_y = None

    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            x = event.x_root - self.start_x
            y = event.y_root - self.start_y
            self.geometry(f"{GEOME}+{x}+{y}")
            self.sub_app.geometry(f"{GEOME}+{x + 385}+{y}")

    def bind_drag_events(self, widget):
        widget.bind("<ButtonPress-1>", self.start_drag)
        widget.bind("<ButtonRelease-1>", self.stop_drag)
        widget.bind("<B1-Motion>", self.on_drag)

    def window_drag(self):
        widgets = [
            self.frame_but,
            self.frame_calc,
            self.title_bar,
            self.main_frame,
        ]

        for widget in widgets:
            self.bind_drag_events(widget)

    def set_sub_window(self):
        self.sub_app = ctk.CTkToplevel(fg_color=TRANSPARENT_COLOR)
        self.sub_app.geometry(GEOME)
        self.sub_app.attributes("-topmost", True)
        self.sub_app.attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.sub_app.wm_overrideredirect(True)
        self.sub_app.withdraw()

        self.sub_frame = ctk.CTkFrame(
            self.sub_app,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            corner_radius=6,
            fg_color=self.dj["color"]["title"],
            border_color=self.dj["color"]["border"],
            border_width=1,
        )
        self.sub_frame.propagate(False)
        self.sub_frame.pack(expand=True, fill=ctk.BOTH)

        self.sub_title_bar = ctk.CTkFrame(
            self.sub_frame,
            width=WINDOW_WIDTH - 6,
            height=FRAME_TITLE,
            corner_radius=10,
        )
        self.sub_title_bar.pack(padx=(0, 0), pady=(1, 0), anchor=ctk.CENTER)

        img_re = ctk.CTkImage(
            dark_image=Image.open(os.path.join(IMAGE_DIR, r"reload.png")), size=(10, 10)
        )
        img_load = ctk.CTkImage(
            dark_image=Image.open(os.path.join(IMAGE_DIR, r"load.png")), size=(10, 10)
        )
        self.clear_canvas_button = ctk.CTkButton(
            self.sub_title_bar,
            text="",
            width=15,
            height=FRAME_TITLE + 1,
            fg_color=self.dj["color"]["command"]["fg"],
            image=img_re,
            corner_radius=0,
            command=self.canvas_clear,
        )
        self.clear_canvas_button.pack(side=ctk.RIGHT, ipadx=1)

        self.save_canvas_button = ctk.CTkButton(
            self.sub_title_bar,
            text="読み込み",
            width=15,
            height=FRAME_TITLE + 1,
            fg_color=self.dj["color"]["command"]["fg"],
            image=img_load,
            corner_radius=0,
            command=self.load_canvas,
        )
        self.save_canvas_button.pack(side=ctk.RIGHT, ipadx=1)

        self.canvas = tk.Canvas(
            self.sub_frame,
            bg=self.dj["color"]["theme"],
            highlightbackground=self.dj["color"]["border"],
            highlightthickness=1,
        )
        self.canvas.pack(expand=True, fill=ctk.BOTH, padx=(0, 1))

        self.canvas.bind("<ButtonPress-1>", self.canvas_on_key_left)
        self.canvas.bind("<B1-Motion>", self.canvas_dragging)

    def load_canvas(self):

        ps_path = os.path.join(FORMULA_DIR, r"img.ps")
        png_path = os.path.join(FORMULA_DIR, r"img.png")
        if os.path.isfile(png_path):
            os.remove(png_path)
            os.remove(ps_path)
        self.canvas.postscript(
            file=ps_path,
            colormode="color",
            fontmap="-*-Helvetica-Bold-O-Normal--*-140-*",
        )

        self.convert_to_png(ps_path, png_path)
        self.recognize_fomula(png_path)

    def convert_to_png(self, ps_path, png_path):
        img = Image.open(ps_path)
        img.save(png_path)

    def recognize_fomula(self, png_path):
        os.environ["PATH"] += os.pathsep + TESSERACT_PATH
        os.environ["TESSDATA_PREFIX"] = TESSDATA_PATH

        tools = pyocr.get_available_tools()
        tool = tools[0]
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        img = Image.open(png_path)
        img_g = img.convert("L")
        img_g.point(lambda x: 0 if x < 230 else x)
        enhancer = ImageEnhance.Contrast(img_g)
        img_con = enhancer.enhance(2.0)
        txt_pyocr = tool.image_to_string(img_con, lang="eng", builder=builder)
        txt_pyocr = txt_pyocr.replace(" ", "")
        self.calc_num = self.calc_num + txt_pyocr
        self.calc_var.set(self.calc_num)

    # sub_window
    def canvas_clear(self):
        self.canvas.delete("all")

    # sub_window
    def canvas_on_key_left(self, event):
        self.curr_id = self.canvas.create_line(
            event.x, event.y, event.x, event.y, fill="#999999", width=2
        )

    # sub_window
    def canvas_dragging(self, event):
        points = self.canvas.coords(self.curr_id)
        points.extend([event.x, event.y])
        self.canvas.coords(self.curr_id, points)

    def set_option(self):
        self.frame_option = ctk.CTkFrame(
            self.main_frame,
            width=WINDOW_WIDTH + 1,
            height=WINDOW_HEIGHT - FRAME_TITLE - 6,
            fg_color=self.dj["color"]["theme"],
            bg_color="transparent",
            corner_radius=4,
        )
        self.frame_option.grid_propagate(False)
        self.frame_option.place(x=1, y=(FRAME_TITLE + 3))
        self.frame_option.place_forget()

        self.button_reset = ctk.CTkButton(
            self.frame_option,
            text="reset",
            width=20,
            command=self.reset_option,
        )
        self.button_reset.grid(row=0, column=3, sticky=tk.E)

        # number_color
        self.label_color_chose_num = ctk.CTkLabel(
            self.frame_option, text="Nnmber Button", width=200
        )
        self.label_color_chose_num.grid(row=1, column=0, sticky=tk.E)
        self.button_color_chose_num = ctk.CTkButton(
            self.frame_option,
            text="select",
            width=20,
            command=self.color_change_num_button,
        )
        self.button_color_chose_num.grid(row=1, column=1, sticky=tk.E)

        # command_color
        self.label_color_chose_com = ctk.CTkLabel(
            self.frame_option, text="Command Button", width=200
        )
        self.label_color_chose_com.grid(row=2, column=0, sticky=tk.E)
        self.button_color_chose_com = ctk.CTkButton(
            self.frame_option,
            text="select",
            width=20,
            command=self.color_change_com_button,
        )
        self.button_color_chose_com.grid(row=2, column=1, sticky=tk.E)

        # buttontext_color
        self.label_color_chose_buttontext = ctk.CTkLabel(
            self.frame_option, text="Button Text", width=200
        )
        self.label_color_chose_buttontext.grid(row=3, column=0, sticky=tk.E)
        self.button_color_chose_com = ctk.CTkButton(
            self.frame_option,
            text="select",
            width=20,
            command=self.color_change_buttontext,
        )
        self.button_color_chose_com.grid(row=3, column=1, sticky=tk.E)

        # theme_color
        self.label_color_chose_theme = ctk.CTkLabel(
            self.frame_option, text="Theme", width=200
        )
        self.label_color_chose_theme.grid(row=4, column=0, sticky=tk.E)
        self.button_color_chose_theme = ctk.CTkButton(
            self.frame_option,
            text="select",
            width=20,
            command=self.color_change_theme,
        )
        self.button_color_chose_theme.grid(row=4, column=1, sticky=tk.E)

        # border_color
        self.label_color_chose_theme = ctk.CTkLabel(
            self.frame_option, text="border", width=200
        )
        self.label_color_chose_theme.grid(row=5, column=0, sticky=tk.E)
        self.button_color_chose_theme = ctk.CTkButton(
            self.frame_option,
            text="select",
            width=20,
            command=self.color_change_border,
        )
        self.button_color_chose_theme.grid(row=5, column=1, sticky=tk.E)

    def reset_option(self):
        self.dj["color"]["number"]["fg"] = NUM_COLOR
        self.dj["color"]["number"]["hover"] = NUM_HOVER_COLOR
        self.dj["color"]["command"]["fg"] = COM_COLOR
        self.dj["color"]["command"]["hover"] = COM_HOVER_COLOR
        self.dj["color"]["button_text"] = BUTTONTEXT_COLOR

        with open(OPTION_DIR, "w") as f:
            json.dump(self.dj, f, indent=2)
        self.set_button()

        if self.dj["color"]["theme"] != THEME_COLOR:
            self.dj["color"]["theme"] = THEME_COLOR
            with open(OPTION_DIR, "w") as f:
                json.dump(self.dj, f, indent=2)
            self.main_frame.destroy()
            self.option_flag = 0
            self.set_main_window()
            self.option_raise()
            self.sub_frame.destroy()
            self.set_sub_window()
            self.window_drag()

        if self.dj["color"]["border"] != BORDER_COLOR:
            self.dj["color"]["border"] = BORDER_COLOR
            with open(OPTION_DIR, "w") as f:
                json.dump(self.dj, f, indent=2)
            self.main_frame.destroy()
            self.option_flag = 0
            self.set_main_window()
            self.option_raise()
            self.sub_frame.destroy()
            self.set_sub_window()
            self.window_drag()

    def lighten_color(self, color):
        rgb_code = []
        defalut_color = color[1]

        rgb_before = ImageColor.getcolor(str(defalut_color), "RGB")

        for rgb in rgb_before:
            if rgb - 1 == -1:
                rgb = rgb
                rgb_code.append(rgb)

            else:
                rgb = rgb - 9
                rgb_code.append(rgb)

        lighten_color = "#{:02x}{:02x}{:02x}".format(*tuple(rgb_code))

        return defalut_color, lighten_color

    def color_change_num_button(self):
        select_color = clch.askcolor()
        if select_color[1]:
            num_color, num_hover_color = self.lighten_color(select_color)
            self.dj["color"]["number"]["fg"] = num_color
            self.dj["color"]["number"]["hover"] = num_hover_color

            with open(OPTION_DIR, "w") as f:
                json.dump(self.dj, f, indent=2)
            self.set_button()

    def color_change_com_button(self):
        select_color = clch.askcolor()
        self.rgb_code = []
        if select_color[1]:
            com_color, com_hover_color = self.lighten_color(select_color)
            self.dj["color"]["command"]["fg"] = com_color
            self.dj["color"]["command"]["hover"] = com_hover_color

            with open(OPTION_DIR, "w") as f:
                json.dump(self.dj, f, indent=2)
            self.set_button()
            self.dif_button.destroy()
            self.dif_button = ctk.CTkSwitch(
                self.title_bar,
                width=30,
                height=FRAME_TITLE,
                switch_height=14,
                switch_width=30,
                corner_radius=100,
                text="",
                button_color="#999999",
                button_hover_color="#999999",
                progress_color=self.dj["color"]["command"]["fg"],
                command=self.switch_event,
            )
            self.dif_button.pack(side=ctk.RIGHT, pady=(2, 0))
            self.sub_frame.destroy()
            self.set_sub_window()

    def color_change_buttontext(self):
        select_color = clch.askcolor()
        self.rgb_code = []
        if select_color[1]:
            text_color = select_color[1]

            self.dj["color"]["button_text"] = text_color

            with open(OPTION_DIR, "w") as f:
                json.dump(self.dj, f, indent=2)
            self.set_button()

    def color_change_theme(self):
        select_color = clch.askcolor()
        if select_color[1]:
            self.dj["color"]["theme"] = select_color[1]

            with open(OPTION_DIR, "w") as f:
                json.dump(self.dj, f, indent=2)

            self.main_frame.destroy()
            self.option_flag = 0
            self.set_main_window()
            self.option_raise()
            self.sub_frame.destroy()
            self.set_sub_window()
            self.window_drag()

    def color_change_border(self):
        select_color = clch.askcolor()
        if select_color[1]:
            self.dj["color"]["border"] = select_color[1]

            with open(OPTION_DIR, "w") as f:
                json.dump(self.dj, f, indent=2)

            self.main_frame.destroy()
            self.option_flag = 0
            self.set_main_window()
            self.option_raise()
            self.sub_frame.destroy()
            self.set_sub_window()
            self.window_drag()


def main():
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()
