from PyInquirer import style_from_dict, Token, Separator
from time import sleep
import sys
style = style_from_dict({
    Token.Seperator: '#fff',
    Token.Selected: '#00BFFF',
    Token.QuestionMark: '#000',
    Token.Pointer: '#fff',
    Token.Instruction: '#fff',
    Token.Answer: '#008000 bold',
    Token.Question: '#FF7F50'
})


def display_label(msg):
   for char in msg:
        sleep(0.01)
        sys.stdout.write(char)
        sys.stdout.flush()
