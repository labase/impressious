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
from impressious.core import Impressious, LOREM
from impressious import main
import sys
if sys.version_info[0] == 2:
    from mock import MagicMock
else:
    from unittest.mock import MagicMock


class ImpressiousTest(unittest.TestCase):

    def setUp(self):
        self.gui = MagicMock(name="gui")
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
        self.gui.svg.foreignObject.assert_called_with(LOREM, x=10, y=10, width=240, height=180)
        self.assertEqual(self.gui, g, "Group is not as expected: %s" % g)

    def test_two_slide(self):
        """cria dois slides com texto"""
        self.app.build_base()
        g = self.app.slide()
        g = self.app.slide()
        self.gui.svg.g.assert_called_with()
        self.gui.svg.rect.assert_called_with(color='grey', y=10, width=240, x=510, height=180, opacity=0.2)
        self.assertEqual(self.gui, g, "Group is not as expected: %s" % g)


if __name__ == '__main__':
    unittest.main()