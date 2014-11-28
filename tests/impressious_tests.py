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
Impressious - Teste Principal
############################################################

Verifica a funcionalidade do cliente web.

"""
import unittest
from impressious.core import Impressious, Slide, LOREM, DIM
from impressious import main
import sys
if sys.version_info[0] == 2:
    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch
WIKI = "https://activufrj.nce.ufrj.br/rest/wiki/activlets/Provas_2014_2"
WCONT = '{"status": 0, "result": {"wikidata": {"conteudo": "<h1>Carlo Emmanoel Tolla de Oliveira<\/h1><ol>' \
    '<li>Society is intrinsically<\/li><li> responsible for capitalism; says Sartre;<\/li>' \
    '<li>Society is intrinsically<\/li><li> responsible for capitalism; says Sartre;<\/li>' \
    '<li>Society is intrinsically<\/li><li> responsible for capitalism; says Sartre;<\/li>' \
    '<li>Society is intrinsically<\/li><li> responsible for capitalism; says Sartre;<\/li>' \
    '<li>Society is intrinsically<\/li><li> responsible for capitalism; says Sartre;<\/li>' \
    '</ol>"}}}'
ICONT = 'Society is intrinsically'


class ImpressiousTest(unittest.TestCase):
    class Evento:
        x = y = 42
    EV = Evento()

    def setUp(self):
        self.gui = MagicMock(name="gui")
        modules = {
            'urllib': self.gui,
            'urllib.request': self.gui.request,
            'urllib.request.urlopen': self.gui.request.urlopen
        }
        uop = MagicMock(name="file")
        self.gui.request.urlopen.return_value = (uop, 0, 0)
        uop.read = MagicMock(name="data", return_value=WCONT)
        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        self.gui.__le__ = MagicMock(name="APPEND")
        self.gui.side_effect = lambda *a, **k: self.gui
        self.gui.svg = self.gui.g = self.gui
        self.gui.document.__getitem__.return_value = self.gui
        self.app = Impressious(self.gui)
        Impressious.SLIDES = []

    def test_main(self):
        """cria um canvas svg"""
        imp = main(self.gui)
        self.assertIsInstance(imp, Impressious, "Intância não criada")
        self.gui.svg.assert_called_with(width=800, height=600)

    def test_slide(self):
        """cria um slide com texto"""
        self.app.build_base()
        g = self.app.slide()
        self.gui.svg.g.assert_called_with(transform='translate (10, 10)')
        self.gui.svg.foreignObject.assert_called_with(x=0, y=0, width=DIM[0], height=DIM[1])
        self.assertIsInstance(g, Slide, "Slide is not as expected: %s" % g)

    def test_two_slide(self):
        """cria dois slides com texto"""
        self.app.build_base()
        self.app.slide()
        g = self.app.slide()
        dx = 200  # DIM[0] * 2 + 30
        self.gui.svg.g.assert_called_with(transform='translate (200, 10)')
        self.assertIsInstance(g, Slide, "Slide is not as expected: %s" % g)

    def test_read_from_wiki(self):
        """le um texto da wiki"""
        self.app.build_base()
        w = self.app.read_wiki(WIKI)
        self.assertIn(ICONT, w, "Wiki is not as expected: %s" % w)

    def test_parse_from_wiki(self):
        """separa um texto da wiki em itens"""
        self.app.build_base()
        w = self.app.read_wiki(WIKI)
        l = self.app.parse_wiki(w)
        self.assertEqual(10, len(l), "list is not as expected: %s" % l)
        self.assertNotIn('<li', l[0], "item is not as expected: %s" % l[0])

    def test_load_slides_from_list(self):
        """separa um texto da wiki em itens"""
        self.app.build_base()
        w = self.app.read_wiki(WIKI)
        l = self.app.parse_wiki(w)
        self.assertEqual(10, len(l), "list is not as expected: %s" % l)
        self.assertNotIn('<li', l[0], "item is not as expected: %s" % l[0])

    def test_select_slide_and_show_cursor(self):
        """Seleciona um slide e mostra o cursor"""
        self.app.build_base()
        l = self.app.load_slides_from_wiki(['Society is intrinsically<\/li>'])
        self.assertEqual(1, len(l), "list is not as expected: %s" % l)
        self.app.SLIDES[0]._select(None)
        self.gui.svg.rect.assert_called_with(
            width=70, x=-35, style={'opacity': 0.5, 'fill': '#b3b3b3'}, transform='rotate (45 0 0)', height=70, y=-35)
        self.gui.svg.g.assert_called_with(transform="translate (100 100)", Id='cursor')

    def test_select_slide_and_switch_cursor(self):
        """Seleciona um slide e troca o cursor que estava em outro slide"""
        self.app.build_base()
        l = self.app.load_slides_from_wiki(['Society is intrinsically<\/li>','Society is intrinsically<\/li>'])
        self.assertEqual(2, len(l), "list is not as expected: %s" % l)
        self.app.SLIDES[0]._select(None)
        self.app.SLIDES[1]._select(None)
        self.gui.svg.g.assert_called_with(transform="translate (100 100)", Id='cursor')
        self.gui.svg.g.setAttribute.assert_called_with('transform', "translate (290 100)")
        #assert self.gui.svg.g.transform == 'translate (290 100)', self.gui.svg.g.transform

    def test_select_slide_move(self):
        """Seleciona um slide e move o slide junto com o cursor"""
        self.app.build_base()
        l = self.app.load_slides_from_wiki(['Society is intrinsically'])
        self.app.SLIDES[0]._select(None)
        self.app.cursor._cursor_start_move(self.EV, self.app.cursor._move_slide)
        self.assertEqual(self.app.cursor._mouse_pos, (42, 42))
        self.EV.x, self.EV.y = (84, 84)

        self.app.cursor._move(self.EV)
        self.assertEqual(self.app.cursor._mouse_pos, (84, 84), "but mouse pos is %d %d " % self.app.cursor._mouse_pos)
        self.assertEqual(self.app.SLIDES[0].position, (-6, -6), "but slide pos is %d %d " % self.app.SLIDES[0].position)
        self.gui.svg.g.setAttribute.assert_called_with('transform', "translate (-6 -6)")
        #self.assertEqual(self.gui.svg.g.mock_calls, [], "but slide pos is %s " % self.gui.svg.g.mock_calls)

if __name__ == '__main__':
    unittest.main()