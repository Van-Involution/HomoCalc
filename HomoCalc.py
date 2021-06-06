from typing import Union, Dict, Any
import json
import re

from mcdreforged.api.types import ServerInterface, CommandSource
from mcdreforged.api.command import Literal, GreedyText
from mcdreforged.api.rtext import RText, RTextTranslation, RTextList, RColor, RAction

PLUGIN_METADATA = {
    'id': 'homo_calculator',
    'version': '1.0.2',
    'name': 'HomoCalc',
    'description': RText('通过 "!!homo <number>" 命令, 用114514生成ホモ特有表达式').h(RText('良い世, 来いよ', RColor.gold)),
    'author': [
        'Van_Nya'
    ],
    'link': 'https://github.com/Van-Nya/HomoCalc',
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
    if bool(number.startswith('-')):
        return f'-({demolish(number[1:])})'
    elif bool(re.search(r'\.0*$', number)):
        return demolish(re.sub(r'\.0*$', '', number))
    elif bool(re.search(r'\.[\d]*$', number)):
        n = len(re.search(r'\.[\d]*$', number.strip('0')).group().strip('.'))
        return f'({demolish(number.replace(".", ""))})*((10))**({demolish(str(-n))})'
    elif number in data.keys():
        return f'({number})'
    else:
        div = 114514
        for key in data:
            if int(key) <= int(number):
                div = int(key)
                break
        return re.sub(
            r'(\+\(0\))|(\*\(\(1\)\))', '',
            f'({div})*({demolish(str(int(number) // div))})+{demolish(str(int(number) % div))}'
        )


def gen_expr(number: Union[int, float]) -> str:
    """
    Generate homo expression

    :param number: A integer or float to 'demolish'
    :return: A string of expression
    """
    global data
    homo = demolish(str(number))
    for key, val in data.items():
        homo = homo.replace(f'({key})', val)
    return homo.replace('+-', '-')


def reply(src: CommandSource, ctx: Dict[Union[str, Any], Union[str, Any]]):
    expr = ctx['expr'].replace('//', '/')
    if not bool(re.search(r'[^\d. (+\-*/)]', expr)):
        try:
            num = eval(expr)  # type: Union[int, float]
            homo = gen_expr(num)
            src.reply(RTextList(
                RText(re.sub(r'\.0*$', '', str(num)), RColor.gray).c(RAction.copy_to_clipboard, expr).h(expr),
                ' = ', RText(homo).c(RAction.copy_to_clipboard, homo).h(RTextTranslation('chat.copy.click'))
            ))
        except Exception as e:
            src.get_server().logger.warning(e)
            src.reply(RText('这么恶臭的表达式还有计算的必要吗, 自裁罢(无慈悲', RColor.red))
    else:
        src.reply(RText('参数包含非法字符!', RColor.red))


def on_load(server: ServerInterface, prev):
    global data
    data = get_data(DEFAULT_DATA_PATH)
    server.register_help_message(DEFAULT_PREFIX, RText('将输入的数或表达式转换成ホモ特有表达式').h('表达式参数支持Python格式的四则运算(+-*/)和乘方(**)'))
    server.register_command(Literal(DEFAULT_PREFIX).runs(lambda src: src.reply(RText('请输入参数以生成表达式!', RColor.red))).then(GreedyText('expr').runs(reply)))
