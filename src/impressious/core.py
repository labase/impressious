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


class Impressious:
    """Classe que define o editor de apresentações no espaço 2D

    :param navegador: Referência ao módulo navegador do Brython
    """
    def __init__(self, navegador):
        """Constroi os objetos iniciais. """
        self.gui = navegador
        self.svg = navegador.svg
        self.svgcanvas = None

    def build_base(self):
        """Constrói as partes do Jogo.

        :return: Self, referência a este objeto
        """
        python_div = self.gui.document['pydiv']
        self.svgcanvas = self.svg.svg(width=800, height=500)
        python_div <= self.svgcanvas
        return self

 
def main(doc, svg):
    print('Carinhas 0.1.0')
    carinhas = Carinhas(doc)
    carinhas.build_base(doc, svg)