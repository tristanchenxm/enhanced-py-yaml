支持yaml中使用环境变量的yaml读取
比如yaml定义如下:
```yaml
root:
  b1:
    k1: ${env_k1} # 假使环境变量已经定义了env_k1为v1
  b2:
    k1: ${root.b1.k1}
```
将会搜索环境变量和yaml本身的上下文，将${env.k1}和{root.b1.k1}都替换成v1.
使用方法：
```python
import yaml_reader
config = yaml_reader.YamlReader('file_location').config
# or
src = '''root:
  b1:
    k1: v1
  b2:
    k1: ${root.b1.k1}'''
config = yaml_rader.YamlReader(config=src).config
```