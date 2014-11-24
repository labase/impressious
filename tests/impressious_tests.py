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
from impressious.core import Impressious, LOREM, DIM
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

    def test_main(self):
        """cria um canvas svg"""
        imp = main(self.gui)
        self.assertIsInstance(imp, Impressious, "Intância não criada")
        self.gui.svg.assert_called_with(width=800, height=600)

    def test_slide(self):
        """cria um slide com texto"""
        self.app.build_base()
        g = self.app.slide()
        self.gui.svg.g.assert_called_with()
        self.gui.svg.foreignObject.assert_called_with(x=10, y=10, width=DIM[0], height=DIM[1])
        self.assertEqual(self.gui, g, "Group is not as expected: %s" % g)

    def test_two_slide(self):
        """cria dois slides com texto"""
        self.app.build_base()
        g = self.app.slide()
        g = self.app.slide()
        self.gui.svg.g.assert_called_with()
        dx = DIM[0] * 2 + 30
        self.gui.svg.rect.assert_called_with(color='grey', y=10, width=DIM[0], x=dx, height=DIM[1], opacity=0.2)
        self.assertEqual(self.gui, g, "Group is not as expected: %s" % g)

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

if __name__ == '__main__':
    unittest.main()