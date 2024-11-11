import collections
import itertools
from textwrap import wrap

# Auteurs : Sophie Langensteiner et Siyu Liao
# Date : 2024-11-10
#
# But : Essayer de decrypter un cryptogramme qui a ete produit
# dans le fichier crypt.py. Il s'agit d'un encryptage en utilisant
# un dictionnaire de taille 256, qui les caractères mono-alphabétiques
# et complete le reste du dictionnaire par les caractères bi-alphabétiques
# les plus frequents.
# Ce programme utilise pour fonction principale decrypt(C) qui prend
# paramètre un cryptogramme C, et retourne un message M en format String
# de ce qui a pu être deviné sur le cryptogramme.
# Ce programme utilise différentes fonctions auxiliaires afin de decrypter
# C, il se base principalement sur la fréquence d'apparition des motifs binaires
# et leurs associations aux symboles les plus frequents.
# Cela prend aussi en compte de certaines règles de bases de francais comme
# pour les espaces, la formation de mot de 2 lettres correctes, ...
# Mais cela vérifie aussi si une fois decrypter, si certains caractères
# sont bien places en vérifiant pour le cas de bi-caractères.
# Cependant, ce programme n'est pas suffisant pour trouver le texte original.
# Ps : le programme peut prendre du temps à tourner lors de la fonction correction

def decrypt(C):
    # Fonction principale prend un cryptogram C en paramètre et retourne un
    # message M par rapport a celui-ci en utilisant des fonctions auxiliaires de
    # décryptages.
    fract_C = frac_8bits(C)
    binary_frequency = frequency_list(fract_C)
    symboles = ['e ', 's ', 'qu', '\r\n', 't ', ', ', 'es', 'en', ' d', 'nt',
                ' p', ' c', ' q', 'on', 're', 'me', ' l', ' e', 'de', 'c',
                'le', 'te', 'i', 'oi', 'é', 'ce', 'f', 'ue', 'se', 'n', 'co',
                'in', 'u', 'n ', 'ie', '\n', ' s', 'm', 'is', 'et', ' n',
                'ou', ' a', 'an', 'i ', 'g', 'tr', 'd', ' ', 'r ', 'it',
                "'e", 'a', 'pa', 'r', 'e', 'un', 'er', 's', 'ne', 'ur', 'la',
                'p', ' m', 'je', 'ê', 'ui', 't', 'el', 'st', 'ns', 'au', 'us',
                "'a", 'ti', 'em', 'ai', 'ut', 'pr', 'il', "'", 'l', ' j', 'u ',
                'ar', 'po', 'ma', 'ir', 'so', 'ch', 'x', 'e\r', 'si', 'a ', 'b',
                'pe', '-', 've', 'll', 'ra', 'or', ' t', 'mo', 'ss', 'l ', 'e,',
                "l'", 'v', 'o', 'vo', 'nc', 'eu', '; ', 'di', '. ', 'bl', 'nd',
                'D', ' r', 'os', 'y', 'ri', ' i', 'at', 'té', "'i", 'è', 'à ',
                's,', 'fa', 'ro', 'j', "u'", ' f', 'ée', 'no', 'é ', 'rt', 'as',
                'lu', 'ho', 'pl', 'to', 'E', 'ca', 'ét', ' u', 'dé', 's\r', ' v',
                ' o', 'ç', 'sa', ' à', 'mm', 't\r', '.', 'ta', ':', 'nn', 'om',
                'uv', 'ec', 'rs', 'io', 'ré', 'su', 'id', ',', 'M', 'da', 'ni',
                'C', 'av', '_', 'li', 'h', 'S', ' b', 'à', 'I', 'T', 'O', 'ô',
                'A', 'z', 'î', 'N', 'P', 'L', 'û', '?', 'R', 'J', 'ù', 'â', 'É',
                'U', ';', '[', ']', '«', 'V', '»', 'Q', 'Ê', 'B', '1', '(', ')',
                'È', 'X', '3', 'H', 'F', '6', '4', 'q', '2', 'G', 'Y', '5', '7',
                'ë', '8', 'ï', '9']

    dictionary = dictionary_generator(binary_frequency, fract_C, symboles)
    M = association(dictionary, symboles)

    return M


# ___________________Fonctions auxiliaires : QUESTION 2________________________


# ___________________Fractionne cryptogramme en 8 bits________________________
def frac_8bits(C):
    # Fractionne notre cryptogramme en 8 bits
    return wrap(C, 8)


# ___________________Fréquence des motifs binaires____________________________
def frequency_list(list_encoded_character):
    # Compte la fréquence d'apparition d'un encodage binaire dans un tableau
    return collections.Counter(list_encoded_character)


# ____________Classe symbole avec equivalence binaire__________________________
# Cree afin de faciliter la recherche du symbole, ou du motif binaire, lorsque
#  l'on cherche les caractéristiques d'un element, comme par exemple
#  lorsque l'on itère dans une liste, on peut facilement obtenir
#  le symbole et le motif binaire, et comparer plus facilement à d'autres valeurs
class SymbolBin:
    def __init__(self, symbol, binary):
        self.symbol = symbol  # Symbole associe
        self.binary = binary  # Motif binaire de 8 bits associe


# _____Stoppe la substitution quand certaines règles françaises respectées______
def stop_substitution(M_decrypt):
    # Pour la substitution par force brute des 9 premiers symboles
    # le 'e ', 's ', ', ', et '\r\n' sont souvent en tete de liste
    # vérifier s'ils respectent les bonnes règles grammaticales entre eux
    # permet d'améliorer le debut du décryptage, en réduisant les erreurs des
    # le debuts lors des associations dans le dictionnaire.
    for i in range(1, len(M_decrypt) - 1):
        actual_value = M_decrypt[i]
        previous_value = M_decrypt[i - 1]
        after_value = M_decrypt[i + 1]

        if actual_value == ('s ' or 'e '):
            if (previous_value or after_value) == ("\r\n" or ", "):
                return False
            if actual_value == 's ' and previous_value == ' e':
                return False
        if actual_value == ", " and (previous_value or after_value) == "\r\n":
            return False

    return True


# _________________Replace occurrence binaire par symbole voulu_______________

def replace_occurrence(check_modif, new_symbol, motif_bin):
    for element in check_modif:
        if element.binary == motif_bin:
            element.symbol = new_symbol

    return check_modif


# _____________________ Génère dictionnaire____________________________________
def dictionary_generator(bin_freq, fract_C, symboles):
    # Génère un dictionnaire de symboles ascii (mono et bi-caractères inclus)
    # à une equivalence binaire decide par leurs fréquences
    # Paramètre bin_freq représente une liste contenant les fréquences des
    # motifs binaires qui ont été recueilli dans un cryptogramme.

    check_modif = [SymbolBin("", i) for i in fract_C]

    # Avant d'associer chaque lettre, on essaie de partir sur un bon depart
    # d'association binaire symbole, pour cela, on teste toutes les permutations
    # pour les premiers 9 symboles et ont s'arrête quand aucune erreur
    # grammaticale n'a ete trouve.
    break_true = False
    for (binary, _) in bin_freq.most_common():
        for perm in itertools.permutations(symboles[:9]):
            for element in perm:
                check_modif = replace_occurrence(check_modif, element, binary)

            message = association(check_modif, fract_C)

            # Pour quitter les imbrications des boucles, on utilise break_true
            if stop_substitution(message):
                break_true = True
                break
            else:
                pass

        if break_true:
            break

    # Pour chaque caractère dans notre liste de symbole, on l'associe à une
    # valeur binaire en partant de la plus fréquente.
    for (binary, _) in bin_freq.most_common():
        for s in symboles:
            if ((not any(s in e.symbol for e in check_modif)) and
                    checkIfNotTwoSpace(check_modif, s, binary)):
                check_modif = replace_occurrence(check_modif, s, binary)

                break

    return check_modif


# ________________________Associe dictionnaire symbole__________________________

def association(equivalence_table, symboles):
    # Cree 1 texte a partir des symboles stockes dans equivalence table
    # equivalence_table est une liste de symboles avec leurs motifs 
    # binaires associes lors de leurs decryptages.
    message = ""
    for element in equivalence_table:
        message += element.symbol

    correction(message, equivalence_table, symboles)

    return message


# ___________________Retourne si c'est lettre seule correct_____________________

def is_alone_lettre(symbole):
    # La liste des lettres de l'alphabet pouvant être seule, exemple " a "
    alone_letter = ["a", "A", "X", "x", "y", "Y", "Ô", "ô", "I", "i", "v", "V",
                    "M", "m"]

    letter = symbole.replace(" ", "")

    if letter.isalpha():
        if letter not in alone_letter:
            return False

    return True


# ___________________Vérifie si mot commun_____________________________________
def is_a_two_word(word):
    word_lower = word.lower()
    # On prend le debut quelques lettres anglaises qui peuvent
    # être presente dans le debut d'un livre en ligne francais
    word_two_character = ['of', 'de', 'la', 'is', 'in', 'at', 'no', 'it',
                          'or', 'if', 'to', 'by', 'of', 'of', 'de', 'le', 'et',
                          'ma', 'en', 'né', 'en', 'et', 'sa', 'un', 'se', 'il',
                          'on', 'eu', 'du', 'dû', 'je', 'au', 'si', 'ce', 'ou',
                          'ne', 'me', 'je', 'ni', 'où', 'là', 'pu', 'pû', 'et',
                          'va', 'tu', 'te', 'vu', 'su', 'ai', 'es', 'ii', 'lu',
                          'ça', 'nu', 'mû', 've', 'vi', 'ta', 'be', 'so', 'an',
                          'do', 'as', 'by', 'it', 'we', 'do', 'he', 'ut', 'up',
                          'we', 'us', 'pg', 'xi', 'tu', 'eh', 'iv', 'ni', 'ix',
                          'oh', 'ah', 'xl', 'te', ]

    return word_lower in word_two_character


# ________________Vérifie concatenation forme un mot___________________________

def is_concat(word_one, word_two):
    # Enlève les espaces non utiles s'ils sont presents.
    # Par exemple pour le mot 1, ce serait un espace au debut
    # Pour le mot 2, ce serait un espace à la fin
    word_one = word_one.replace(" ", "")
    word_two = word_two.replace(" ", "")

    if word_one.isalpha() and word_two.isalpha():
        word = word_one + word_two

        if not is_a_two_word(word):
            return False

    return True


# ________________Vérifie si espace correct entre symbole____________________

def checkIfNotTwoSpace(list_modif, symbole, motif_bin):
    # En paramètre, on a la liste qu'on souhaite modifier,
    # En 2e le symbole qu'on souhaite insérer, en dernier paramètre,
    # on met le motif binaire qu'on veut remplacer par le symbole

    # On vérifie dans un premier temps si dans le symbole à remplacer
    # On a un espace à traiter :
    if " " in symbole:
        for i in range(1, len(list_modif)):
            if list_modif[i].binary == motif_bin:
                list_length = len(list_modif) - 1

                # CAS symbole à remplacer commence avec espace :
                if symbole.startswith(" ") and symbole != " ":

                    # ______ Cas pour le prédécesseur :____
                    # Valeur précédente
                    pred = list_modif[i - 1].symbol

                    # Cas 1 : 2 espaces entre symboles exemple : "a  a"
                    if pred.endswith(" "):
                            return False

                    # Cas 2 : Si lettre peut etre seule correct sinon Faux
                    elif pred.startswith(" "):
                      if not (is_alone_lettre(pred)):
                            return False

                    # ______ Cas pour le successeur : ____________
                    # Valeur suivante/ successeur
                    if not ((i + 1) > list_length):
                      suc = list_modif[i + 1].symbol
                      # Cas 1 : Voir si forme un mot de deux lettres.
                      if suc.endswith(" ") and not is_concat(symbole, suc):
                            return False

                        # Cas 2 : Si lettre peut etre seule correct sinon Faux
                      if suc.startswith(" ") and not (is_alone_lettre(symbole)):
                            return False

                # CAS symbole à remplacer fini avec espace :
                else:
                    # ______ Cas pour le prédécesseur :____
                    # Valeur précédente
                    pred = list_modif[i - 1].symbol

                    # Cas 1 : Si lettre peut être seule correct sinon Faux
                    if pred.endswith(" ") and not (is_alone_lettre(symbole)):
                        return False

                    # Cas 2 : Voir si forme un mot de deux lettres
                    if pred.startswith(" ") and not is_concat(pred, symbole):
                        return False

                    # ______ Cas pour le successeur : ____________
                    # Valeur suivante/ successeur
                    if not ((i + 1) > list_length):
                        suc = list_modif[i + 1].symbol

                        # Cas 1 : 2 espaces entre symboles exemple : "a  a"
                        if suc.startswith(" "):
                            return False

                        # Cas 2 : Si lettre peut être seule correct sinon Faux
                        if suc.endswith(" ") and not (is_alone_lettre(suc)):
                            return False
    # Cas si le symbole est un saut de ligne, on vérifie que le symbole
    # précédant n'est pas coupé, est formé bien un mot seul correct.
    if "\n" in symbole:
        for i in range(1, len(list_modif)):
            if list_modif[i].binary == motif_bin:
                # Valeur précédente
                pred = list_modif[i - 1].symbol
                if not (is_alone_lettre(pred)):
                    return False

    return True

# ________________Vérifie si caractères ne forment pas bi-caractères connus____
def correction(M_decrypt, list_dictionnaire, symboles):
    # Si on aperçoit un motif de bi-caractère verifier si on a bien le
    # bi-caractère et non pas 2 lettres combinées

    bicaracteres = ['e ', 's ', 't ', 'on', 'qu', ' d', 'es', 'en', 'de',
                    'nt', ' p', ' l', ' c', 're', 'le', 'te', 'an', 'ou', ' a',
                    'me', ' e', ' q', 'ce', 'in', ' s', 'is', 'n ', 'er', 'r ',
                    'co', ' n', 'tr', ' t', 'ut', 'ie', 'it', 'ns', 'se', 'ue',
                    'et', 'la', 'un', 'or', 'i ', 'ar', 'di', 'st', 'ai', 'ti',
                    'a ', 'il', '. ', 'ne', 'oi', 'pa', 'ur', 'us', 'ui', 'ch',
                    'ma', ' m', 'ro', 'pr', 'u ', 'el', 'ra', 'pe', "'e", 'po',
                    'au', 'si', 've', ' i', ' o', 'em', 'eu', 'll', 'at', 'je',
                    'nd', 'no', 'so', 'ée', 'l ', 'ir', 'ss', 'e,', 'os', 's,',
                    'vo', 'ri', "'a", ' f', '; ', ' r', 'mo', 'ho', 'é ',
                    'bl', 'io', 'pl', 'lu', 'to', 'ta', 'om', ' u', 'dé', 'nc',
                    'ét', 'as', 'ré', 'té', 'su', 'à ', ' j', "l'", ' v',
                    "'i", 'id', 'mm', 'ca', 'ec', ' b', 'av', "u'", 'sa',
                    'fa', 'rs', 'li', 'rt', 'da', 'ni', ' à', 'uv', 'nn']

    for i in range(len(M_decrypt) - 1):
        actual_value = M_decrypt[i]
        previous_value = M_decrypt[i - 1]
        after_value = M_decrypt[i + 1]

        pair = actual_value + after_value

        # Si la paire forme un bi-caractère, on doit vérifie si la paire
        # précédente forme aussi ou non un bi-caractère avec le symbole actuel
        # si oui alors, il n'y a pas eu d'erreur. Sinon, il faut changer notre
        # symbole
        if actual_value in symboles:
            index = symboles.index(actual_value)
            if pair in bicaracteres:
                if (previous_value + actual_value) not in bicaracteres:
                    # On cherche un symbole suivant qui ne forme pas un bi-caractère
                    # car si cela forme un bi-caractère cela aurait dû etre directement
                    # encode par un bi-caractère non de 2 symboles côte à côte
                    while symboles[index] + previous_value in bicaracteres:
                        index += 1
                        if index >= len(symboles):
                            break

            symbol_to_swap = symboles[index]
            for element in list_dictionnaire:
                # On remplace les symboles grace aux 2
                # if en parcourant la liste
                if element == symbol_to_swap:
                    element.symbol = actual_value

                if element == actual_value:
                    element.symbol = symbol_to_swap
