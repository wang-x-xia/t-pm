import os
import yaml
import argparse
from src.concept import check_concept_data
from src.module import check_module_data, check_module_files, visualize_module_dependencies, check_module_dependencies, analyze_module_dependencies
from src.requirement import check_requirement_data, create_requirement, create_user_story, list_requirements_with_stories, list_user_stories, check_requirement_story_relation
from src.method import list_pending_methods, create_method, edit_method, apply_method, list_methods, check_method_data
from src.process import check_process_data, create_process, edit_process, visualize_process, list_processes
from src.background import check_background_data, create_background, edit_background, display_background, list_backgrounds

def check_all_data():
    """检查项目内所有数据的合理性"""
    # 收集所有检查结果和明细信息
    check_results = {
        "概念管理数据": {
            "状态": "",
            "成功": [],
            "失败": []
        },
        "背景管理数据": {
            "状态": "",
            "成功": [],
            "失败": []
        },
        "方法管理数据": {
            "状态": "",
            "成功": [],
            "失败": []
        },
        "模块与外部模块管理数据": {
            "状态": "",
            "成功": [],
            "失败": []
        },
        "需求与用户故事管理数据": {
            "状态": "",
            "成功": [],
            "失败": []
        },
        "流程管理数据": {
            "状态": "",
            "成功": [],
            "失败": []
        },
        "模块文件": {
            "状态": "",
            "成功": [],
            "失败": []
        },
        "模块依赖关系": {
            "状态": "",
            "成功": [],
            "失败": []
        },
        "需求和用户故事关联关系": {
            "状态": "",
            "成功": [],
            "失败": []
        }
    }
    
    # 检查概念管理数据
    concept_result, concept_success, concept_failure = check_concept_data()
    check_results["概念管理数据"]["状态"] = "通过" if concept_result else "失败"
    check_results["概念管理数据"]["成功"] = concept_success
    check_results["概念管理数据"]["失败"] = concept_failure
    
    # 检查背景管理数据
    background_result, background_success, background_failure = check_background_data()
    check_results["背景管理数据"]["状态"] = "通过" if background_result else "失败"
    check_results["背景管理数据"]["成功"] = background_success
    check_results["背景管理数据"]["失败"] = background_failure
    
    # 检查方法管理数据
    method_result, method_success, method_failure = check_method_data()
    check_results["方法管理数据"]["状态"] = "通过" if method_result else "失败"
    check_results["方法管理数据"]["成功"] = method_success
    check_results["方法管理数据"]["失败"] = method_failure
    
    # 检查模块与外部模块管理数据
    module_result, module_success, module_failure = check_module_data()
    check_results["模块与外部模块管理数据"]["状态"] = "通过" if module_result else "失败"
    check_results["模块与外部模块管理数据"]["成功"] = module_success
    check_results["模块与外部模块管理数据"]["失败"] = module_failure
    
    # 检查需求与用户故事管理数据
    requirement_result, requirement_success, requirement_failure = check_requirement_data()
    check_results["需求与用户故事管理数据"]["状态"] = "通过" if requirement_result else "失败"
    check_results["需求与用户故事管理数据"]["成功"] = requirement_success
    check_results["需求与用户故事管理数据"]["失败"] = requirement_failure
    
    # 检查流程管理数据
    process_result, process_success, process_failure = check_process_data()
    check_results["流程管理数据"]["状态"] = "通过" if process_result else "失败"
    check_results["流程管理数据"]["成功"] = process_success
    check_results["流程管理数据"]["失败"] = process_failure
    
    # 检查模块文件
    module_files_result, _, module_files_success, module_files_failure = check_module_files()
    check_results["模块文件"]["状态"] = "通过" if module_files_result else "失败"
    check_results["模块文件"]["成功"] = module_files_success
    check_results["模块文件"]["失败"] = module_files_failure
    
    # 检查模块依赖关系
    module_deps_result, module_deps_success, module_deps_failure = check_module_dependencies()
    check_results["模块依赖关系"]["状态"] = "通过" if module_deps_result else "失败"
    check_results["模块依赖关系"]["成功"] = module_deps_success
    check_results["模块依赖关系"]["失败"] = module_deps_failure
    
    # 检查需求和用户故事关联关系
    req_story_result, req_story_success, req_story_failure = check_requirement_story_relation()
    check_results["需求和用户故事关联关系"]["状态"] = "通过" if req_story_result else "失败"
    check_results["需求和用户故事关联关系"]["成功"] = req_story_success
    check_results["需求和用户故事关联关系"]["失败"] = req_story_failure
    
    # 生成最终的YAML结果
    final_result = {
        "检查结果": check_results,
        "整体状态": "通过" if all([concept_result, background_result, method_result, module_result, requirement_result, process_result, module_files_result, module_deps_result, req_story_result]) else "失败"
    }
    
    # 输出YAML格式结果
    print(yaml.dump(final_result, allow_unicode=True, sort_keys=False))
    
    return all([concept_result, background_result, method_result, module_result, requirement_result, process_result, module_files_result, module_deps_result, req_story_result])

def check_yaml_files(directory):
    """检查指定目录下所有yaml文件的格式"""
    valid = True
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        yaml.safe_load(f)
                    print(f"✓ {file_path} - 格式正确")
                except yaml.YAMLError as e:
                    print(f"✗ {file_path} - 格式错误: {e}")
                    valid = False
    return valid

def display_pending_methods():
    """显示所有待处理方法及其关联的流程"""
    print("\n罗列所有待处理方法及其流程:")
    pending_methods = list_pending_methods()
    
    if not pending_methods:
        print("没有找到待处理方法")
        return
    
    for i, method in enumerate(pending_methods, 1):
        print(f"\n{ i }. 待处理方法: { method['名称'] }")
        print(f"   说明: { method['说明'] }")
        print("   流程:")
        for j, step in enumerate(method['流程'], 1):
            print(f"     { j }. { step }")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='t-pm 产品管理系统')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 检查命令
    check_parser = subparsers.add_parser('check', help='检查相关功能')
    check_subparsers = check_parser.add_subparsers(dest='check_command', help='检查命令')
    
    # 检查所有数据
    check_subparsers.add_parser('all', help='检查所有数据的合理性')
    
    # 检查yaml文件格式
    yaml_parser = check_subparsers.add_parser('yaml', help='检查yaml文件格式')
    yaml_parser.add_argument('directory', default='.', help='要检查的目录')
    
    # 显示命令
    show_parser = subparsers.add_parser('show', help='显示相关信息')
    show_subparsers = show_parser.add_subparsers(dest='show_command', help='显示命令')
    
    # 显示待处理方法
    show_subparsers.add_parser('pending', help='显示所有待处理方法')
    
    # 显示流程
    show_subparsers.add_parser('processes', help='显示所有流程')
    
    # 显示背景
    show_subparsers.add_parser('backgrounds', help='显示所有背景')
    
    # 显示方法
    show_subparsers.add_parser('methods', help='显示所有方法')
    
    # 显示需求和用户故事
    show_subparsers.add_parser('requirements', help='显示所有需求及其用户故事')
    show_subparsers.add_parser('stories', help='显示所有用户故事及其所属需求')
    
    # 显示模块依赖关系
    show_subparsers.add_parser('dependencies', help='显示模块依赖关系')
    
    # 创建命令
    create_parser = subparsers.add_parser('create', help='创建相关资源')
    create_subparsers = create_parser.add_subparsers(dest='create_command', help='创建命令')
    
    # 创建流程
    process_parser = create_subparsers.add_parser('process', help='创建新流程')
    process_parser.add_argument('name', help='流程名称')
    process_parser.add_argument('background', help='背景')
    process_parser.add_argument('inputs', help='输入')
    process_parser.add_argument('method', help='方法')
    process_parser.add_argument('result', help='结果')
    
    # 创建背景
    background_parser = create_subparsers.add_parser('background', help='创建新背景')
    background_parser.add_argument('name', help='背景名称')
    background_parser.add_argument('description', help='背景说明')
    
    # 创建方法
    method_parser = create_subparsers.add_parser('method', help='创建新方法')
    method_parser.add_argument('name', help='方法名称')
    method_parser.add_argument('description', help='方法说明')
    method_parser.add_argument('process', nargs='+', help='流程步骤')
    
    # 创建需求
    requirement_parser = create_subparsers.add_parser('requirement', help='创建新需求')
    requirement_parser.add_argument('name', help='需求名称')
    requirement_parser.add_argument('description', help='需求说明')
    
    # 创建用户故事
    story_parser = create_subparsers.add_parser('story', help='创建新用户故事')
    story_parser.add_argument('requirement', help='所属需求名称')
    story_parser.add_argument('name', help='用户故事名称')
    story_parser.add_argument('description', help='用户故事说明')
    story_parser.add_argument('process', nargs='+', help='流程步骤')
    
    # 应用命令
    apply_parser = subparsers.add_parser('apply', help='应用相关功能')
    apply_subparsers = apply_parser.add_subparsers(dest='apply_command', help='应用命令')
    
    # 应用方法
    apply_method_parser = apply_subparsers.add_parser('method', help='应用方法到特定上下文')
    apply_method_parser.add_argument('name', help='方法名称')
    apply_method_parser.add_argument('context', help='应用上下文')
    
    # 可视化命令
    visualize_parser = subparsers.add_parser('visualize', help='可视化相关功能')
    visualize_subparsers = visualize_parser.add_subparsers(dest='visualize_command', help='可视化命令')
    
    # 可视化流程
    visualize_process_parser = visualize_subparsers.add_parser('process', help='可视化展示流程')
    visualize_process_parser.add_argument('name', help='流程名称')
    
    # 解析参数
    args = parser.parse_args()
    
    # 执行命令
    if args.command == 'check':
        if args.check_command == 'all':
            check_all_data()
        elif args.check_command == 'yaml':
            check_yaml_files(args.directory)
    elif args.command == 'show':
        if args.show_command == 'pending':
            display_pending_methods()
        elif args.show_command == 'processes':
            list_processes()
        elif args.show_command == 'backgrounds':
            list_backgrounds()
        elif args.show_command == 'methods':
            list_methods()
        elif args.show_command == 'requirements':
            list_requirements_with_stories()
        elif args.show_command == 'stories':
            list_user_stories()
        elif args.show_command == 'dependencies':
            dependencies = analyze_module_dependencies()
            if dependencies:
                print("\n模块依赖分析结果:")
                for module, deps in dependencies.items():
                    print(f"{module}: {', '.join(deps) if deps else '无依赖'}")
            else:
                print("\n没有找到模块依赖关系")
    elif args.command == 'create':
        if args.create_command == 'process':
            create_process(args.name, args.background, args.inputs, args.method, args.result)
        elif args.create_command == 'background':
            create_background(args.name, args.description)
        elif args.create_command == 'method':
            create_method(args.name, args.description, args.process)
        elif args.create_command == 'requirement':
            create_requirement(args.name, args.description)
        elif args.create_command == 'story':
            create_user_story(args.requirement, args.name, args.description, args.process)
    elif args.command == 'apply':
        if args.apply_command == 'method':
            apply_method(args.name, args.context)
    elif args.command == 'visualize':
        if args.visualize_command == 'process':
            visualize_process(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
