#!/usr/bin/env python3
'''
Morse Code Converter(Unicode)
Copyright (C) 2018 sosei

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
        "è": "..-..",
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
	return 'U+'+str.upper(str.zfill(str.lstrip(hex(ord(one_character)),'0x'), 4))  #和JS版本不同在于，hex函数转16进制会带“0x”前缀，JS的.toString(16)返回数不带前缀

def Unicode_number_To_Char (a_unicode_number: str) -> chr:
	return chr(int(str.replace(str.upper(a_unicode_number), 'U+', '0x'), 16))

def Do_MCarr_Match (mcarr_key: str, match_type_flag: str) -> str:
	"match_type_flag = 'char' or match_type_flag = 'code'"
	if match_type_flag == 'char':
		if len(mcarr_key) == 1:  #单个字符就转小写字符规范化下
			mcarr_key = str.lower(mcarr_key)
		return dict.get(char_from_morse_code, mcarr_key)
	elif match_type_flag == 'code':
		return dict.get(morse_code_from_char, mcarr_key)

def Telegraph_text_To_Morse_code (telegraph_text: str) -> list:
	mess = []
	for messarr in re.findall('(?:\{[\w #]+?\})|(?:.)', telegraph_text, re.S):  #依次 按“{...}” 或 单个字符 分割
		translated_string = Do_MCarr_Match(messarr, 'char')
		if translated_string != None:
			mess.append(translated_string)
		else:  #译摩尔斯码尝试失败则转如下判别
			if len(messarr) == 1:  #如是单个字符，则为非摩尔斯码表中字符，转译为“U+xxxx”样式Unicode再译摩尔斯码
				mess.extend(Telegraph_text_To_Morse_code(Char_To_Unicode_number(messarr)))  #这递归返回一个列表，所以用extend方法添加
			else:
				mess.append('{#}')  #错误的“{#}”项无法翻译会返回“{#}”
	return mess

def Morse_code_To_Telegraph_text (morse_code_text: str) -> str:
	mess = ''
	for messarr in re.finditer('([.-]+)|( {4,})|(\{#\})', morse_code_text):  #依次找出 摩尔斯码 或 4个及以上空格 或 “{#}”
		if messarr.group(1) != None:  #有找出摩尔斯码，则译码
			translated_string = Do_MCarr_Match(messarr.group(1), 'code')
			if translated_string == None :
				translated_string = '{#}'  #错误的摩尔斯码无法译出就给出“{#}”
			mess += translated_string
		elif messarr.group(2) != None:  #有找出空格，4或7空格转首个1空格，大于7的按增量4计算1空格
			space_len = len(messarr.group(2))
			if space_len == 7:
				mess += ' '
			elif space_len % 4 == 0:
				mess += ' '* (space_len // 4)
			else:
				mess += ' '* (1 + (space_len - 7) // 4)
		elif messarr.group(3) != None:  #有找出错误标志“{#}”，原样输出
			mess += messarr.group(3)
	return mess

def Do_Morse_Encrypt (telegraph_text: str) -> str:
	'电报文本译为摩尔斯码就调用这个函数'
	return str.join('   ', Telegraph_text_To_Morse_code(telegraph_text))  #电码间用三空格间隔连成摩尔斯码字符串

def Do_Morse_Decrypt (morse_code_text: str) -> str:
	'摩尔斯码译为电报文本就调用这个函数'
	return re.sub('(?i:U\+[0-9A-F]{4})', lambda regex_match: Unicode_number_To_Char(regex_match.group()), Morse_code_To_Telegraph_text(morse_code_text))  #先把译出来的电报字符连成字符串，再找出“U+四个hex数”样式替换成对应字符
