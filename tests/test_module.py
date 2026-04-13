# 模块-方法映射完整性测试
import os
import ast
import yaml
import pytest
from src.paths import get_module_dir, get_project_root


def load_all_modules():
    """加载所有模块的 YAML 数据"""
    module_dir = get_module_dir()
    modules = {}
    for root, _, files in os.walk(module_dir):
        for file in files:
            if file == '模块.yaml':
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                modules[file_path] = data
    return modules


def extract_functions_from_file(python_file):
    """从 Python 文件中提取所有函数名"""
    functions = []
    with open(python_file, 'r', encoding='utf-8') as f:
        content = f.read()
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
    return functions


def load_method_files(method_dir):
    """加载方法目录中所有方法 YAML 文件的函数映射"""
    defined_functions = []
    if not os.path.exists(method_dir):
        return defined_functions
    for method_file in os.listdir(method_dir):
        if method_file.endswith('.yaml'):
            method_file_path = os.path.join(method_dir, method_file)
            with open(method_file_path, 'r', encoding='utf-8') as f:
                method_data = yaml.safe_load(f)
            if '定义' in method_data and '函数' in method_data['定义']:
                defined_functions.append(method_data['定义']['函数'])
    return defined_functions


class TestModuleMethodMapping:
    """测试模块与方法的映射完整性"""

    def test_all_modules_have_code_field(self):
        """所有模块必须有代码字段"""
        modules = load_all_modules()
        for file_path, data in modules.items():
            assert '代码' in data, f"{file_path} 缺少代码字段"

    def test_all_module_code_files_exist(self):
        """所有模块指定的代码文件必须存在"""
        project_root = get_project_root()
        modules = load_all_modules()
        for file_path, data in modules.items():
            if '代码' in data:
                code_path = os.path.join(project_root, data['代码'])
                assert os.path.exists(code_path), (
                    f"{file_path} 指向的代码文件不存在: {data['代码']}"
                )

    def test_every_function_has_method_yaml(self):
        """每个 Python 函数都必须有对应的方法 YAML 文件"""
        project_root = get_project_root()
        modules = load_all_modules()
        missing = []
        for file_path, data in modules.items():
            if '代码' not in data:
                continue
            code_path = os.path.join(project_root, data['代码'])
            if not os.path.exists(code_path):
                continue
            method_dir = os.path.join(os.path.dirname(file_path), '方法')
            functions = extract_functions_from_file(code_path)
            defined = load_method_files(method_dir)
            for func in functions:
                if func not in defined:
                    missing.append(f"{data.get('名称', '?')}: {func}")
        assert not missing, f"以下函数缺少方法 YAML 文件:\n" + "\n".join(missing)

    def test_method_yaml_references_valid_function(self):
        """方法 YAML 引用的函数必须在对应代码文件中存在"""
        project_root = get_project_root()
        modules = load_all_modules()
        invalid = []
        for file_path, data in modules.items():
            if '代码' not in data:
                continue
            code_path = os.path.join(project_root, data['代码'])
            if not os.path.exists(code_path):
                continue
            method_dir = os.path.join(os.path.dirname(file_path), '方法')
            if not os.path.exists(method_dir):
                continue
            functions = extract_functions_from_file(code_path)
            for method_file in os.listdir(method_dir):
                if method_file.endswith('.yaml'):
                    method_file_path = os.path.join(method_dir, method_file)
                    with open(method_file_path, 'r', encoding='utf-8') as f:
                        method_data = yaml.safe_load(f)
                    if '定义' in method_data and '函数' in method_data['定义']:
                        func_name = method_data['定义']['函数']
                        if func_name not in functions:
                            invalid.append(
                                f"{method_file}: 函数 {func_name} 不存在于 {data['代码']}"
                            )
        assert not invalid, (
            f"以下方法 YAML 引用了不存在的函数:\n" + "\n".join(invalid)
        )

    def test_all_modules_have_name(self):
        """所有模块必须有名称字段"""
        modules = load_all_modules()
        for file_path, data in modules.items():
            assert '名称' in data, f"{file_path} 缺少名称字段"

    def test_all_modules_have_description(self):
        """所有模块必须有说明字段"""
        modules = load_all_modules()
        for file_path, data in modules.items():
            assert '说明' in data, f"{file_path} 缺少说明字段"
