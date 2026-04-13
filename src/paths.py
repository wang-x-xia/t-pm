# 路径工具模块
import os


def get_project_root():
    """获取项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_concept_dir():
    """获取概念目录"""
    return os.path.join(get_project_root(), "概念")


def get_background_dir():
    """获取背景目录"""
    return os.path.join(get_project_root(), "背景")


def get_process_dir():
    """获取流程目录"""
    return os.path.join(get_project_root(), "流程")


def get_module_dir():
    """获取模块目录"""
    return os.path.join(get_project_root(), "模块")


def get_requirement_dir():
    """获取需求目录"""
    return os.path.join(get_project_root(), "需求")


def get_method_dir():
    """获取方法管理的方法目录"""
    return os.path.join(get_module_dir(), "方法管理", "方法")


def get_concept_meta_dir():
    """获取元概念目录"""
    return os.path.join(get_concept_dir(), "元概念")


def get_concept_product_dir():
    """获取产品侧概念目录"""
    return os.path.join(get_concept_dir(), "产品侧")


def get_concept_process_dir():
    """获取流程侧概念目录"""
    return os.path.join(get_concept_dir(), "流程侧")


def get_concept_development_dir():
    """获取开发侧概念目录"""
    return os.path.join(get_concept_dir(), "开发侧")


def get_concept_status_dir():
    """获取状态概念目录"""
    return os.path.join(get_concept_dir(), "状态")


def get_concept_basetype_dir():
    """获取基础类型概念目录"""
    return os.path.join(get_concept_dir(), "基础类型")
