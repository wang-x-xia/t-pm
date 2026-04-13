# 概念管理模块
import os
import logging
import yaml
from src.paths import get_concept_dir

logger = logging.getLogger(__name__)

def check_concept_data():
    """检查概念管理数据的合理性"""
    concept_dir = get_concept_dir()
    valid = True
    success = []
    failure = []
    
    # 先收集所有概念名称，用于验证关联概念引用
    all_concept_names = set()
    for file in os.listdir(concept_dir):
        if file.endswith('.yaml'):
            all_concept_names.add(file.replace('.yaml', ''))
    
    required_fields = ['名称', '说明', '类别', '详情', '关联概念']
    valid_categories = {'产品侧', '开发侧', '通用'}
    
    # 检查概念目录下的所有yaml文件
    for file in os.listdir(concept_dir):
        if file.endswith('.yaml'):
            file_path = os.path.join(concept_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                file_valid = True
                
                # 检查所有必要字段
                for field in required_fields:
                    if field not in data:
                        failure.append(f"{file_path} - 缺少必要字段: {field}")
                        failure.append(f"  修复建议: 添加 '{field}' 字段")
                        valid = False
                        file_valid = False
                
                # 检查名称与文件名一致
                expected_name = file.replace('.yaml', '')
                if data.get('名称') != expected_name:
                    failure.append(f"{file_path} - 名称 '{data.get('名称')}' 与文件名 '{expected_name}' 不一致")
                    valid = False
                    file_valid = False
                
                # 检查类别是列表且值有效
                if '类别' in data:
                    if not isinstance(data['类别'], list):
                        failure.append(f"{file_path} - 类别字段应该是列表")
                        valid = False
                        file_valid = False
                    else:
                        for cat in data['类别']:
                            if cat not in valid_categories:
                                failure.append(f"{file_path} - 未知类别: {cat}，有效类别: {valid_categories}")
                                valid = False
                                file_valid = False
                
                # 检查关联概念是列表且引用存在
                if '关联概念' in data:
                    if not isinstance(data['关联概念'], list):
                        failure.append(f"{file_path} - 关联概念字段应该是列表")
                        valid = False
                        file_valid = False
                    else:
                        for ref in data['关联概念']:
                            if ref not in all_concept_names:
                                failure.append(f"{file_path} - 关联概念 '{ref}' 不存在于概念目录中")
                                valid = False
                                file_valid = False
                
                if file_valid:
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

def create_concept(name, description):
    """创建新的概念"""
    concept_dir = get_concept_dir()
    file_path = os.path.join(concept_dir, f"{name}.yaml")
    
    # 检查文件是否已存在
    if os.path.exists(file_path):
        logger.warning(f"概念文件已存在: {file_path}")
        return False
    
    # 构建概念数据
    concept_data = {
        '名称': name,
        '说明': description,
    }
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(concept_data, f, allow_unicode=True, default_flow_style=False)
        logger.info(f"概念创建成功: {file_path}")
        return True
    except Exception as e:
        logger.error(f"概念创建失败: {e}")
        return False
