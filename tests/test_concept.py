# 概念数据结构验证测试
import os
import yaml
import pytest
from src.paths import get_concept_dir


# 概念 YAML 必须包含的字段
REQUIRED_CONCEPT_FIELDS = ["名称", "说明", "类别", "详情", "关联概念"]


def load_all_concepts():
    """加载所有概念 YAML 文件"""
    concept_dir = get_concept_dir()
    concepts = {}
    for root, _, files in os.walk(concept_dir):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                rel_path = os.path.relpath(file_path, concept_dir)
                concepts[rel_path] = data
    return concepts


def get_all_concept_names():
    """获取所有概念名称"""
    concepts = load_all_concepts()
    return {data["名称"] for data in concepts.values() if "名称" in data}


class TestConceptStructure:
    """测试概念数据结构的规范性"""

    def test_concept_dir_exists(self):
        """概念目录应该存在"""
        assert os.path.isdir(get_concept_dir())

    def test_at_least_one_concept(self):
        """至少应该有一个概念文件"""
        concepts = load_all_concepts()
        assert len(concepts) > 0

    @pytest.fixture
    def all_concepts(self):
        return load_all_concepts()

    def test_all_concepts_have_required_fields(self, all_concepts):
        """所有概念必须包含规范的字段: 名称, 说明, 类别, 详情, 关联概念"""
        for file, data in all_concepts.items():
            for field in REQUIRED_CONCEPT_FIELDS:
                assert field in data, f"{file} 缺少必要字段: {field}"

    def test_name_matches_filename(self, all_concepts):
        """概念的名称字段应该与文件名一致"""
        for file, data in all_concepts.items():
            expected_name = os.path.basename(file).replace(".yaml", "")
            assert data["名称"] == expected_name, (
                f"{file} 的名称字段 '{data['名称']}' 与文件名 '{expected_name}' 不一致"
            )

    def test_category_is_list(self, all_concepts):
        """类别字段应该是列表"""
        for file, data in all_concepts.items():
            if "类别" in data:
                assert isinstance(data["类别"], list), f"{file} 的类别字段应该是列表"

    def test_related_concepts_is_list(self, all_concepts):
        """关联概念字段应该是列表"""
        for file, data in all_concepts.items():
            if "关联概念" in data:
                assert isinstance(data["关联概念"], list), (
                    f"{file} 的关联概念字段应该是列表"
                )

    def test_related_concepts_reference_existing(self, all_concepts):
        """关联概念中的每个引用必须指向已存在的概念"""
        all_names = get_all_concept_names()
        for file, data in all_concepts.items():
            related = data.get("关联概念", [])
            for concept_name in related:
                assert concept_name in all_names, (
                    f"{file} 的关联概念 '{concept_name}' 不存在于概念目录中"
                )

    def test_description_not_empty(self, all_concepts):
        """说明字段不应为空"""
        for file, data in all_concepts.items():
            assert data.get("说明"), f"{file} 的说明字段不能为空"


class TestConceptCategories:
    """测试概念类别的有效性"""

    @pytest.fixture
    def all_concepts(self):
        return load_all_concepts()

    def test_valid_categories(self, all_concepts):
        """类别应该是已知的分类"""
        valid_categories = {
            "产品侧",
            "开发侧",
            "通用",
            "元概念",
            "流程侧",
            "状态",
            "基础类型",
        }
        for file, data in all_concepts.items():
            for cat in data.get("类别", []):
                assert cat in valid_categories, (
                    f"{file} 含有未知类别 '{cat}'，有效类别: {valid_categories}"
                )
