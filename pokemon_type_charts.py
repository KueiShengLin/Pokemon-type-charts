# -*-coding:utf-8-*-
import logging
from kivy.config import Config
Config.set('graphics', 'width', '1300')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'minimum_width', '1200')
Config.set('graphics', 'minimum_height', '600')
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

TYPE = ["一般", "格鬥", "飛行", "毒", "地面", "岩石", "蟲", "幽靈",
        "鋼", "火", "水", "草", "電", "超能力", "冰", "龍", "惡", "妖精"]

EFFECTIVE = {}
TYPE_COLOR = {}


class TypeGrid(GridLayout):
    global TYPE, EFFECTIVE, TYPE_COLOR, TypeLogger

    def __init__(self, **kwargs):
        super().__init__()
        for name, value in kwargs.items():
            # magic! set self.'name' = value
            # contain describe_box_widgets, now_eff
            setattr(self, name, value)

        self.read_effectiveness()
        self.add_items()
        self.widget_items = {}

        for widget in self.walk(restrict=True):
            self.widget_items[widget.id] = widget

    def add_items(self):
        """
        Add button and label into grid
        :return:
        """
        TypeLogger.info("add widgets into the grid...")

        # first row
        clear_btn = Button(text="Clear", on_press=self.callback, background_color=[1, 1, 1, 1], color=[0, 0, 0, 1], id="clear")
        self.add_widget(clear_btn)
        for tid, defend_pokemon in enumerate(TYPE):
            btn = Button(text=defend_pokemon, on_press=self.callback, background_color=TYPE_COLOR[defend_pokemon], id="btn_1_" + str(tid))
            self.add_widget(btn)

        # Other rows
        for tid, attack_pokemon in enumerate(TYPE):
            btn = Button(text=attack_pokemon, on_press=self.callback, background_color=TYPE_COLOR[attack_pokemon], id="btn_0_" + str(tid))
            self.add_widget(btn)
            for defend_pokemon in range(len(TYPE)):
                output_text = "x" + str(int(EFFECTIVE[attack_pokemon][defend_pokemon]))
                if EFFECTIVE[attack_pokemon][defend_pokemon] == 0.5:
                    output_text = "x" + str(EFFECTIVE[attack_pokemon][defend_pokemon])

                label = BackGroundLabel(text=output_text, id="label_"+str(tid)+'_'+str(defend_pokemon))
                self.add_widget(label)

    def callback(self, instance):
        """
        Button event
        :param instance:
        :return:
        """
        TypeLogger.debug("callback:"+instance.id)

        if instance.id == "clear":
            self._clear_button()

        else:
            locate = instance.id.split('_')
            self._label_antiwhite(axis=int(locate[1]), num=int(locate[2]))
            self._describe_layout(axis=int(locate[1]), pokemon_type=TYPE[int(locate[2])])

    def read_effectiveness(self):
        """
        read each type effectiveness by rows
        :return:
        """
        TypeLogger.info("Read the effectiveness file...")
        data_list = [EFFECTIVE, TYPE_COLOR]
        now_data = 0
        f = open("effectiveness", 'r', encoding='utf8')
        while True:
            line = f.readline()
            line = line.replace("\n", '')

            if line == "=":
                now_data += 1
                continue
            elif not line:
                break

            each_type = line.split(',')
            input_list = list(map(float, each_type[1:]))

            # if data is rbga, translate it to float
            if now_data == 1:
                input_list = [i/255 for i in map(float, each_type[1:])]
                input_list[-1] = input_list[-1] * 255
                # TypeLogger.debug("Color: ", each_type[0] + " " + str(input_list))

            data_list[now_data][each_type[0]] = input_list

    def _label_antiwhite(self, axis=0, num=0):
        """
        Anti-white a pick row or column
        axis (int): row(0) or col(1) need to be anti-white
        num (int): which row/column need to be anti-white
        :return: anti-white row/col
        """
        anti_white = False
        if axis == 0:
            # It is very colorful if you use 't' to pick the TYPE_COLOR
            # check if row is anti-white
            # for i in range(len(TYPE)):
            #     label_id = "label_" + str(num) + '_' + str(i)
            #     bg_color = self.widget_items[label_id].background_color
            #     if bg_color != [1, 1, 1, 1]:
            #         self.widget_items[label_id].background_color = [1, 1, 1, 1]
            #         anti_white =

            # if not, anti_white it
            if anti_white is False:
                for i, t in enumerate(TYPE):
                    label_id = "label_" + str(num) + '_' + str(i)
                    self.widget_items[label_id].background_color = TYPE_COLOR[TYPE[num]]

        else:
            # It is very colorful if you use 't' to pick the TYPE_COLOR
            # check if row is anti-white
            # for i in range(len(TYPE)):
            #     label_id = "label_" + str(i) + '_' + str(num)
            #     bg_color = self.widget_items[label_id].background_color
            #     if bg_color != [1, 1, 1, 1]:
            #         self.widget_items[label_id].background_color = [1, 1, 1, 1]
            #         anti_white = True

            if anti_white is False:
                for i, t in enumerate(TYPE):
                    label_id = "label_" + str(i) + '_' + str(num)
                    self.widget_items[label_id].background_color = TYPE_COLOR[TYPE[num]]
                    # self.widget_items[label_id].color = [1, 1, 1]

    def _describe_layout(self, axis=0, pokemon_type="一般"):
        """
        Show the effective of attck or defend at the right labels
        :param axis(int): 0 = attack, 1 = defend
        :param pokemon_type(str): type of attcker(defender)
        """
        TypeLogger.debug("describe box layout: " + str(axis) + " " + pokemon_type)

        self.describe_box_widgets["label_deputation"].color = TYPE_COLOR[pokemon_type]

        # attack
        if axis == 0:
            # Show the type of attacker
            self.describe_box_widgets["label_deputation"].text = pokemon_type + " 打人"

            # effective of attack
            for i, eff in enumerate(EFFECTIVE[pokemon_type]):
                self.now_eff[i] = eff
                self.describe_box_widgets["label_" + TYPE[i]].text = TYPE[i] + ": " + str(eff)
                if eff < 1:
                    print(eff)
                    self.describe_box_widgets["label_" + TYPE[i]].color = [0, 0.6, 0, 1]
                elif eff > 1:
                    self.describe_box_widgets["label_" + TYPE[i]].color = [1, 0, 0, 1]
                else:
                    self.describe_box_widgets["label_" + TYPE[i]].color = [0, 0, 0, 1]
        # defend
        # Notice that, EFFECTIVE is stored by attacker so we need to transfer it to defender (row2col)
        else:
            type_id = -1
            for i, t in enumerate(TYPE):
                if t == pokemon_type:
                    type_id = i
                    break

            new_text = str.split(self.describe_box_widgets["label_deputation"].text, " ")
            # Check is multiple effective or attacker
            if new_text[-1] == "打人":
                new_text = []
                for i in range(len(TYPE)):
                    self.now_eff[i] = 1

            # Show the type of defender
            self.describe_box_widgets["label_deputation"].text = " ".join(new_text[:-1]) + " " + pokemon_type + " 被打"
            #  Show the eff
            for i, t in enumerate(TYPE):
                self.now_eff[i] = self.now_eff[i] * EFFECTIVE[t][type_id]
                print(t, EFFECTIVE[t][type_id])
                self.describe_box_widgets["label_" + TYPE[i]].text = TYPE[i] + ": " + str(self.now_eff[i])

                if self.now_eff[i] < 1:
                    self.describe_box_widgets["label_" + TYPE[i]].color = [0, 0.6, 0, 1]
                elif self.now_eff[i] > 1:
                    self.describe_box_widgets["label_" + TYPE[i]].color = [1, 0, 0, 1]
                else:
                    self.describe_box_widgets["label_" + TYPE[i]].color = [0, 0, 0, 1]

        TypeLogger.debug("label_deputation color: " + str(list(self.describe_box_widgets["label_deputation"].color)))
        TypeLogger.debug("label_deputation bg color: " + str(list(self.describe_box_widgets["label_deputation"].background_color)))

    def _clear_button(self):
        """
        When you click the "Clear" Button
        :return:
        """
        # Clear GridLayout
        for row in range(len(TYPE)):
            for col in range(len(TYPE)):
                label_id = "label_" + str(row) + '_' + str(col)
                self.widget_items[label_id].background_color = [1, 1, 1, 1]

        # Clear DescribeBox
        self.describe_box_widgets["label_deputation"].text = "打人"
        self.now_eff = []
        for i, t in enumerate(TYPE):
            self.now_eff.append(1)
            self.describe_box_widgets["label_" + t].text = t + ": 1.0"
            self.describe_box_widgets["label_" + t].color = [0, 0, 0, 1]


class DescribeBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global TYPE, TypeLogger
        TypeLogger.info("init the describe box...")

        self.describe_labels = {}
        self.now_eff = [1 for _ in range(len(TYPE))]
        # add label to layout
        # 這個"問號"真的讓我很問號，為什麼第一個label顏色會特別淺??!!!
        label = BackGroundLabel(text="問號", id="idnt", size_hint=(.1, 0))
        self.add_widget(label)
        label = BackGroundLabel(text="打架", id="label_deputation")
        self.add_widget(label)

        for i, type_name in enumerate(TYPE):
            label = BackGroundLabel(text=type_name+": ", id="label_" + type_name)
            self.add_widget(label)

        # mark widget id
        for widget in self.walk(restrict=True):
            self.describe_labels[widget.id] = widget


class PokemonApp(App):
    # Window.size = (1100, 600)
    # Config.set('graphics', 'resizable', False)

    def build(self):
        self.title = "Pokemon Effective v0.1"
        app_layout = BoxLayout(orientation="horizontal")

        describe_box = DescribeBox(size_hint=(.1, 1))
        type_grid = TypeGrid(describe_box_widgets=describe_box.describe_labels, now_eff=describe_box.now_eff)

        app_layout.add_widget(describe_box)
        app_layout.add_widget(type_grid)
        return app_layout


class BackGroundLabel(Label):
    """
    This is the class for labels which need to anti-white
    the setting is in the .kv
    """
    pass


if __name__ == '__main__':
    fmt = "%(asctime)s %(levelname)s: %(message)s"
    fmt = logging.Formatter(fmt=fmt)

    TypeLogger = logging.getLogger("type")
    TypeLogger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    TypeLogger.addHandler(handler)

    PokemonApp().run()
#
