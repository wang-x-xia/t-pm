# 自举完整性测试
import os
import yaml
import pytest
from src.paths import (
    get_project_root,
    get_concept_dir,
    get_background_dir,
    get_process_dir,
    get_module_dir,
    get_requirement_dir,
)


class TestBootstrap:
    """测试项目的自举完整性——项目能够用自身的数据结构完整描述自己"""

    def test_all_directories_exist(self):
        """所有核心数据目录必须存在"""
        for dir_fn in [
            get_concept_dir,
            get_background_dir,
            get_process_dir,
            get_module_dir,
            get_requirement_dir,
        ]:
            d = dir_fn()
            assert os.path.isdir(d), f"目录不存在: {d}"

    def test_all_source_files_have_module(self):
        """每个 Python 源文件都必须有对应的模块 YAML"""
        project_root = get_project_root()
        module_dir = get_module_dir()

        # 收集所有模块 YAML 中声明的代码文件
        declared_code_files = set()
        for root, _, files in os.walk(module_dir):
            for file in files:
                if file == "模块.yaml":
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if "代码" in data:
                        declared_code_files.add(os.path.normpath(data["代码"]))

        # 收集所有实际 Python 文件 (排除 tests 和 __pycache__)
        actual_py_files = set()
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [
                d for d in dirs if d not in {".venv", "__pycache__", "tests", ".git"}
            ]
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    rel_path = os.path.normpath(
                        os.path.relpath(os.path.join(root, file), project_root)
                    )
                    actual_py_files.add(rel_path)

        undeclared = actual_py_files - declared_code_files
        assert not undeclared, f"以下 Python 文件没有对应的模块 YAML:\n" + "\n".join(
            sorted(undeclared)
        )

    def test_check_all_data_passes(self):
        """内置的 check_all_data 必须全部通过"""
        from main import check_all_data
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            result = check_all_data(False)
        finally:
            sys.stdout = old_stdout

        assert result, "check_all_data 未通过"

    def test_core_concepts_exist(self):
        """核心概念必须全部定义"""
        expected_concepts = {
            "概念",
            "需求",
            "用户故事",
            "流程",
            "背景",
            "方法",
            "模块",
            "外部模块",
        }
        concept_dir = get_concept_dir()
        actual = set()
        for root, _, files in os.walk(concept_dir):
            for file in files:
                if file.endswith(".yaml"):
                    actual.add(file.replace(".yaml", ""))

        missing = expected_concepts - actual
        assert not missing, f"缺少核心概念定义: {missing}"

    def test_at_least_one_background(self):
        """至少应该有一个背景实例"""
        bg_dir = get_background_dir()
        bg_files = [f for f in os.listdir(bg_dir) if f.endswith(".yaml")]
        assert len(bg_files) > 0, "背景目录中没有背景实例"

    def test_at_least_one_process(self):
        """至少应该有一个流程"""
        process_dir = get_process_dir()
        process_files = [f for f in os.listdir(process_dir) if f.endswith(".yaml")]
        assert len(process_files) > 0, "流程目录中没有流程"

    def test_at_least_one_requirement(self):
        """至少应该有一个需求"""
        req_dir = get_requirement_dir()
        req_dirs = [
            d for d in os.listdir(req_dir) if os.path.isdir(os.path.join(req_dir, d))
        ]
        assert len(req_dirs) > 0, "需求目录中没有需求"

    def test_no_hardcoded_paths_in_source(self):
        """源代码中不应存在硬编码的绝对路径"""
        project_root = get_project_root()
        src_dir = os.path.join(project_root, "src")
        violations = []
        for file in os.listdir(src_dir):
            if file.endswith(".py"):
                file_path = os.path.join(src_dir, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                if "c:/Users/" in content or "C:\\Users\\" in content:
                    violations.append(file)
        assert not violations, f"以下源文件包含硬编码路径: {violations}"

    def test_all_processes_have_required_fields(self):
        """所有流程 YAML 必须包含必要字段"""
        process_dir = get_process_dir()
        required_fields = {"名称", "背景", "输入", "方法", "结果"}
        for file in os.listdir(process_dir):
            if file.endswith(".yaml"):
                fpath = os.path.join(process_dir, file)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                missing = required_fields - set(data.keys())
                assert not missing, f"{file} 缺少字段: {missing}"

    def test_all_processes_method_is_list(self):
        """所有流程的方法字段必须是列表"""
        process_dir = get_process_dir()
        for file in os.listdir(process_dir):
            if file.endswith(".yaml"):
                fpath = os.path.join(process_dir, file)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if "方法" in data:
                    assert isinstance(data["方法"], list), f"{file} 的方法字段不是列表"

    def test_all_processes_name_matches_filename(self):
        """所有流程名称必须与文件名一致"""
        process_dir = get_process_dir()
        for file in os.listdir(process_dir):
            if file.endswith(".yaml"):
                fpath = os.path.join(process_dir, file)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                expected = file.replace(".yaml", "")
                assert data.get("名称") == expected, (
                    f"{file} 名称 '{data.get('名称')}' 与文件名不一致"
                )

    def test_all_method_yamls_have_flow(self):
        """所有方法 YAML 文件必须包含流程字段"""
        module_dir = get_module_dir()
        missing = []
        for module_name in os.listdir(module_dir):
            method_dir = os.path.join(module_dir, module_name, "方法")
            if not os.path.isdir(method_dir):
                continue
            for fname in os.listdir(method_dir):
                if fname.endswith(".yaml"):
                    fpath = os.path.join(method_dir, fname)
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if "流程" not in data:
                        missing.append(f"{module_name}/{fname}")
        assert not missing, f"以下方法YAML缺少流程字段: {missing}"

    def test_all_backgrounds_have_required_fields(self):
        """所有背景 YAML 必须包含名称和说明"""
        bg_dir = get_background_dir()
        for file in os.listdir(bg_dir):
            if file.endswith(".yaml"):
                fpath = os.path.join(bg_dir, file)
                with open(fpath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                assert "名称" in data, f"{file} 缺少名称字段"
                assert "说明" in data, f"{file} 缺少说明字段"

    def test_module_dependencies_all_valid(self):
        """所有模块依赖必须引用已存在的模块"""
        from src.module import check_module_dependencies

        valid, success, failure = check_module_dependencies()
        assert valid, f"模块依赖检查失败: {failure}"

    def test_user_stories_have_list_flow(self):
        """所有用户故事的流程字段必须是列表格式"""
        req_dir = get_requirement_dir()
        bad = []
        for req_name in os.listdir(req_dir):
            story_dir = os.path.join(req_dir, req_name, "用户故事")
            if not os.path.isdir(story_dir):
                continue
            for fname in os.listdir(story_dir):
                if fname.endswith(".yaml"):
                    fpath = os.path.join(story_dir, fname)
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if "流程" in data and not isinstance(data["流程"], list):
                        bad.append(f"{req_name}/{fname}")
        assert not bad, f"以下用户故事流程字段不是列表: {bad}"
