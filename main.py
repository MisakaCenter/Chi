import operator as op

"""我太菜了 我是废物"""


def reader(content):
    return content.replace('我太菜了', ' 我太菜了 ').replace('我是废物', ' 我是废物 ').split()


def builder(data):
    if len(data) == 0:
        print('<Error> 等死吧，傻逼')
        return
    word = data.pop(0)
    if word == '我太菜了':
        exp = []
        while data[0] != '我是废物':
            exp.append(builder(data))
        data.pop(0)
        return exp
    elif word == '我是废物':
        print('<Error> 等死吧，傻逼')
        return
    else:
        return atom(word)


def atom(data):
    try:
        return int(data)
    except ValueError:
        try:
            return float(data)
        except ValueError:
            _str = str(data)
            if _str == 'True':
                return True
            elif _str == 'False':
                return False
            return _str


def initial_env():
    env = Env()
    env['神说'] = lambda *x: x[-1]
    env['加'] = op.add
    env['减'] = op.sub
    env['乘'] = op.mul
    env['除'] = op.truediv
    env['大于'] = op.gt
    env['小于'] = op.lt
    env['大于等于'] = op.ge
    env['小于等于'] = op.le
    env['等于'] = op.eq
    env['等于？'] = op.is_
    env['我说'] = print
    env['列表'] = lambda *x: list(x)
    env['首先'] = lambda x: x[0]
    env['其余'] = lambda x: x[1:]
    env['连接'] = lambda x, y: [x] + y
    return env


class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        super().__init__()
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var: object) -> object:
        if var in self:
            return self
        elif not self.outer is None:
            return self.outer.find(var)
        else:
            print('<Error> 等死吧，傻逼')
            return self


class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return translator(self.body, Env(self.parms, args, self.env))


environment = initial_env()


def translator(x, env=environment):
    if isinstance(x, list):
        if len(x) == 0:
            print('<Error> 等死吧，傻逼')
            return

    if isinstance(x, str):
        return env.find(x)[x]

    elif not isinstance(x, list):
        return x
    elif x[0] == '曰':
        _, *args = x
        return args[0]
    elif x[0] == '如果':
        (_, test, conseq, alt) = x
        exp = (conseq if translator(test, env) else alt)
        return translator(exp, env)
    elif x[0] == '定义':
        (_, symbol, exp) = x
        env[symbol] = translator(exp, env)
    elif x[0] == '迟说':
        (_, symbol, exp) = x
        env[symbol] = translator(exp, env)
    elif x[0] == '入':
        (_, parms, body) = x
        return Procedure(parms, body, env)
    elif x[0] == '设定':
        (_, symbol, exp) = x
        env.find(symbol)[symbol] = translator(exp, env)
    else:
        proc = translator(x[0], env)
        args = [translator(arg, env) for arg in x[1:]]
        return proc(*args)


def chi_to_str(exp):
    if isinstance(exp, list):
        return '我太菜了 ' + ' '.join(map(chi_to_str, exp)) + ' 我是废物'
    else:
        return str(exp)


def loop(prompt = 'Chi> '):
    while True:
        val = translator(builder(reader(input(prompt))))
        if val is not None:
            print(chi_to_str(val))


if __name__ == '__main__':
    loop()

# Chi> 我太菜了 定义 圆的面积 我太菜了 入 我太菜了 半径 我是废物 我太菜了 乘 3.14 我太菜了 乘 半径 半径 我是废物 我是废物 我是废物 我是废物
# Chi> 我太菜了 圆的面积 2 我是废物
# 12.56
# Chi> 我太菜了 定义 阶乘 我太菜了 入 我太菜了 计数 我是废物 我太菜了 如果 我太菜了 小于等于 计数 1 我是废物 1 我太菜了 乘 计数 我太菜了 阶乘 我太菜了 减 计数 1 我是废物 我是废物 我是废物 我是废物 我是废物 我是废物
# Chi> 我太菜了 阶乘 10 我是废物
# 3628800
# Chi> 我太菜了 定义 数数 我太菜了 入 我太菜了 目标 列 我是废物 我太菜了 如果 列 我太菜了 加 我太菜了 等于？ 目标 我太菜了 首先 列 我是废物 我是废物 我太菜了 数数 目标 我太菜了 其余 列 我是废物 我是废物 我是废物 0 我是废物 我是废物 我是废物
# Chi> 我太菜了 数数 0 我太菜了 列表 0 1 2 3 4 0 0 1 2 3 4 我是废物 我是废物
# 3
# Chi> 我太菜了 神说 我太菜了 定义 注定的 250 我是废物 我太菜了 大于 注定的 注定的 我是废物 我是废物
# False
# Chi> 我太菜了 定义 呵呵 我太菜了 列表 1 1 1 1 我是废物 我是废物
# Chi> 呵呵
# 我太菜了 1 1 1 1 我是废物
# Chi> 我太菜了 我说 呵呵 我是废物
# [1, 1, 1, 1]
# Chi> 我太菜了 定义 我失败，谁赞同，谁反对 True 我是废物
# Chi> 我太菜了 我说 我失败，谁赞同，谁反对 我是废物
# True