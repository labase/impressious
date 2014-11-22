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
from impressious.core import Impressious
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
        self.gui.svg = self.gui
        self.gui.document.__getitem__.return_value = self.gui
        self.app = Impressious(self.gui)

    def test_main(self):
        """cria um canvas svg"""
        imp = main(self.gui, self.gui)
        self.assertIsInstance(imp, Impressious, "Intância não criada")
        self.gui.svg.assert_called_with(width=800, height=500)


if __name__ == '__main__':
    unittest.main()