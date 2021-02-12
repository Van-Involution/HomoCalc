# HomoCalc

这么臭的插件真的会有人用 :horse:？不会吧不会吧不会吧（

> **注意**：HomoCalc 基于 [**MCDR v1.x**](https://github.com/Fallen-Breath/MCDReforged) 开发，并且**不支持** MCDR v0.x

**HomoCalc** 是一个 MCDR 插件，移植了 [itoor](https://github.com/itorr)/[**homo**](https://github.com/itorr/homo) 的程序和数据到 MCDR 平台，提供将给定的数或表达式转化成**ホモ特有表达式**的命令 `!!homo`，以及可被其他插件调用的**ホモ特有表达式**生成器函数 `gen_expr()`。

## 安装插件

### 最新发布

在 [**Releases 页面**](https://github.com/Van-Involution/HomoCalc/releases)下载最新的 `HomoCalc-<版本号>.zip`，解压后将 `HomoCalc.py` 放入 `plugins/` 目录中，将 `HomoData.json` 放入 `config/` 目录中。

### 最新源码

将仓库克隆（`git clone`）至 `plugins/` 目录中，复制一份 `HomoData.json` 放入 `config/` 目录中，并按如下代码块编辑 **MCDR 实例**的 `config.yml`：

```YAML
# The list of directory path where MCDR will search for plugin to load
# Example: "path/to/my/plugin/directory"
plugin_directories:
- plugins
- plugins/HomoCalc
```

## 使用插件

### 命令

插件提供如下格式的命令：

```
!!homo <表达式>
```

参数 `<表达式>` 支持整数、浮点数，以及 **Python** 格式的四则运算 (`+-*/`) 和乘方 (`**`) 表达式，在保证格式符合 **Python** 语法的前提下，可以带有空格。

### 函数

插件定义了一个可供引用的生成器函数：

```Python
def gen_expr(number: Union[int, float]) -> str
```
参数 `number` 是一个用于生成**ホモ特有表达式**的整数或浮点数。
