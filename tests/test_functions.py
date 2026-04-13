# 各模块函数单元测试
import os
import tempfile
import shutil
import yaml
import pytest
from src.paths import get_concept_dir, get_background_dir, get_process_dir, get_requirement_dir


class TestConceptModule:
    """测试概念管理模块"""

    def test_check_concept_data_returns_tuple(self):
        """check_concept_data 应返回三元组"""
        from src.concept import check_concept_data
        result = check_concept_data()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_check_concept_data_passes(self):
        """check_concept_data 应该通过"""
        from src.concept import check_concept_data
        valid, success, failure = check_concept_data()
        assert valid, f"概念数据检查失败: {failure}"

    def test_create_concept_prevents_duplicate(self, tmp_path, monkeypatch):
        """create_concept 不应创建重复的概念"""
        from src.concept import create_concept
        monkeypatch.setattr('src.concept.get_concept_dir', lambda: str(tmp_path))
        # 手动创建一个已存在的文件
        existing = tmp_path / "测试.yaml"
        existing.write_text("名称: 测试\n说明: 测试\n", encoding='utf-8')
        result = create_concept("测试", "重复的概念")
        assert result is False

    def test_create_concept_success(self, tmp_path, monkeypatch):
        """create_concept 应该成功创建新概念"""
        from src.concept import create_concept
        monkeypatch.setattr('src.concept.get_concept_dir', lambda: str(tmp_path))
        result = create_concept("新概念", "这是新概念的说明")
        assert result is True
        # 验证文件被创建
        file_path = tmp_path / "新概念.yaml"
        assert file_path.exists()
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        assert data['名称'] == '新概念'
        assert data['说明'] == '这是新概念的说明'


class TestBackgroundModule:
    """测试背景管理模块"""

    def test_check_background_data_returns_tuple(self):
        """check_background_data 应返回三元组"""
        from src.background import check_background_data
        result = check_background_data()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_check_background_data_passes(self):
        """check_background_data 应该通过"""
        from src.background import check_background_data
        valid, success, failure = check_background_data()
        assert valid, f"背景数据检查失败: {failure}"

    def test_create_background_success(self, tmp_path, monkeypatch):
        """create_background 应该成功创建新背景"""
        from src.background import create_background
        monkeypatch.setattr('src.background.get_background_dir', lambda: str(tmp_path))
        result = create_background("测试背景", "这是测试背景说明")
        assert result is True
        file_path = tmp_path / "测试背景.yaml"
        assert file_path.exists()

    def test_create_background_prevents_duplicate(self, tmp_path, monkeypatch):
        """create_background 不应创建重复的背景"""
        from src.background import create_background
        monkeypatch.setattr('src.background.get_background_dir', lambda: str(tmp_path))
        existing = tmp_path / "已存在.yaml"
        existing.write_text("名称: 已存在\n", encoding='utf-8')
        result = create_background("已存在", "重复")
        assert result is False


class TestProcessModule:
    """测试流程管理模块"""

    def test_check_process_data_returns_tuple(self):
        """check_process_data 应返回三元组"""
        from src.process import check_process_data
        result = check_process_data()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_check_process_data_passes(self):
        """check_process_data 应该通过"""
        from src.process import check_process_data
        valid, success, failure = check_process_data()
        assert valid, f"流程数据检查失败: {failure}"

    def test_create_process_success(self, tmp_path, monkeypatch):
        """create_process 应该成功创建新流程"""
        from src.process import create_process
        monkeypatch.setattr('src.process.get_process_dir', lambda: str(tmp_path))
        result = create_process("测试流程X", "背景", "输入", "方法", "结果")
        assert result is True
        file_path = tmp_path / "测试流程X.yaml"
        assert file_path.exists()


class TestRequirementModule:
    """测试需求管理模块"""

    def test_check_requirement_data_returns_tuple(self):
        """check_requirement_data 应返回三元组"""
        from src.requirement import check_requirement_data
        result = check_requirement_data()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_check_requirement_data_passes(self):
        """check_requirement_data 应该通过"""
        from src.requirement import check_requirement_data
        valid, success, failure = check_requirement_data()
        assert valid, f"需求数据检查失败: {failure}"

    def test_check_requirement_story_relation_passes(self):
        """check_requirement_story_relation 应该通过"""
        from src.requirement import check_requirement_story_relation
        valid, success, failure = check_requirement_story_relation()
        assert valid, f"需求用户故事关联检查失败: {failure}"

    def test_create_requirement_success(self, tmp_path, monkeypatch):
        """create_requirement 应该成功创建新需求"""
        from src.requirement import create_requirement
        monkeypatch.setattr('src.requirement.get_requirement_dir', lambda: str(tmp_path))
        result = create_requirement("测试需求X", "测试说明")
        assert result is True
        req_file = tmp_path / "测试需求X" / "需求.yaml"
        assert req_file.exists()


class TestModuleModule:
    """测试模块管理模块"""

    def test_check_module_data_returns_tuple(self):
        """check_module_data 应返回三元组"""
        from src.module import check_module_data
        result = check_module_data()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_check_module_data_passes(self):
        """check_module_data 应该通过"""
        from src.module import check_module_data
        valid, success, failure = check_module_data()
        assert valid, f"模块数据检查失败: {failure}"

    def test_check_module_files_returns_tuple(self):
        """check_module_files 应返回四元组"""
        from src.module import check_module_files
        result = check_module_files()
        assert isinstance(result, tuple)
        assert len(result) == 4

    def test_check_module_files_passes(self):
        """check_module_files 应该通过"""
        from src.module import check_module_files
        valid, _, success, failure = check_module_files()
        assert valid, f"模块文件检查失败: {failure}"


class TestMethodModule:
    """测试方法管理模块"""

    def test_check_method_data_returns_tuple(self):
        """check_method_data 应返回三元组"""
        from src.method import check_method_data
        result = check_method_data()
        assert isinstance(result, tuple)
        assert len(result) == 3


class TestPathsModule:
    """测试路径工具模块"""

    def test_project_root_exists(self):
        """项目根目录应该存在"""
        from src.paths import get_project_root
        assert os.path.isdir(get_project_root())

    def test_project_root_contains_main(self):
        """项目根目录应该包含 main.py"""
        from src.paths import get_project_root
        assert os.path.isfile(os.path.join(get_project_root(), 'main.py'))

    def test_all_dirs_under_project_root(self):
        """所有目录函数返回的路径应该在项目根目录下"""
        from src.paths import (
            get_project_root, get_concept_dir, get_background_dir,
            get_process_dir, get_module_dir, get_requirement_dir,
            get_method_dir,
        )
        root = get_project_root()
        for fn in [get_concept_dir, get_background_dir, get_process_dir,
                   get_module_dir, get_requirement_dir, get_method_dir]:
            path = fn()
            assert path.startswith(root), f"{fn.__name__}() 返回的路径不在项目根目录下"
