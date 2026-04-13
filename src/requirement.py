# 需求和用户故事管理模块
import os
import logging
import yaml
from src.paths import get_requirement_dir

logger = logging.getLogger(__name__)

def check_requirement_data():
    """检查需求与用户故事管理数据的合理性"""
    requirement_dir = get_requirement_dir()
    valid = True
    success = []
    failure = []
    
    # 检查需求目录下的所有yaml文件
    for root, _, files in os.walk(requirement_dir):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    
                    # 检查必要字段
                    if '名称' not in data:
                        failure.append(f"{file_path} - 缺少必要字段: 名称")
                        failure.append("  修复建议: 添加 '名称' 字段，例如: 名称: 需求名称")
                        valid = False
                    
                    # 检查用户故事文件的特定字段
                    if '用户故事' in root and file.endswith('.yaml'):
                        if '说明' not in data:
                            failure.append(f"{file_path} - 缺少字段: 说明")
                            failure.append("  修复建议: 添加 '说明' 字段，描述用户故事的内容")
                        if '流程' not in data:
                            failure.append(f"{file_path} - 缺少字段: 流程")
                            failure.append("  修复建议: 添加 '流程' 字段，描述用户故事的实现流程")
                    
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

def create_requirement(name, description):
    """创建新的需求"""
    requirement_dir = get_requirement_dir()
    # 创建需求目录
    req_dir = os.path.join(requirement_dir, name)
    if not os.path.exists(req_dir):
        os.makedirs(req_dir)
    
    # 创建需求文件
    file_path = os.path.join(req_dir, "需求.yaml")
    
    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"✗ 需求文件已存在: {file_path}")
        return False
    
    # 构建需求数据
    requirement_data = {
        '名称': name,
        '说明': description,
        '用户故事': []
    }
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(requirement_data, f, allow_unicode=True, default_flow_style=False)
        print(f"✓ 需求创建成功: {file_path}")
        return True
    except Exception as e:
        print(f"✗ 需求创建失败: {e}")
        return False

def create_user_story(requirement_name, story_name, description, process):
    """为需求创建新的用户故事"""
    requirement_dir = get_requirement_dir()
    req_dir = os.path.join(requirement_dir, requirement_name)
    
    # 检查需求是否存在
    if not os.path.exists(req_dir):
        print(f"✗ 需求不存在: {requirement_name}")
        return False
    
    # 创建用户故事目录
    story_dir = os.path.join(req_dir, "用户故事")
    if not os.path.exists(story_dir):
        os.makedirs(story_dir)
    
    # 创建用户故事文件
    file_path = os.path.join(story_dir, f"{story_name}.yaml")
    
    # 检查文件是否已存在
    if os.path.exists(file_path):
        print(f"✗ 用户故事文件已存在: {file_path}")
        return False
    
    # 构建用户故事数据
    story_data = {
        '名称': story_name,
        '说明': description,
        '流程': process
    }
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(story_data, f, allow_unicode=True, default_flow_style=False)
        
        # 更新需求文件中的用户故事列表
        req_file = os.path.join(req_dir, "需求.yaml")
        if os.path.exists(req_file):
            with open(req_file, 'r', encoding='utf-8') as f:
                req_data = yaml.safe_load(f)
            
            if '用户故事' not in req_data:
                req_data['用户故事'] = []
            
            if story_name not in req_data['用户故事']:
                req_data['用户故事'].append(story_name)
                
                with open(req_file, 'w', encoding='utf-8') as f:
                    yaml.dump(req_data, f, allow_unicode=True, default_flow_style=False)
                print(f"✓ 更新需求文件中的用户故事列表")
        
        print(f"✓ 用户故事创建成功: {file_path}")
        return True
    except Exception as e:
        print(f"✗ 用户故事创建失败: {e}")
        return False

def list_requirements_with_stories():
    """列出所有需求及其关联的用户故事"""
    requirement_dir = get_requirement_dir()
    requirements = []
    
    if not os.path.exists(requirement_dir):
        print(f"✗ 需求目录不存在: {requirement_dir}")
        return []
    
    # 遍历需求目录
    for req_name in os.listdir(requirement_dir):
        req_dir = os.path.join(requirement_dir, req_name)
        if os.path.isdir(req_dir):
            req_file = os.path.join(req_dir, "需求.yaml")
            if os.path.exists(req_file):
                try:
                    with open(req_file, 'r', encoding='utf-8') as f:
                        req_data = yaml.safe_load(f)
                    
                    # 获取用户故事
                    stories = req_data.get('用户故事', [])
                    
                    # 检查用户故事目录
                    story_dir = os.path.join(req_dir, "用户故事")
                    actual_stories = []
                    if os.path.exists(story_dir):
                        for file in os.listdir(story_dir):
                            if file.endswith('.yaml'):
                                actual_stories.append(file.replace('.yaml', ''))
                    
                    requirements.append({
                        '名称': req_data.get('名称', req_name),
                        '说明': req_data.get('说明', '无'),
                        '用户故事': stories,
                        '实际用户故事': actual_stories
                    })
                except Exception as e:
                    print(f"✗ 读取需求文件失败: {req_file} - {e}")
    
    if requirements:
        print("\n所有需求及其用户故事:")
        for i, req in enumerate(requirements, 1):
            print(f"\n{i}. 需求: {req['名称']}")
            print(f"   说明: {req['说明']}")
            print("   用户故事:")
            if req['用户故事']:
                for story in req['用户故事']:
                    print(f"     - {story}")
            else:
                print("     无")
            
            # 检查实际用户故事与需求文件中的用户故事是否一致
            if set(req['用户故事']) != set(req['实际用户故事']):
                print("   警告: 用户故事列表与实际文件不一致")
                print(f"   需求文件中的用户故事: {req['用户故事']}")
                print(f"   实际用户故事文件: {req['实际用户故事']}")
    else:
        print("\n没有找到需求")
    
    return requirements

def list_user_stories():
    """列出所有用户故事及其关联的需求"""
    requirement_dir = get_requirement_dir()
    user_stories = []
    
    if not os.path.exists(requirement_dir):
        print(f"✗ 需求目录不存在: {requirement_dir}")
        return []
    
    # 遍历需求目录
    for req_name in os.listdir(requirement_dir):
        req_dir = os.path.join(requirement_dir, req_name)
        if os.path.isdir(req_dir):
            story_dir = os.path.join(req_dir, "用户故事")
            if os.path.exists(story_dir):
                for file in os.listdir(story_dir):
                    if file.endswith('.yaml'):
                        story_file = os.path.join(story_dir, file)
                        try:
                            with open(story_file, 'r', encoding='utf-8') as f:
                                story_data = yaml.safe_load(f)
                            
                            user_stories.append({
                                '名称': story_data.get('名称', file.replace('.yaml', '')),
                                '说明': story_data.get('说明', '无'),
                                '所属需求': req_name
                            })
                        except Exception as e:
                            print(f"✗ 读取用户故事文件失败: {story_file} - {e}")
    
    if user_stories:
        print("\n所有用户故事及其所属需求:")
        for i, story in enumerate(user_stories, 1):
            print(f"\n{i}. 用户故事: {story['名称']}")
            print(f"   说明: {story['说明']}")
            print(f"   所属需求: {story['所属需求']}")
    else:
        print("\n没有找到用户故事")
    
    return user_stories

def check_requirement_story_relation():
    """检查需求和用户故事的关联关系"""
    requirement_dir = get_requirement_dir()
    valid = True
    success = []
    failure = []
    
    if not os.path.exists(requirement_dir):
        failure.append(f"需求目录不存在: {requirement_dir}")
        return False, success, failure
    
    # 遍历需求目录
    for req_name in os.listdir(requirement_dir):
        req_dir = os.path.join(requirement_dir, req_name)
        if os.path.isdir(req_dir):
            req_file = os.path.join(req_dir, "需求.yaml")
            if os.path.exists(req_file):
                try:
                    with open(req_file, 'r', encoding='utf-8') as f:
                        req_data = yaml.safe_load(f)
                    
                    # 检查用户故事列表
                    stories = req_data.get('用户故事', [])
                    
                    # 检查用户故事目录
                    story_dir = os.path.join(req_dir, "用户故事")
                    if os.path.exists(story_dir):
                        actual_stories = []
                        for file in os.listdir(story_dir):
                            if file.endswith('.yaml'):
                                actual_stories.append(file.replace('.yaml', ''))
                        
                        # 检查是否有用户故事在需求文件中但实际文件不存在
                        for story in stories:
                            if story not in actual_stories:
                                failure.append(f"需求 {req_name} 引用了不存在的用户故事: {story}")
                                failure.append(f"  修复建议: 创建用户故事文件或从需求文件中移除该用户故事")
                                valid = False
                        
                        # 检查是否有用户故事文件存在但未在需求文件中引用
                        for story in actual_stories:
                            if story not in stories:
                                failure.append(f"用户故事 {story} 存在但未被需求 {req_name} 引用")
                                failure.append(f"  修复建议: 在需求文件的用户故事列表中添加该用户故事")
                                valid = False
                        
                        if len(stories) == len(actual_stories) and set(stories) == set(actual_stories):
                            success.append(f"需求 {req_name} 的用户故事关联关系检查通过")
                    else:
                        if stories:
                            failure.append(f"需求 {req_name} 引用了用户故事，但用户故事目录不存在")
                            failure.append(f"  修复建议: 创建用户故事目录并添加相应的用户故事文件")
                            valid = False
                        else:
                            success.append(f"需求 {req_name} 无用户故事，跳过关联关系检查")
                except Exception as e:
                    failure.append(f"检查需求 {req_name} 时出错: {e}")
                    valid = False
    
    return valid, success, failure

