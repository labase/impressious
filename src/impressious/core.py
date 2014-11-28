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
        self.gui = navegador
        self.svg = navegador.svg
        self.html = navegador.html
        self.ajax = navegador.ajax
        self.svgcanvas = self.cursor = None
        self.dim = (800, 600)

    def build_base(self, width=800, height=600):
        """Constrói as partes do Jogo.

        :return: Self, referência a este objeto
        """
        python_div = self.gui.document['pydiv']
        self.dim = width, height
        self.svgcanvas = self.svg.svg(width=width, height=height)
        python_div <= self.svgcanvas
        return self

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
        ee.onmousedown = ww.onmousedown = lambda e: self._cursor_start_move(e, self._widen_slide)
        ss.onmousedown = nn.onmousedown = lambda e: self._cursor_start_move(e, self._heighten_slide)
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
