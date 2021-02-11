# -*- coding: UTF-8 -*-

from typing import Union, Dict
import json
import re

from mcdreforged.api.types import ServerInterface
from mcdreforged.api.command import Literal, Number
from mcdreforged.api.rtext import RTextBase, RText, RTextTranslation, RTextList, RAction

PLUGIN_METADATA = {
    'id': 'homo_calculator',
    'version': '0.1.0',
    'name': 'HomoCalc',
    'description': 'Use command "!!homo <number>" to get a homosexual expression formatted by 114514',
    'author': [
        'Van_Involution'
    ],
    'link': 'https://github.com/Van-Involution/HomoCalc',
    'dependencies': {
        'mcdreforged': '>=1.0.0',
    }
}

DEFAULT_DATA_PATH = 'config/HomoData.json'
DEFAULT_PREFIX = '!!homo'
REPO_URL = PLUGIN_METADATA['link']

data = dict()  # type: Dict[str, str]


def get_data(path: str) -> Dict[str, str]:
    with open(path, 'r') as file:
        return json.load(file)


def demolish(number: str) -> str:
    global data
    if bool(re.search(r'\.(0*)$', number)):
        return demolish(number.strip('0').strip('.'))
    elif bool(re.search(r'\.([\d]*)$', number)):
        n = len(re.search(r'\.([\d]*)$', number.strip('0')).group().strip('.'))
        return f'{"(" * n}({demolish(number.replace(".", ""))}){"/((10)))" * n}'
    elif bool(re.match(r'^-', number)):
        return f'((-1))*({demolish(number[1:])})'
    elif number in data.keys():
        return f'({number})'
    else:
        div = 114514
        for key in data:
            if int(key) <= int(number):
                div = int(key)
                break
        return re.sub(
            r'(\*\(\(1\)\))|(\+\(0\))', '',
            f'({div})*({demolish(str(int(number) // div))})+{demolish(str(int(number) % div))}'
        )


def gen_expr(number: Union[int, float]) -> RTextBase:
    global data
    expr = demolish(str(number))
    for key, val in data.items():
        expr = re.sub(r'\(' + key + r'\)', val, expr)
    expr = re.sub(r'\+-', '-', expr)
    return RTextList(
        f'§7{str(number)}§r = ',
        RText(expr).h(RTextTranslation('chat.copy.click')).c(RAction.copy_to_clipboard, expr)
    )


def on_load(server: ServerInterface, prev):
    global data
    data = get_data(DEFAULT_DATA_PATH)
    server.register_help_message(DEFAULT_PREFIX, '用114514生成ホモ特有四则运算表达式')
    server.register_command(
        Literal(DEFAULT_PREFIX)
        .then(
            Number('num')
            .runs(lambda src, ctx: src.reply(gen_expr(ctx['num'])))
        )
    )
