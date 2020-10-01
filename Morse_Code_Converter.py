#!/usr/bin/env python3
'''
Morse Code Converter(Unicode)
Copyright (C) 2020 sosei

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
'''
import re

char_from_morse_code = {
        "a": ".-",
        "b": "-...",
        "c": "-.-.",
        "d": "-..",
        "e": ".",
        "è": "..-..",  #lgtm [py/encoding-error]
        "f": "..-.",
        "g": "--.",
        "h": "....",
        "i": "..",
        "j": ".---",
        "k": "-.-",
        "l": ".-..",
        "m": "--",
        "n": "-.",
        "o": "---",
        "p": ".--.",
        "q": "--.-",
        "r": ".-.",
        "s": "...",
        "t": "-",
        "u": "..-",
        "v": "...-",
        "w": ".--",
        "x": "-..-",
        "y": "-.--",
        "z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        ".": ".-.-.-",
        ",": "--..--",
        ":": "---...",
        "?": "..--..",
        "’": ".----.",
        "-": "-....-",
        "/": "-..-.",
        "(": "-.--.",
        ")": "-.--.-",
        '"': ".-..-.",
        "=": "-...-",
        "{Understood}": "...-.",
        "{Error}": "........",
        "+": ".-.-.",
        "{Wait}": ".-...",
        "{End of work}": "...-.-",
        "{Starting signal}": "-.-.-",
        "@": ".--.-.",
        " ": " "
}

morse_code_from_char = {value: key for key, value in dict.items(char_from_morse_code)}

def Char_To_Unicode_number (one_character: chr) -> str:
	return 'U+' + str.upper(str.zfill(str.lstrip(hex(ord(one_character)), '0x'), 4))

def Unicode_number_To_Char (a_unicode_number: str) -> chr:
	return chr(int(str.replace(str.upper(a_unicode_number), 'U+', '0x'), 16))

def Do_MCarr_Match (mcarr_key: str, match_type_flag: str) -> str:
	"match_type_flag = 'char' or match_type_flag = 'code'"
	if match_type_flag == 'char':
		if len(mcarr_key) == 1:
			mcarr_key = str.lower(mcarr_key)
		return dict.get(char_from_morse_code, mcarr_key)
	elif match_type_flag == 'code':
		return dict.get(morse_code_from_char, mcarr_key)

def Telegraph_text_To_Morse_code (telegraph_text: str) -> list:
	mess = []
	for messarr in re.findall('(?:\{[\w #]+?\})|(?:.)', telegraph_text, re.S):
		translated_string = Do_MCarr_Match(messarr, 'char')
		if translated_string is not None:
			mess.append(translated_string)
		else:
			if len(messarr) == 1:
				mess.extend(Telegraph_text_To_Morse_code(Char_To_Unicode_number(messarr)))
			else:
				mess.append('{#}')
	return mess

def Morse_code_To_Telegraph_text (morse_code_text: str) -> str:
	mess = ''
	for messarr in re.finditer('([.-]+)|( {3,})|(\{#\})', morse_code_text):
		if messarr.group(1) is not None:
			translated_string = Do_MCarr_Match(messarr.group(1), 'code')
			if translated_string is None :
				translated_string = '{#}'
			mess += translated_string
		elif messarr.group(2) is not None:
			space_len = len(messarr.group(2))
			if space_len == 3:
				mess += ' '
			else:
				mess += ' ' * (1 + (space_len - 3) // 2)
		elif messarr.group(3) is not None:
			mess += messarr.group(3)
	return mess

def Do_Morse_Encrypt (telegraph_text: str) -> str:
	'The function is called when the telegraph text is translated into Morse code'
	return str.join(' ', Telegraph_text_To_Morse_code(telegraph_text))  #A three - space interval is used to form a Morse code string

def Do_Morse_Decrypt (morse_code_text: str) -> str:
	'This function is called when Morse code is translated into telegraph text'
	return re.sub('(?i:U\+[0-9A-F]{4})', lambda regex_match: Unicode_number_To_Char(regex_match.group()), Morse_code_To_Telegraph_text(morse_code_text))
