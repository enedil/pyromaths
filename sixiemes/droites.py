#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Pyromaths
# Un programme en Python qui permet de créer des fiches d'exercices types de
# mathématiques niveau collège ainsi que leur corrigé en LaTeX.
# Copyright (C) 2006 -- Jérôme Ortais (jerome.ortais@pyromaths.org)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
#

import random
import math


def nodesep(ligne):
    """
    D\xc3\xa9fini les valeurs nodesep : 0 pour une extr\xc3\xa9mit\xc3\xa9, -0.5 pour une continuit\xc3\xa9
    @param ligne: droite, demi-droite, segment
    @type ligne: string
    """

    if ligne == 'droite':
        retour = ['-0.8', '-0.8']
    elif ligne == 'demi-droite':
        retour = ['0', '-0.8']
    else:
        retour = ['0', '0']
    return retour


def choix_points(n):
    """
    choisit n points parmi A, B, C, ..., Z
    @param n: nombre de points \xc3\xa0 choisir
    @type n: integer
    """

    points = [chr(i + 65) for i in range(26)]
    liste = []
    for i in range(n):
        liste.append(points.pop(random.randrange(len(points))))
    return liste


def choix_ligne(n):
    """
    Retourne n propositions parmi droite, segment et demi-droite
    @param n: nombre de propositions
    @type n: interger
    """

    lignes = ['droite', 'demi-droite', 'segment']
    (liste_lignes, retour) = ([], [])
    for i in range((n - 1) // len(lignes) + 1):
        liste_lignes.extend(lignes)
    for i in range(n):
        retour.append(liste_lignes.pop(random.randrange(len(liste_lignes))))
    return retour


def symboles(ligne):
    """
    Retourne les couples (), [] ou [) correspondant au type de ligne
    @param ligne: droite, demi-droite ou segment
    @type ligne: string
    """

    if ligne == 'droite':
        retour = ['(', ')']
    elif ligne == 'demi-droite':
        retour = ['[', ')']
    else:
        retour = ['[', ']']
    return retour


def prepare_tuple(lpoints, ligne):
    """
    Prepare deux tuples pour permettre l'affichage de la question et
    de la solution
    @param lpoints: les points de la figure
    @type lpoints: liste de lettres
    @param ligne: droite, demi-droite ou segment
    @type ligne: string
    """

    (retour_exo, retour_sol) = ([], [])

    #choix des deux points permettant de tracer la ligne :

    templist = [i for i in range(len(lpoints))]
    deuxpoints = []
    for i in range(2):
        deuxpoints.append(lpoints[templist.pop(random.randrange(len(templist)))])

    #choix des symbole correspondant à la ligne :

    lsymboles = symboles(ligne)
    retour_sol.append(lsymboles[0])
    retour_sol.extend(deuxpoints)
    retour_sol.append(lsymboles[1])
    retour_sol.append(ligne)

    #choix des trous pour l'exercice :

    alea = random.randrange(3)
    if alea > 1:
        retour_exo = ['\\ldots', '\\ldots', '\\ldots', '\\ldots',
                      '\\dotfill']
    elif alea > 0:
        retour_exo = ['\\ldots']
        retour_exo.extend(retour_sol[1:3])
        retour_exo.extend(['\\ldots', retour_sol[4]])
    else:
        retour_exo = retour_sol[:4]
        retour_exo.append('\\dotfill')
    return (tuple(retour_exo), tuple(retour_sol))


def tex_figure(liste, lpoints, nodesep=0):
    """
    \xc3\x89crit dans un fichier tex la construction de 3 points et \xc3\xa9ventuellement
    une droite, une demi-droite ou un segment.
    @param liste: liste d'exos ou corrigés
    @type liste: liste
    @param lpoints: liste de 3 points
    @type lpoints: liste de 3 strings
    @param nodesep: liste des dépassements pour pstricks
    @type nodesep: liste de 2 strings
    """

    ordonnees = ['0.5', '1', '1.5']
    l_ord = []
    for i in range(3):
        l_ord.append(ordonnees.pop(random.randrange(len(ordonnees))))
    points_coord = []
    for i in range(3):
        points_coord.append(l_ord[i])
        points_coord.append(lpoints[i])
    points_coord = tuple(points_coord)
    liste.append('  \\begin{pspicture}(-0.5,0.2)(4.5,2.2)\n')
    liste.append('    \\psset{PointSymbol=x}\n')
    liste.append('    \\pstGeonode[PosAngle=90](0.5,%s){%s}(2,%s){%s}(3.5,%s){%s}\n' %
               points_coord)
    if nodesep:
        liste.append('    \\pstLineAB[nodesepA=%s, nodesepB=%s]{%s}{%s}\n' %
                   tuple(nodesep))
    liste.append('  \\end{pspicture}\\\\\n')


def tex_ligne_tableau(exo, cor, ligne):
    """
    \xc3\x89crit une ligne de tableau dans un fichier tex
    @param exo: fichier d'exercices
    @type exo: file
    @param cor: fichier de corrections
    @type cor: file
    @param ligne: droite, demi-droite ou segment
    @type ligne: string
    """

    lpoints = choix_points(3)
    (exer, solution) = prepare_tuple(lpoints, ligne)
    exo.append('  \\hfill{} $%s %s%s %s$ \\hfill{} &\\hfill{}  %s \\hfill{} &\n' %
             exer)
    cor.append('  \\hfill{} $%s %s%s %s$ \\hfill{} &\\hfill{}  %s \\hfill{} &\n' %
             solution)
    lnodesep = nodesep(ligne)
    lnodesep.extend(solution[1:3])
    if exer != ('\\ldots', '\\ldots', '\\ldots', '\\ldots', '\\dotfill'):
        tex_figure(exo, lpoints)
    else:
        tex_figure(exo, lpoints, lnodesep)
    tex_figure(cor, lpoints, lnodesep)
    exo.append('  \\hline\n')
    cor.append('  \\hline\n')


def Droites():
    """
    \xc3\x89crit les 5 lignes du tableau
    @param exo: fichier d'exercices
    @type exo: file
    @param cor: fichier de corrections
    @type cor: file
    """
    exo = ["\\exercice", u"Compléter :\\par\n", '\\begin{tabular}{|p{3cm}|p{5cm}|c|}\n', '  \\hline\n', u'  \\hfill{} \\textbf{Nom} \\hfill{} & \\hfill{}\\textbf{Catégorie}\\hfill{} & \\textbf{Figure} \\\\\n \\hline\n']
    cor = ["\\exercice*", u"Compléter :\\par\n", '\\begin{tabular}{|p{3cm}|p{5cm}|c|}\n', '  \\hline\n', u'  \\hfill{} \\textbf{Nom} \\hfill{} & \\hfill{}\\textbf{Catégorie}\\hfill{} & \\textbf{Figure} \\\\\n \\hline\n']
    
    line = choix_ligne(5)
    for i in range(5):
        tex_ligne_tableau(exo, cor, line[i])

    exo.append('\\end{tabular}\n')
    cor.append('\\end{tabular}\n')
    return (exo, cor)


#------------------------------------------------------------------------------
# Parallèles et perpendiculaires
#------------------------------------------------------------------------------
#perp à (ac) passant par b => val2=('a', 'c', 'a', 'c', 'b', 'b', 'b', 'a'
#para à (ab) passant apr d => val2=('a', 'b', 'a', 'b', 'd', 'd')


def fig_perp(points, coor, solution=0, per=[], par=[]):
    val_enonce = (
        points[0],
        points[1],
        coor[0],
        coor[1],
        coor[2],
        coor[3],
        points[2],
        points[3],
        coor[4],
        coor[5],
        coor[6],
        coor[7],
        )
    pts = ('a', 'b', 'c', 'd')
    text = \
        """  \\begin{pspicture*}(-4,-4)(4,4)
    \multips(-3.6,4)(.4,0){20}{\psline(0,0)(0,-.05)}
    \multips(-4,-4)(.4,0){20}{\psline(0,0)(0,.05)}
    \multips(-4,-3.6)(0,.4){20}{\psline(0,0)(0.05,0)}
    \multips(4,-4)(0,.4){20}{\psline(0,0)(-.05,0)}
    \pstGeonode[PointName={%s,%s}](%s;%s){a}(%s;%s){b}
    \pstGeonode[PointName={%s,%s}](%s; %s){c}(%s; %s){d}\n""" % \
        val_enonce
    if solution:
        val_soluce = (
            pts[per[0]],
            pts[per[1]],
            pts[per[0]],
            pts[per[1]],
            pts[per[2]],
            pts[per[2]],
            pts[per[2]],
            pts[per[0]],
            pts[par[0]],
            pts[par[1]],
            pts[par[0]],
            pts[par[1]],
            pts[par[2]],
            pts[par[2]],
            )

        text = text + \
            """    \pstLineAB[nodesep=-4]{%s}{%s}
    \pstProjection[PointName=none]{%s}{%s}{%s}[e]\pstLineAB[nodesep=-7]{%s}{e}
    \pstRightAngle{%s}{e}{%s}
    \pstLineAB[nodesep=-4]{%s}{%s}
    \pstTranslation[PointName=none,PointSymbol=none]{%s}{%s}{%s}[f]
    \pstLineAB[nodesep=-7]{%s}{f}
  \end{pspicture*}\n""" % \
            val_soluce
    return text


def noms_sommets(nb):  # renvoie nb noms de sommets
    (listenb, listepts) = ([], [])
    for i in range(26):
        listenb.append(i + 65)
    for i in range(nb):
        listepts.append(chr(listenb.pop(random.randrange(26 - i))))
    listepts.sort()
    return tuple(listepts)


def cree_coordonnees(long=3):
    from math import floor
    alpha = random.randrange(180)
    k0 = random.randrange(50, 100) / 100.0
    a0 = alpha + random.randrange(30, 120)
    k1 = random.randrange(50, 100) / 100.0
    a1 = alpha + random.randrange(210, 300)
    return (long, alpha, long, alpha + 180, floor((k0 * 10) * long) /
            10.0, a0, floor((k1 * 10) * long) / 10.0, a1)


def enonce_perp(exo, cor):
    coor = cree_coordonnees(3)
    noms = noms_sommets(4)
    (par, per) = ([], [])
    lval = [0, 1, 2, 3]
    for i in range(3):
        par.append(lval.pop(random.randrange(len(lval))))
    lval = [0, 1, 2, 3]
    for i in range(3):
        per.append(lval.pop(random.randrange(len(lval))))
    exo.append(fig_perp(noms, coor))
    cor.append(fig_perp(noms, coor, 1, per, par))
    exo.append('''  \end{pspicture*}\\par
  \\begin{enumerate}
''')
    cor.append('''  \\par
  \\begin{enumerate}
''')
    s_per = u"  \\item Tracer la droite perpendiculaire à la droite $(%s%s)$ passant par $%s$\n"
    s_par = u"  \\item Tracer la droite parallèle à la droite $(%s%s)$ passant par $%s$\n"
    s_per = s_per % (noms[per[0]], noms[per[1]], noms[per[2]])
    s_par = s_par % (noms[par[0]], noms[par[1]], noms[par[2]])
    exo.append(s_par)
    cor.append(s_par)
    exo.append(s_per)
    cor.append(s_per)
    exo.append('  \\end{enumerate}\n')
    cor.append('  \\end{enumerate}\n')


def Perpendiculaires():
    exo = ["\\exercice", u"Réaliser les figures suivantes :\\par\n", '\\begin{multicols}{2}\n']
    cor = ["\\exercice*", u"Réaliser les figures suivantes :\\par\n", '\\begin{multicols}{2}\n']
    
    enonce_perp(exo, cor)
    
    exo.append('  \\columnbreak\n')
    cor.append('  \\columnbreak\n')
    
    enonce_perp(exo, cor)
    
    exo.append('\\end{multicols}\n')
    cor.append('\\end{multicols}\n')
    return (exo, cor)


#------------------------------------------------------------------------------
# Propriétés
#------------------------------------------------------------------------------


def fonction(angle, xa, ya, dist=0, droite='par'):
    """
    Retourne une fonction \xc3\xa0 utiliser avec psplot
    @param angle: compris entre 1 et 89\xc2\xb0 ou 91 et 179\xc2\xb0. Angle entre la droite et l'axe des abscisses
    @type angle:
    @param xa: abscisse d'un point de la droite
    @type xa:
    @param ya: ordonn\xc3\xa9e d'un point de la droite
    @type ya:
    @param dist: distance entre l'origine et la droite
    @type dist:
    @param droite: 'par' pour une parall\xc3\xa8le et 'per' pour une perpendiculaire
    """

    angle_rad = (angle * math.pi) / 180
    if droite == 'par':
        coef = math.floor(math.tan(angle_rad) * 100) / 100.0
        ord_or = math.floor(((ya - xa * math.tan(angle_rad)) - dist /
                            math.cos(angle_rad)) * 100) / 100.0
        return '{x %s mul %s add}' % (coef, ord_or)
    else:
        coef = math.floor(-100 / math.tan(angle_rad)) / 100.0
        return '{x %s mul}' % coef


def PointInter(angle, xa, ya, dist=0):
    angle_rad = (angle * math.pi) / 180
    coef1 = math.floor(math.tan(angle_rad) * 100) / 100.0
    ord_or1 = math.floor(((ya - xa * math.tan(angle_rad)) - dist / math.cos(angle_rad)) *
                         100) / 100.0
    coef2 = math.floor(-100 / math.tan(angle_rad)) / 100.0
    x = ord_or1 / (coef2 - coef1)
    y = x * coef2
    return ',PosAngle=%s](%s,%s)' % (45 + angle, math.floor(x * 100) /
            100.0, math.floor(y * 100) / 100.0)


def Points(angle, xa, ya, dist=0):
    angle_rad = (angle * math.pi) / 180
    coef = math.floor(math.tan(angle_rad) * 100) / 100.0
    ord_or = math.floor(((ya - xa * math.tan(angle_rad)) - dist / math.cos(angle_rad)) *
                        100) / 100.0
    lpos = []
    if -1.5 < -2 * coef + ord_or < 1.5:
        x = -1.5
        y = math.floor((x * coef + ord_or) * 100) / 100.0
        lpos.append('(%s,%s)' % (x, y))
    if -1.5 < 2 * coef + ord_or < 1.5:
        x = 1.5
        y = math.floor((x * coef + ord_or) * 100) / 100.0
        lpos.append('(%s,%s)' % (x, y))
    if -2 < (1.5 - ya + dist / math.cos(angle_rad) + xa * math.tan(angle_rad)) / \
        math.tan(angle_rad) < 2:
        y = 1.1
        x = math.floor(((y - ya + dist / math.cos(angle_rad) + xa * math.tan(angle_rad)) /
                       math.tan(angle_rad)) * 100) / 100.0
        lpos.append('(%s,%s)' % (x, y))
    if -2 < (-1.5 - ya + dist / math.cos(angle_rad) + xa * math.tan(angle_rad)) / \
        math.tan(angle_rad) < 2:
        y = -1.1
        x = math.floor(((y - ya + dist / math.cos(angle_rad) + xa * math.tan(angle_rad)) /
                       math.tan(angle_rad)) * 100) / 100.0
        lpos.append('(%s,%s)' % (x, y))
    return lpos


def figure(angle, xa, ya, dist, lpoints, noms, par_per, dist2=0):
    """

    @param angle:
    @param xa:
    @param ya:
    @param dist:
    @param lpoints:
    @param noms: 1: nomme la droite (AB)
                 2: nomme la dorite (d1)
    @param par_per: 1: parall\xc3\xa8les + perpendiculaires
                    2: 3 parall\xc3\xa8les
                    3: 2 perpendiculaires
    """

    ltxt = []
    ltxt.append('\\begin{pspicture*}[shift=-1.5](-2,-1.5)(2,1.5)')
    ltxt.append('    \\footnotesize')
    if par_per < 3:
        ltxt.append('    \\psplot[linewidth=1.5\\pslinewidth]{-2}{2}%s' %
                    fonction(angle, xa, ya))
        ltxt.append('    \\psplot[linewidth=1.5\\pslinewidth]{-2}{2}%s' %
                    fonction(angle, xa, ya, dist))
    else:
        ltxt.append('    \\psplot{-2}{2}%s' % fonction(angle, xa, ya))
        ltxt.append('    \\psplot{-2}{2}%s' % fonction(angle, xa, ya,
                    dist))
    if par_per == 2:
        ltxt.append('    \\psplot[linewidth=1.5\\pslinewidth]{-2}{2}%s' %
                    fonction(angle, xa, ya, dist2))
    else:
        ltxt.append('    \\psplot{-2}{2}%s' % fonction(angle, xa, ya,
                    droite='per'))
    if noms:  #nomme les droites par deux points
        if par_per != 2:  #2 points d'intersection
            ltxt.append('    \\pstGeonode[PointSymbol={none,x},PointName={%s,%s} %s{i1}%s{a1}' %
                        (lpoints[0], lpoints[1], PointInter(angle, xa,
                        ya), Points(angle, xa, ya)[0]))
            ltxt.append('    \\pstGeonode[PointSymbol={none,x},PointName={%s,%s} %s{i2}%s{b1}' %
                        (lpoints[2], lpoints[3], PointInter(angle, xa,
                        ya, dist), Points(angle, xa, ya, dist)[0]))
            ltxt.append('    \\pstGeonode[PointSymbol=none,PointName=none]%s{c1}%s{c2}' %
                        (Points(angle + 90, 0, 0)[0], Points(angle + 90,
                        0, 0)[1]))
        else:

              #pas de point d'intersection

            pts = Points(angle, xa, ya)
            ltxt.append('    \\pstGeonode[PointSymbol=x,PosAngle=%s,PointName={%s,%s}]%s{a1}%s{a2}' %
                        (angle + 45, lpoints[0], lpoints[1], pts[0], pts[1]))
            pts = Points(angle, xa, ya, dist)
            ltxt.append('    \\pstGeonode[PointSymbol=x,PosAngle=%s,PointName={%s,%s}]%s{b1}%s{b2}' %
                        (angle - (45.0 * dist) / abs(dist), lpoints[2],
                        lpoints[3], pts[0], pts[1]))
            pts = Points(angle, xa, ya, dist2)
            ltxt.append('    \\pstGeonode[PointSymbol=x,PosAngle=%s,PointName={%s,%s}]%s{c1}%s{c2}' %
                        (angle - (45.0 * dist2) / abs(dist2), lpoints[4],
                        lpoints[5], pts[0], pts[1]))
    else:

          #nomme les droites (d_1), ...

        if par_per != 2:  #2 points d'intersection
            ltxt.append('    \\pstGeonode[PointSymbol=none,PointName={none,%s} %s{i1}%s{a1}' %
                        (lpoints[0], PointInter(angle, xa, ya), Points(angle,
                        xa, ya)[0]))
            ltxt.append('    \\pstGeonode[PointSymbol=none,PointName={none,%s} %s{i2}%s{b1}' %
                        (lpoints[1], PointInter(angle, xa, ya, dist),
                        Points(angle, xa, ya, dist)[0]))
            ltxt.append('    \\pstGeonode[PointSymbol=none,PointName={none,%s}]%s{c1}%s{c2}' %
                        (lpoints[2], Points(angle + 90, 0, 0)[0], Points(angle +
                        90, 0, 0)[1]))
        else:
            pts = Points(angle, xa, ya)
            ltxt.append('    \\pstGeonode[PointSymbol=none,PosAngle=%s,PointName={%s,none}]%s{a1}%s{a2}' %
                        (angle + 45, lpoints[0], pts[0], pts[1]))
            pts = Points(angle, xa, ya, dist)
            ltxt.append('    \\pstGeonode[PointSymbol=none,PosAngle=%s,PointName={%s,none}]%s{b1}%s{b2}' %
                        (angle - (45.0 * dist) / abs(dist), lpoints[1],
                        pts[0], pts[1]))
            pts = Points(angle, xa, ya, dist2)
            ltxt.append('    \\pstGeonode[PointSymbol=none,PosAngle=%s,PointName={%s,none}]%s{c1}%s{c2}' %
                        (angle - (45.0 * dist2) / abs(dist2), lpoints[2],
                        pts[0], pts[1]))
    if par_per != 2:
        if angle < 90:
            ltxt.append('    \\pstRightAngle[RightAngleSize=.2]{c1}{i1}{a1}')
        else:
            ltxt.append('    \\pstRightAngle[RightAngleSize=.2]{c2}{i1}{a1}')
    if par_per == 3:
        if angle < 90:
            ltxt.append('    \\pstRightAngle[RightAngleSize=.2]{c1}{i2}{b1}')
        else:
            ltxt.append('    \\pstRightAngle[RightAngleSize=.2]{c2}{i2}{b1}')
    ltxt.append('  \\end{pspicture*}')
    return ltxt


def valeurs_figures(par_per):
    noms = random.randrange(2)
    if noms:
        lpoints = noms_sommets(6)
    else:
        lindices = [1, 2, 3]
        lpoints = []
        for i in range(3):
            lpoints.append('(d_%s)' % lindices.pop(random.randrange(len(lindices))))
    angle = random.randrange(1, 90) + 90 * random.randrange(2)
    xa = random.randrange(-5, 5) / 10.0
    ya = random.randrange(-3, 3) / 10.0
    if random.randrange(2):
        dist = random.randrange(4, 9) / 10.0
    else:
        dist = -random.randrange(4, 9) / 10.0
    if par_per == 2:
        if dist > 0:
            dist2 = -random.randrange(4, 9) / 10.0
        else:
            dist2 = random.randrange(4, 9) / 10.0
        return (angle, xa, ya, dist, lpoints, noms, dist2)
    else:
        return (angle, xa, ya, dist, lpoints, noms)


def enonce_prop(exo, cor):
    exo.append('\\begin{tabularx}{\\textwidth}[t]{|p{3cm}|p{4cm}|X|p{3cm}|}\n')
    exo.append('  \\hline\n')
    exo.append(u'  Données & Figure codée & Propriété & Conclusion \\\\ \n')
    cor.append('\\begin{tabularx}{\\textwidth}[t]{|p{3cm}|p{4cm}|X|p{3cm}|}\n')
    cor.append('  \\hline\n')
    cor.append(u'  Données & Figure codée & Propriété & Conclusion \\\\ \n')
    ltypes = [1, 2, 3]
    lexos = []
    for i in range(3):
        lexos.append(ltypes.pop(random.randrange(len(ltypes))))
    for i in range(3):
        exo.append('  \\hline\n')
        cor.append('  \\hline\n')
        v = valeurs_figures(lexos[i])
        if lexos[i] == 2:
            if v[5]:  #noms de la forme (AB), on ajoute des parenthèses
                exo.append('''  $(%s%s)//(%s%s)$\\par et\\par $(%s%s)//(%s%s)$ &
  \\begin{pspicture*}[shift=-1.5](-2,-1.5)(2,1.5)
  \\end{pspicture*}
  & & \\\\\n''' %
                         (v[4][0], v[4][1], v[4][2], v[4][3], v[4][0], v[4][1],
                         v[4][4], v[4][5]))
                cor.append('  $(%s%s)//(%s%s)$\\par et\\par $(%s%s)//(%s%s)$ & \n' %
                         (v[4][0], v[4][1], v[4][2], v[4][3], v[4][0], v[4][1],
                         v[4][4], v[4][5]))
            else:
                exo.append('''  $%s//%s$\\par et\\par $%s//%s$ &
  \\begin{pspicture*}[shift=-1.5](-2,-1.5)(2,1.5)
  \\end{pspicture*}
  & & \\\\\n''' %
                         (v[4][0], v[4][1], v[4][0], v[4][2]))
                cor.append('  $%s//%s$\\par et\\par $%s//%s$ & \n' % (v[4][0],
                         v[4][1], v[4][0], v[4][2]))
            cor.append('  %s & \n' % ('\n').join(figure(v[0], v[1], v[2],
                     v[3], v[4], v[5], lexos[i], v[6])))
            cor.append(u'  Si deux droites sont parallèles, alors toute parallèle à l\'une est parallèle à l\'autre. &\n')
            if v[5]:
                cor.append('$(%s%s)//(%s%s)$ \\\\\n  \\hline\n' % (v[4][2],
                         v[4][3], v[4][4], v[4][5]))
            else:
                cor.append('  $%s//%s$ \\\\\n  \\hline\n' % (v[4][1], v[4][2]))
        else:

            fig = random.randrange(2)
            if lexos[i] == 1:
                if v[5]:
                    if not fig:
                        exo.append('''  $(%s%s)//(%s%s)$\\par et\\par $(%s%s)\\perp(%s%s)$ &
  \\begin{pspicture*}[shift=-1.5](-2,-1.5)(2,1.5)
  \\end{pspicture*}
  & & \\\\\n''' %
                                 (v[4][0], v[4][1], v[4][2], v[4][3], v[4][0],
                                 v[4][1], v[4][0], v[4][2]))
                    cor.append('  $(%s%s)//(%s%s)$\\par et\\par $(%s%s)\\perp(%s%s)$ &\n' %
                             (v[4][0], v[4][1], v[4][2], v[4][3], v[4][0],
                             v[4][1], v[4][0], v[4][2]))
                else:
                    if not fig:
                        exo.append('''  $%s//%s$\\par et\\par $%s\perp%s$ &
  \\begin{pspicture*}[shift=-1.5](-2,-1.5)(2,1.5)
  \\end{pspicture*}
  & & \\\\\n''' %
                                 (v[4][0], v[4][1], v[4][0], v[4][2]))
                    cor.append('  $%s//%s$\\par et\\par $%s\perp%s$ &\n' %
                             (v[4][0], v[4][1], v[4][0], v[4][2]))
                if fig:
                    exo.append('  & %s & & \\\\\n' % ('\n').join(figure(v[0],
                             v[1], v[2], v[3], v[4], v[5], lexos[i])))
                cor.append('  %s & \n' % ('\n').join(figure(v[0], v[1], v[2],
                         v[3], v[4], v[5], lexos[i])))
                cor.append(u'  Si deux droites sont parallèles, alors toute perpendiculaire à l\'une est perpendiculaire à l\'autre. &\n')
                if v[5]:
                    cor.append('  $(%s%s)\\perp(%s%s)$ \\\\\n  \\hline\n' %
                             (v[4][2], v[4][3], v[4][0], v[4][2]))
                else:
                    cor.append('  $%s\perp%s$ \\\\\n  \\hline\n' % (v[4][1],
                             v[4][2]))
            else:
                if v[5]:
                    if not fig:
                        exo.append('''  $(%s%s)\\perp(%s%s)$\\par et\\par $(%s%s)\\perp(%s%s)$ &
  \\begin{pspicture*}[shift=-1.5](-2,-1.5)(2,1.5)
  \\end{pspicture*}
  & & \\\\\n''' %
                                 (v[4][0], v[4][1], v[4][0], v[4][2], v[4][2],
                                 v[4][3], v[4][0], v[4][2]))
                    cor.append('  $(%s%s)\\perp(%s%s)$\\par et\\par $(%s%s)\\perp(%s%s)$ &\n' %
                             (v[4][0], v[4][1], v[4][0], v[4][2], v[4][2],
                             v[4][3], v[4][0], v[4][2]))
                else:
                    if not fig:
                        exo.append('''  $%s\\perp%s$\\par et\\par $%s\perp%s$ &
  \\begin{pspicture*}[shift=-1.5](-2,-1.5)(2,1.5)
  \\end{pspicture*}
  & & \\\\\n''' %
                                 (v[4][0], v[4][2], v[4][1], v[4][2]))
                    cor.append('  $%s\\perp%s$\\par et\\par $%s\perp%s$ &\n' %
                             (v[4][0], v[4][2], v[4][1], v[4][2]))
                if fig:
                    exo.append('  & %s & & \\\\\n' % ('\n').join(figure(v[0],
                             v[1], v[2], v[3], v[4], v[5], lexos[i])))
                cor.append('  %s &\n' % ('\n').join(figure(v[0], v[1], v[2],
                         v[3], v[4], v[5], lexos[i])))
                cor.append(u'  Si deux droites sont perpendiculaires à une même troisième alors elles sont parallèles entre elles. &\n')
                if v[5]:
                    cor.append('  $(%s%s)//(%s%s)$ \\\\\n  \\hline\n' % (v[4][0],
                             v[4][1], v[4][2], v[4][3]))
                else:
                    cor.append('  $%s//%s$ \\\\\n  \\hline\n' % (v[4][0],
                             v[4][1]))
    exo.append('''  \\hline
\\end{tabularx}
''')
    cor.append('\\end{tabularx}\n')


def Proprietes():
    exo = ["\\exercice", u"Compléter le tableau suivant :\\par Les droites en gras sont parall\xe8les.\\par """]
    cor = ["\\exercice", u"Compléter le tableau suivant :\\par Les droites en gras sont parall\xe8les.\\par """]

    enonce_prop(exo, cor)
    return (exo, cor)