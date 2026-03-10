# 概念管理模块
import os
import yaml

def check_concept_data():
    """检查概念管理数据的合理性"""
    concept_dir = "c:/Users/fly_d/IdeaProjects/t-pm/概念"
    valid = True
    success = []
    failure = []
    
    # 检查概念目录下的所有yaml文件
    for file in os.listdir(concept_dir):
        if file.endswith('.yaml'):
            file_path = os.path.join(concept_dir, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                # 检查必要字段
                if '名称' not in data:
                    failure.append(f"{file_path} - 缺少必要字段: 名称")
                    failure.append("  修复建议: 添加 '名称' 字段，例如: 名称: 概念名称")
                    valid = False
                
                # 检查概念文件的特定字段
                if file == "概念.yaml" and isinstance(data.get("概念"), list):
                    for i, concept in enumerate(data["概念"], 1):
                        if '名称' not in concept:
                            failure.append(f"{file_path} - 概念 {i} 缺少必要字段: 名称")
                            failure.append("  修复建议: 为每个概念添加 '名称' 字段")
                            valid = False
                        if '说明' not in concept:
                            failure.append(f"{file_path} - 概念 {i} 缺少字段: 说明")
                            failure.append("  修复建议: 为每个概念添加 '说明' 字段，描述概念的含义")
                
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

