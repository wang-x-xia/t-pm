# 需求-用户故事关联测试
import os
import yaml
import pytest
from src.paths import get_requirement_dir


def load_all_requirements():
    """加载所有需求数据"""
    requirement_dir = get_requirement_dir()
    requirements = {}
    for req_name in os.listdir(requirement_dir):
        req_dir = os.path.join(requirement_dir, req_name)
        if os.path.isdir(req_dir):
            req_file = os.path.join(req_dir, "需求.yaml")
            if os.path.exists(req_file):
                with open(req_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                requirements[req_name] = {
                    'data': data,
                    'dir': req_dir,
                }
    return requirements


def get_actual_stories(req_dir):
    """获取需求目录下实际存在的用户故事文件"""
    story_dir = os.path.join(req_dir, "用户故事")
    stories = []
    if os.path.exists(story_dir):
        for file in os.listdir(story_dir):
            if file.endswith('.yaml'):
                stories.append(file.replace('.yaml', ''))
    return stories


class TestRequirementStoryRelation:
    """测试需求与用户故事的关联关系"""

    def test_requirement_dir_exists(self):
        """需求目录应该存在"""
        assert os.path.isdir(get_requirement_dir())

    def test_all_requirements_have_name(self):
        """所有需求必须有名称字段"""
        requirements = load_all_requirements()
        for req_name, info in requirements.items():
            assert '名称' in info['data'], f"需求 {req_name} 缺少名称字段"

    def test_all_requirements_have_story_list(self):
        """所有需求必须有用户故事列表"""
        requirements = load_all_requirements()
        for req_name, info in requirements.items():
            assert '用户故事' in info['data'], (
                f"需求 {req_name} 缺少用户故事字段"
            )

    def test_referenced_stories_have_files(self):
        """需求中引用的用户故事必须有对应的文件"""
        requirements = load_all_requirements()
        missing = []
        for req_name, info in requirements.items():
            stories = info['data'].get('用户故事', [])
            actual = get_actual_stories(info['dir'])
            for story in stories:
                if story not in actual:
                    missing.append(f"需求 {req_name}: 引用了不存在的用户故事 '{story}'")
        assert not missing, "\n".join(missing)

    def test_story_files_are_referenced(self):
        """所有用户故事文件必须被需求引用"""
        requirements = load_all_requirements()
        orphans = []
        for req_name, info in requirements.items():
            stories = info['data'].get('用户故事', [])
            actual = get_actual_stories(info['dir'])
            for story in actual:
                if story not in stories:
                    orphans.append(
                        f"需求 {req_name}: 用户故事文件 '{story}' 未被需求引用"
                    )
        assert not orphans, "\n".join(orphans)

    def test_story_files_have_required_fields(self):
        """所有用户故事文件必须有必要字段"""
        requirement_dir = get_requirement_dir()
        missing_fields = []
        for req_name in os.listdir(requirement_dir):
            story_dir = os.path.join(requirement_dir, req_name, "用户故事")
            if not os.path.isdir(story_dir):
                continue
            for file in os.listdir(story_dir):
                if file.endswith('.yaml'):
                    file_path = os.path.join(story_dir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    if '名称' not in data:
                        missing_fields.append(f"{file_path}: 缺少名称字段")
                    if '说明' not in data:
                        missing_fields.append(f"{file_path}: 缺少说明字段")
        assert not missing_fields, "\n".join(missing_fields)

    def test_story_name_matches_filename(self):
        """用户故事的名称字段应该与文件名一致"""
        requirement_dir = get_requirement_dir()
        mismatches = []
        for req_name in os.listdir(requirement_dir):
            story_dir = os.path.join(requirement_dir, req_name, "用户故事")
            if not os.path.isdir(story_dir):
                continue
            for file in os.listdir(story_dir):
                if file.endswith('.yaml'):
                    file_path = os.path.join(story_dir, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    expected = file.replace('.yaml', '')
                    if data.get('名称') != expected:
                        mismatches.append(
                            f"{file_path}: 名称 '{data.get('名称')}' != 文件名 '{expected}'"
                        )
        assert not mismatches, "\n".join(mismatches)
