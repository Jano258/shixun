文档检索系统部署说明书
环境要求
在部署文档检索系统之前，请确保您的计算机满足以下环境要求：
1.操作系统：Windows, MacOS 或 Linux
2.Python版本：3.6 及以上
3.必要库：
1.docx
2.pdfplumber
3.pandas
4.scikit-learn
5.Tkinter（用于图形用户界面）
安装步骤
1. 获取项目代码
首先，解压文件‘202158334055-宋永康.zip’，然后复制项目的代码（py2.py）到您的本地计算机上。
2. 创建虚拟环境
建议创建一个虚拟环境来隔离项目的依赖关系：
bash
python -m venv venvsource venv/bin/activate # 对于Linux和MacOS
venv\Scripts\activate # 对于Windows
3. 安装依赖库
使用以下命令安装项目所需的依赖库：
bash
pip install -r requirements.txt
如果没有 requirements.txt 文件，请手动安装所需的库：
bash
pip install python-docx pdfplumber pandas scikit-learn tk
4. 配置初始数据目录
确保在项目目录下有一个名为 data 的文件夹，并将需要检索的文档放入该文件夹中。支持的文档格式包括 .docx, .pdf, .txt, .xlsx 等。
5. 配置 PyCharm
5.1.打开 PyCharm 并选择 “Open” 打开项目目录。
5.2.配置项目解释器：
5.2.1打开 File -> Settings (Windows) 或 PyCharm -> Preferences (MacOS)。
5.2.2在 Project: <project_name> 下选择 Python Interpreter。
5.2.3选择项目使用的虚拟环境解释器，如果没有虚拟环境，请选择 Python 解释器并点击 Apply。
5.3.配置依赖库：
确保所有必要的库都已安装，如果未安装，请使用上述命令手动安装。
6. 运行项目
在 PyCharm 中，找到项目的主脚本文件（例如 py2.py），右键点击并选择 “Run 'py2'” 运行项目。
7. 使用说明
启动应用程序后，将会出现一个图形用户界面（GUI），请按以下步骤操作：
1.选择文件夹：点击 “选择文件夹” 按钮，选择包含文档的目录。
2.输入关键词：在 “请输入关键词” 输入框中输入查询关键词。
3.设置搜索数量：在 “搜索数量” 输入框中输入希望返回的文档数量。
4.执行搜索：点击 “Search” 按钮，系统将根据输入的关键词进行文档检索，并在下方文本区域显示检索结果，包括文档名称及相关度评分。
注意事项
确保文档目录路径正确，并且目录中包含的文档格式支持系统处理。
在进行大规模文档检索时，建议使用高性能计算资源以提高检索效率。
系统当前支持的文档格式为 .docx, .pdf, .txt, .xlsx，如需支持其他格式，请相应修改 DocumentReader 类中的读取方法。
技术支持
如在安装或使用过程中遇到任何问题，自行解决。
