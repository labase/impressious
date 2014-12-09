# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Impressious
# Copyright 2013-2014 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Impressious é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser  útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
#  a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

"""
############################################################
Impressious - Principal
############################################################

Módulo que define o editor de apresentações no espaço 2D

"""
LOREM = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy" \
        " nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat."
DIM = (180, 180)
ICON = "wysiwyg-classic-icons.jpg"
GUI = None


class Slide:
    """Um slide com texto que pode ser selecionado e a geometria editada

    :param navegador: Referência ao módulo navegador do Brython
    :param canvas: àrea onde o slide deve ser desenhado
    :param pai: Referência ao objeto pai que possui esse slide
    """

    def __init__(self, navegador, canvas, pai):
        self.gui = navegador
        self.svg = navegador.svg
        self.html = navegador.html
        self.svgcanvas = canvas
        self.pai = pai
        self.rect = self.area = self.group = self.position = self.dimension = None

    def slide(self, text=LOREM, position=None, dimension=None):
        """Cria um novo slide com o texto, posição e dimensão dadas

        :param text: O texto a ser colocado no slide
        :param position: Posição do slide (x, y) - automática se None
        :param dimension: Dimensão  do slide (w, h) - automática se None
        :return: Referência para o objeto slide
        """
        x, y = self.position = position or self.pai.new_position()
        w, h = self.dimension = dimension or DIM
        self.group = self.svg.g(transform='translate (%d, %d)' % self.position)
        self.rect = self.svg.rect(x=0, y=0, width=w, height=h, color="grey", opacity=0.2)
        self.area = self.svg.foreignObject(x=0, y=0, width=w, height=h)
        self.area.html = text
        self.group <= self.area
        self.group <= self.rect
        self.svgcanvas <= self.group
        Impressious.SLIDES.append(self)
        self.group.onclick = self._select
        return self

    def widen(self, delta):
        """Enlarguesse o slide

        :param delta: aumento na largura
        """
        w, h = self.dimension
        w, h = self.dimension = (w+delta, h)
        self.rect.setAttribute('width', '%d' % w)
        self.area.setAttribute('width', '%d' % w)

    def heighten(self, delta):
        """Enaltece o slide

        :param delta: aumento na largura
        """
        w, h = self.dimension
        w, h = self.dimension = (w, h+delta)
        self.rect.setAttribute('height', '%d' % h)
        self.area.setAttribute('height', '%d' % h)

    def move(self, x, y):
        """Movimenta o slide para uma nova posição

        :param x: nova posição x
        :param y: nova posição y
        """
        (ox, oy), (w, h) = self.position, self.dimension
        self.position = (x-w//2, y-h//2)
        self.group.setAttribute('transform', 'translate (%d %d)' % self.position)

    def _select(self, event):
        """Cria um cursor ao ser selecionado

        :param event: Dados do mouse quando clicado
        :return: Nada
        """
        (x, y), (w, h) = self.position, self.dimension
        center = x+w//2, y+h//2
        self.pai.build_cursor(self, center)


class Impressious:
    """Classe que define o editor de apresentações no espaço 2D

    :param navegador: Referência ao módulo navegador do Brython
    """
    SLIDES = []

    def __init__(self, navegador):
        """Constroi os objetos iniciais. """
        global GUI
        self.gui = GUI = navegador
        self.svg = navegador.svg
        self.html = navegador.html
        self.ajax = navegador.ajax
        self.svgcanvas = self.cursor = self.icon = self.menu = self.back = None
        self.load = self.save = lambda ev: None
        self.dim = (800, 600)

    def build_base(self, width=800, height=600):
        """Constrói as partes do Jogo.

        :return: Self, referência a este objeto
        """
        python_div = self.gui.document['pydiv']
        self.dim = width, height
        self.svgcanvas = self.svg.svg(width=width, height=height)
        python_div <= self.svgcanvas
        self.back = self.svg.g()
        self.svgcanvas <= self.back
        menu = dict(main=dict(load={"img%s" % gab: self.load for gab in range(50)}, save=self.save))
        #self.menu = Menu()
        self.icon = Sprite(ICON, 37, 43, 12, 10, 2).sprites(main=[4, 1], save=[0, 0], load=[0, 2])
        self.icon["main"].render(python_div, 2, 0, self.ad_template, "img50")
        self.icon["save"].render(python_div, 2, 40)
        self.icon["load"].render(python_div, 2, 80)
        return self

    def _process_arguments(self, gui):

        def set_prop(value):
            self.props = self.json.loads(value)['result']
            self.pmenu = Menu(self.gui, 'ad_objeto', menu=self.props, prefix=MENUITEM, command='', extra=[MARKER])
            print('set_prop', self.props)

        def set_scene(value):
            self.scene = self.json.loads(value)['result']
            self.smenu = Menu(self.gui, 'ad_cenario', menu=self.scenes, prefix=MENUITEM, command='')
            print('set_scene', self.scene)

        args = self.win.location.search
        if '=' in args:
            self.args = {k: v for k, v in [c.split('=') for c in args[1:].split('&')]}
            props = self.properties = self.args.setdefault('props', 'jeppeto')
            self.folder = self.args.setdefault('folder', '')
            scenes = self.args.setdefault('scenes', 'EICA')
            self.gui.send(STUDIO % (props, 1), record=set_prop, method="GET")
            self.gui.send(STUDIO % (scenes, 2), record=set_scene, method="GET")
            print(self.args, props, STUDIO % (props, 1))
            if 'game' in self.args:
                gui.start_a_game(self.args['game'])
            else:
                gui.show_front_menu()
        else:
            gui.show_front_menu()

    def new_position(self):
        """Aloca uma posição automática para um novo slide

        :return: a posição (x, y)
        """
        dx, dy = DIM
        ox, oy = 10, 10
        dx, dy = dx+ox, dy+oy
        sx, sy = self.dim
        xlim = sx // dx
        slide = len(Impressious.SLIDES)
        print(xlim, (slide % xlim) * dx + ox, (slide // xlim) * dy + oy)
        return (slide % xlim) * dx + ox, (slide // xlim) * dy + oy

    def slide(self, text=LOREM, position=None, dimension=None):
        """Cria um novo slide com o texto, posição e dimensão dadas

        :param text: O texto a ser colocado no slide
        :param position: Posição do slide (x, y) - automática se None
        :param dimension: Dimensão  do slide (w, h) - automática se None
        :return: Referência para o objeto slide
        """
        return Slide(self.gui, self.svgcanvas, self).slide(text, position, dimension)

    def read_wiki(self, url):
        """Lê uma página da wiki com uma chamada REST

        :param url: Url REST da wiki a ser lida
        :return: COnteúdo da página wiki
        """
        FAKEC = '<h1></h1>' + '<li>Lê uma página da wiki com uma chamada REST</li>' * 10
        FAKE = dict(result=dict(wikidata=dict(conteudo=FAKEC)))
        try:
            import urllib.request
            import json
            _fp = urllib.request.urlopen(url)
            print(_fp)
            if isinstance(_fp, tuple):
                _fp = _fp[0]
                _data = _fp.read()
            else:
                _data = _fp.read().decode('utf8')
            print(_data)
            _json = json.loads(str(_data))
        except Exception as ex:
            _json = FAKE

        if "result" in _json and "wikidata" in _json["result"]\
                and "conteudo" in _json["result"]["wikidata"]:
            return _json["result"]["wikidata"]["conteudo"]
        else:
            return ""

    def parse_wiki(self, html_text):
        """Separa slides e items do texto

        :param html_text: texto em html contendo h1 e li
        :return: lista de itens na página
        """
        conteudo = html_text.split('</h1>')[1]
        return [item.split("</li>")[0] for item in conteudo.split("<li>")[1:]]

    def load_slides_from_wiki(self, item_list):
        """Cria slides e items do texto

        :param item_list: lista de itens a serem convertidos em slides
        :return: lista de slides criados
        """
        return [self.slide(item) for item in item_list]

    def build_cursor(self, slide, center):
        """Cria o cursor geométrico

        :return: o elemento grupo do cursor
        """
        self.cursor = Cursor(self.svgcanvas, self.svg, slide, center)
        self.build_cursor = lambda s, p:\
            self.cursor.setAttribute(s, 'transform', "translate (%d %d)" % p)

    def ad_template(self, template):
        FAKESVG = '<g>%s</g>' % ['<rect style="fill:red" x="%d" y="9" width="9" height="9" />' % x for x in range(10)]
        try:
            import urllib.request
            import json
            _fp = urllib.request.urlopen(MENUFPX % template.target.id[3:])
            print("ad_template", _fp)
            if isinstance(_fp, tuple):
                _fp = _fp[0]
            _data = _fp.read()

        except Exception as ex:
            _data = FAKESVG
        #_data = _data.split('<g')[1].split('</g>')[0]
        #close_g_tag = _data.find(">")
        #_data = _data[close_g_tag+1:]
        print("ad_template _data", _data)

        self.back.html = _data


class Cursor:
    """Cursor usado para modificar geometricamente um slide

    :param canvas: elemento svg do DOM
    :param svg: módulo svg do browser brython
    :param slide: o slide para o qual o cursor foi alocado
    :param position: a posição onde o cursor deve ser colocado
    """

    def _cursor_start_move(self, event, mover):
        self._move = mover
        self._mouse_pos = (event.x, event.y)

    def _move_slide(self, event):
        """Movimenta o cursor geométrico
        """
        self._mouse_pos = (event.x, event.y)
        self.cursor.setAttribute('transform', "translate (%d %d)" % (event.x, event.y))
        self.slide.move(event.x, event.y)

    def _widen_slide(self, event):
        """Enlarguesse o cursor geométrico
        """
        self._mouse_pos, delta = (event.x, event.y), event.x - self._mouse_pos[0]
        self.cursor.setAttribute('transform', "translate (%d %d)" % (event.x, event.y))
        self.slide.widen(delta)

    def _heighten_slide(self, event):
        """Enaltece o cursor geométrico
        """
        self._mouse_pos, delta = (event.x, event.y), event.y - self._mouse_pos[1]
        self.cursor.setAttribute('transform', "translate (%d %d)" % (event.x, event.y))
        self.slide.heighten(delta)

    def __init__(self, canvas, svg, slide, position=(0, 0)):
        x, y = position
        self.svg = svg
        self.slide = slide
        t45 = "rotate (45 0 0)"
        group = self.cursor = self.svg.g(Id="cursor", transform="translate (%d %d)" % position)
        ne = self.svg.rect(x=0, y=-35, width=35, height=35, style={"opacity": 0.5, "fill": "#b3b3b3"})
        se = self.svg.rect(x=0, y=0, width=35, height=35, style={"opacity": 0.5, "fill": "#b3b3b3"})
        sw = self.svg.rect(x=-35, y=0, width=35, height=35, style={"opacity": 0.5, "fill": "#b3b3b3"})
        nw = self.svg.rect(x=-35, y=-35, width=35, height=35, style={"opacity": 0.5, "fill": "#b3b3b3"})
        ww = self.svg.rect(x=0, y=-35, width=35, height=35, transform=t45, style={"opacity": 0.5, "fill": "#b3b3b3"})
        ss = self.svg.rect(x=0, y=0, width=35, height=35, transform=t45, style={"opacity": 0.5, "fill": "#b3b3b3"})
        ee = self.svg.rect(x=-35, y=0, width=35, height=35, transform=t45, style={"opacity": 0.5, "fill": "#b3b3b3"})
        nn = self.svg.rect(x=-35, y=-35, width=35, height=35, transform=t45, style={"opacity": 0.5, "fill": "#b3b3b3"})
        circle = self.svg.circle(cx=0, cy=0, r=35, style={"opacity": 0.5, "fill": "#ffffff"})
        eye = self.svg.circle(cx=0, cy=0, r=20, style={"opacity": 0.5, "fill": "#999999"})
        for element in [ne, se, sw, nw, nn, ee, ss, ww, circle, eye]:
            group <= element
        canvas <= group

        def end_move():
            self._move = lambda e: None
        end_move()
        eye.onmousedown = lambda e: self._cursor_start_move(e, self._move_slide)
        ee.onmousedown = lambda e: self._cursor_start_move(e, self._widen_slide)
        ww.onmousedown = lambda e: self._cursor_start_move(e, self._widen_slide)
        ss.onmousedown = lambda e: self._cursor_start_move(e, self._heighten_slide)
        nn.onmousedown = lambda e: self._cursor_start_move(e, self._heighten_slide)
        group.onmousemove = lambda e: self._move(e)
        group.onmouseup = lambda e: end_move()

    def setAttribute(self, slide, attr, value):
        """Muda o slide corrente e um atributo do slide

        :param slide: o novo slide que é controlado pelo cursor
        :param attr: o nome do atributo que vai mudado no cursor
        :param value: o valor novo do atributo
        """
        self.slide = slide
        self.cursor.setAttribute(attr, value)

MENUPX = "http://www.corsproxy.com/activufrj.nce.ufrj.br/static/desenhos/img%s.png"
MENUFPX = "http://www.corsproxy.com/activufrj.nce.ufrj.br/static/desenhos/img%s.svg"
EL, ED = [], {}
MENU_DEFAULT = ['ad_objeto', 'ad_cenario', 'wiki', 'navegar', 'jeppeto']


class Menu:
    MENU = {}

    def __init__(self, sprites, originator=None, **menu):
        self.sprites, self.originator = sprites, originator
        Id = self.Id = menu.keys()[0]
        self.action = self.build_item(Id, menu[Id])

    def __no__init__(self, gui, originator=None, menu=None, command='menu_',
                 prefix=MENUPX, event="click", activate=False, extra=EL):
        self.gui, self.item, self.prefix = gui, originator, prefix
        self.command, self.prefix, self.activated = command, prefix, activate
        self.originator = originator or "__ROOT__"
        self.book = self.gui.doc["book"]
        self.target, self.id, self.menu = self, '', None
        menu and self.build_menu(menu, extra=extra)

    def build_item(self, item, menu):
        self.sprites[item].render(self.originator, 0, 0, menu, item)

    def build_menu(self, menu=MENU_DEFAULT, display="none", extra=EL):
        #print ("build_menu:", self.gui.div)
        Menu.MENU[self.originator] = self
        self.menu = self.gui.div(
            self.gui.doc, s_position='absolute', s_top='50%', s_left='50%',
            s_display=display, s_border='1px solid #d0d0d0', o_Id=self.item)
        #print ('build_menu', [self.comm[kwargs['o_click']] for kwargs in menu])
        [self.build_item(item, EXTRA % item, self) for item in extra]
        [self.build_item(item, self.prefix % item, self) for item in menu]
        return self.menu

    def click(self, event):
        event.stopPropagation()
        event.preventDefault()
        self.menu.style.display = 'none'
        menu_id = event.target.id[2:]
        item = menu_id in Menu.MENU and menu_id or self.item
        obj = menu_id in Menu.MENU and Menu.MENU[menu_id] or self
        #self.activate(self.command or self.item, event, obj)
        print('click:', menu_id, self.command + item, self.menu.Id, self.prefix)  # , self.item, item)
        self.activate(self.command + item, event, obj)


class Sprite:
    """Gerencia uma coleção de sprites a partir de uma folha com imagens

    :param img: Url da folha de imagem
    :param dx: espaçamento x de cada sprite
    :param dy: espaçamento y de cada sprite
    :param offx: inicio em x da coleção de sprites (default 0)
    :param offy: inicio em y da coleção de sprites (default 0)
    :param padx: desconto em x de cada imagem do sprite (default 0)
    :param pady: desconto em y de cada imagem do sprite (default 0)
    :param x: posição em x na matriz de sprites deste sprite (default 0)
    :param y: posição em y na matriz de sprites deste sprite (default 0)
    :param Id: identificador do sprite no DOM ou no dicionário SPRITE
    """
    SPRITE = {}  # Coleção de sprites

    def __init__(self, img, dx, dy, offx=0, offy=0, padx=0, pady=0, x=0, y=0, Id=""):
        self.img, self.dx, self.dy, self.offx, self.offy, self.padx, self.pady = img, dx, dy, offx, offy, padx, pady
        self.x, self.y, self.Id = x, y, Id
        self.menu = None

    def sprites(self, **kwargs):
        """Recorta sprites da imagem e registra no dicionário SPRITE.

        :param kwargs: lista de argumentos da forma nome_do_sprite=[sprite_x, sprite_y]
        :return: o dicionário SPRITE
        """
        def cut_sprite(name, x, y):
            return Sprite(self.img, self.dx, self.dy, self.offx, self.offy, self.padx, self.pady, x, y, name)

        Sprite.SPRITE.update({name: cut_sprite(name, *coordinates) for name, coordinates in kwargs.items()})
        return Sprite.SPRITE

    def render(self, element, x=0, y=0, action=None, Id=""):
        """Desenha um sprite no elemento dado

        :param element: elemento onde o sprite vai ser desenhado
        :param x: posição x no elemento onde o sprite vai ser desenhado (default 0)
        :param y:  posição y no elemento onde o sprite vai ser desenhado (default 0)
        :param action: função aser chamada quando o sprite for clicado (default nenhuma)
        :param Id: identificador do sprite no DOM ou no dicionário SPRITE
        :return:
        """
        self.menu = GUI.html.DIV(Id=Id or "spr%s" % self.Id)
        self.menu.style.backgroundImage = "url(%s)" % self.img
        self.menu.style.position = "absolute"
        top = self.offy + self.y*self.dy + self.pady
        left = self.offx + self.x*self.dx + self.padx
        print(self.img, self.dx, self.dy, self.offx, self.offy, self.padx, self.pady, x, y, top, left)
        self.menu.style.top = y
        self.menu.style.left = x
        self.menu.style.width = self.dx - 2*self.padx
        self.menu.style.height = self.dy - 2*self.pady
        self.menu.style.backgroundPosition = "-%dpx -%dpx" % (left, top)
        self.menu.onclick = action if action else lambda ev: None
        element <= self.menu
