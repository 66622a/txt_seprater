# txt_seprater
TXT分割器，支持进度目录，用于手环

## 使用方法
使用`pip install opencc`安装繁体转简体模块（可选，如不需要可在代码中注释）后，将需要合并的txt文件与`main.py`置于同一目录下，运行即可

## 如何打包为.exe？
使用`pip install pyinstaller`安装pyinstaller后
### 需要 OpenCC的：
执行：
```cmd
pyinstaller --onefile --add-data "<你的Python安装目录>\site-packages\opencc\config\*;opencc/config" --add-data "<你的Python安装目录>\site-packages\opencc\dictionary\*;opencc/dictionary"  .\main.py
```
### 不需 OpenCC的
执行：
```cmd
pyinstaller --onefile .\main.py
```
