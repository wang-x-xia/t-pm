# 模块与外部模块管理模块
import os
import yaml
import re
import logging
from src.paths import get_module_dir, get_project_root

logger = logging.getLogger(__name__)

def check_module_data():
    """检查模块与外部模块管理数据的合理性"""
    module_dir = get_module_dir()
    valid = True
    success = []
    failure = []
    
    # 检查模块目录下的所有yaml文件
    for root, _, files in os.walk(module_dir):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    
                    # 检查必要字段
                    if file == "模块.yaml":
                        if '名称' not in data:
                            failure.append(f"{file_path} - 缺少必要字段: 名称")
                            failure.append("  修复建议: 添加 '名称' 字段，例如: 名称: 模块名称")
                            valid = False
                        if '代码' not in data:
                            failure.append(f"{file_path} - 缺少必要字段: 代码")
                            failure.append("  修复建议: 添加 '代码' 字段，指定模块对应的Python文件路径")
                            valid = False
                        if '方法' in data:
                            if not isinstance(data['方法'], list):
                                failure.append(f"{file_path} - 方法字段应该是列表")
                                failure.append("  修复建议: 方法字段应该是方法名称的列表")
                                valid = False
                            else:
                                for i, method in enumerate(data['方法'], 1):
                                    if not isinstance(method, str):
                                        failure.append(f"{file_path} - 方法 {i} 格式错误，应该是字符串")
                                        failure.append("  修复建议: 方法列表中每一项应该是方法名称字符串")
                                        valid = False
                        # 检查依赖字段
                        if '依赖' in data and not isinstance(data['依赖'], list):
                            failure.append(f"{file_path} - 依赖字段格式错误")
                            failure.append("  修复建议: 依赖字段应该是一个列表")
                            valid = False
                    
                    success.append(f"{file_path} - 检查通过")
                except yaml.YAMLError as e:
                    failure.append(f"{file_path} - YAML格式错误: {e}")
                    failure.append("  修复建议: 检查YAML格式是否正确，确保缩进和语法正确")
                    valid = False
                except Exception as e:
                    failure.append(f"{file_path} - 检查失败: {e}")
                    failure.append("  修复建议: 检查文件是否存在，权限是否正确")
                    valid = False
    
    return valid, success, failure

def check_module_files():
    """检查模块对应的Python文件是否存在，并创建内部模块映射"""
    module_dir = get_module_dir()
    project_root = get_project_root()
    valid = True
    success = []
    failure = []
    module_mapping = {}
    
    # 检查项目根目录下的所有Python文件（过滤掉虚拟环境目录）
    all_py_files = []
    for root, _, files in os.walk(project_root):
        # 过滤掉虚拟环境目录
        if '.venv' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                all_py_files.append(os.path.relpath(os.path.join(root, file), project_root))
    
    # 确保模块目录存在
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)
        success.append(f"创建模块目录: {module_dir}")
    
    # 检查模块目录下的所有模块.yaml文件
    for root, _, files in os.walk(module_dir):
        for file in files:
            if file == '模块.yaml':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    
                    # 检查必要字段
                    if '名称' not in data:
                        failure.append(f"{file_path} - 缺少必要字段: 名称")
                        failure.append("  修复建议: 添加 '名称' 字段，例如: 名称: 模块名称")
                        valid = False
                        continue
                    
                    if '代码' not in data:
                        failure.append(f"{file_path} - 缺少必要字段: 代码")
                        failure.append("  修复建议: 添加 '代码' 字段，指定模块对应的Python文件路径")
                        valid = False
                        continue
                    
                    module_name = data['名称']
                    code_path = data['代码']
                    full_code_path = os.path.join(project_root, code_path)
                    
                    # 检查Python文件是否存在
                    if not os.path.exists(full_code_path):
                        # 创建缺失的Python文件
                        os.makedirs(os.path.dirname(full_code_path), exist_ok=True)
                        with open(full_code_path, 'w', encoding='utf-8') as f:
                            f.write(f"""# {module_name}模块

""")
                        success.append(f"创建缺失的Python文件: {full_code_path}")
                    else:
                        success.append(f"Python文件存在: {full_code_path}")
                    
                    # 添加到模块映射
                    module_key = code_path.replace('.py', '').replace('/', '_')
                    module_mapping[module_key] = module_name
                    
                except yaml.YAMLError as e:
                    failure.append(f"{file_path} - YAML格式错误: {e}")
                    failure.append("  修复建议: 检查YAML格式是否正确，确保缩进和语法正确")
                    valid = False
                except Exception as e:
                    failure.append(f"{file_path} - 检查失败: {e}")
                    failure.append("  修复建议: 检查文件是否存在，权限是否正确")
                    valid = False
    
    # 显示所有Python文件
    success.append("\n所有Python文件:")
    for py_file in all_py_files:
        success.append(f"- {py_file}")
    
    # 显示模块映射
    success.append("\n模块映射:")
    for key, value in module_mapping.items():
        success.append(f"{key} → {value}")
    
    return valid, module_mapping, success, failure

def analyze_module_dependencies():
    """分析模块之间的依赖关系"""
    project_root = get_project_root()
    dependencies = {}
    
    # 扫描所有Python文件
    for root, _, files in os.walk(project_root):
        # 过滤掉虚拟环境目录
        if '.venv' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_root)
                
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 提取导入语句
                    imports = []
                    # 匹配 from ... import ... 语句
                    from_imports = re.findall(r'from\s+([\w\.]+)\s+import', content)
                    imports.extend(from_imports)
                    # 匹配 import ... 语句
                    import_imports = re.findall(r'import\s+([\w\.]+)', content)
                    imports.extend(import_imports)
                    
                    # 过滤掉标准库和第三方库
                    project_imports = []
                    for imp in imports:
                        # 只保留项目内的模块导入
                        if imp.startswith('src.') or imp in ['main']:
                            project_imports.append(imp)
                    
                    if project_imports:
                        dependencies[relative_path] = project_imports
                except Exception as e:
                    print(f"✗ 分析 {file_path} 时出错: {e}")
    
    return dependencies

def visualize_module_dependencies():
    """可视化展示模块依赖关系"""
    dependencies = analyze_module_dependencies()
    
    if not dependencies:
        print("没有找到模块依赖关系")
        return
    
    print("\n模块依赖关系:")
    print("====================================")
    
    for module, deps in dependencies.items():
        print(f"模块: {module}")
        if deps:
            print("依赖:")
            for dep in deps:
                print(f"  - {dep}")
        else:
            print("无依赖")
        print("------------------------------------")

def check_module_dependencies():
    """检查模块依赖关系的合理性"""
    project_root = get_project_root()
    module_dir = get_module_dir()
    valid = True
    success = []
    failure = []
    
    # 分析模块依赖
    dependencies = analyze_module_dependencies()
    
    # 检查模块.yaml文件中的依赖字段
    for root, _, files in os.walk(module_dir):
        for file in files:
            if file == '模块.yaml':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    
                    if '代码' in data and '依赖' in data:
                        code_path = data['代码']
                        module_deps = data['依赖']
                        
                        # 检查依赖是否存在（依赖名称是模块名称，对应 模块/{name}/模块.yaml）
                        for dep in module_deps:
                            dep_module_yaml = os.path.join(module_dir, dep, '模块.yaml')
                            if not os.path.exists(dep_module_yaml):
                                failure.append(f"{file_path} - 依赖模块不存在: {dep}")
                                failure.append(f"  修复建议: 确保依赖模块 {dep} 存在")
                                valid = False
                    else:
                        success.append(f"{file_path} - 无依赖或依赖字段不存在，跳过依赖检查")
                except Exception as e:
                    failure.append(f"检查 {file_path} 依赖时出错: {e}")
                    valid = False
    
    return valid, success, failure

def check_method_files():
    """检查所有模块中定义的方法是否都有对应的方法文件"""
    module_dir = get_module_dir()
    project_root = get_project_root()
    valid = True
    success = []
    failure = []
    
    # 遍历所有模块目录
    for root, _, files in os.walk(module_dir):
        for file in files:
            if file == '模块.yaml':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    
                    # 检查是否有代码路径
                    if '代码' in data:
                        code_path = data['代码']
                        full_code_path = os.path.join(project_root, code_path)
                        module_name = data.get('名称', '未知模块')
                        
                        # 方法文件应该存储在当前模块目录的方法子目录中
                        method_dir = os.path.join(os.path.dirname(file_path), '方法')
                        
                        # 检查Python文件是否存在
                        if os.path.exists(full_code_path):
                            # 提取Python文件中的所有函数
                            functions = extract_functions(full_code_path)
                            
                            if functions:
                                # 读取方法目录中的所有YAML文件，提取定义的函数名
                                defined_functions = []
                                if os.path.exists(method_dir):
                                    for method_file in os.listdir(method_dir):
                                        if method_file.endswith('.yaml'):
                                            method_file_path = os.path.join(method_dir, method_file)
                                            try:
                                                with open(method_file_path, 'r', encoding='utf-8') as mf:
                                                    method_data = yaml.safe_load(mf)
                                                if '定义' in method_data and '函数' in method_data['定义']:
                                                    defined_functions.append(method_data['定义']['函数'])
                                            except Exception as e:
                                                failure.append(f"读取方法文件失败: {method_file_path} - {e}")
                                                valid = False
                                
                                # 检查每个Python函数是否有对应的方法文件
                                for func_name in functions:
                                    if func_name not in defined_functions:
                                        failure.append(f"{file_path} - Python方法缺少对应的方法文件: {func_name}")
                                        failure.append(f"  修复建议: 在 {method_dir} 目录中创建方法文件，并在其中设置 '定义: {{函数: {func_name}}}'")
                                        valid = False
                                    else:
                                        success.append(f"{file_path} - Python方法对应的方法文件存在: {func_name}")
                            else:
                                success.append(f"{file_path} - Python文件中无方法定义，跳过方法文件检查")
                        else:
                            failure.append(f"{file_path} - Python文件不存在: {code_path}")
                            failure.append(f"  修复建议: 创建Python文件 {full_code_path}")
                            valid = False
                    else:
                        success.append(f"{file_path} - 无代码路径定义，跳过方法文件检查")
                except yaml.YAMLError as e:
                    failure.append(f"{file_path} - YAML格式错误: {e}")
                    failure.append("  修复建议: 检查YAML格式是否正确，确保缩进和语法正确")
                    valid = False
                except Exception as e:
                    failure.append(f"{file_path} - 检查失败: {e}")
                    failure.append("  修复建议: 检查文件是否存在，权限是否正确")
                    valid = False
    
    return valid, success, failure

def extract_functions(python_file):
    """从Python文件中提取所有函数名"""
    import ast
    functions = []
    
    try:
        with open(python_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析Python代码
        tree = ast.parse(content)
        
        # 遍历AST节点，找到所有函数定义
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
    except Exception as e:
        print(f"提取函数时出错: {python_file} - {e}")
    
    return functions

