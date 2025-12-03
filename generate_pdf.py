#!/usr/bin/env python3
"""
将 Claude Code 完全指南转换为 PDF
"""
import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

# 注册中文字体（使用系统自带字体）
try:
    # macOS 系统字体
    pdfmetrics.registerFont(TTFont('SourceHanSans', '/System/Library/Fonts/PingFang.ttc', subfontIndex=1))
    pdfmetrics.registerFont(TTFont('SourceHanSans-Bold', '/System/Library/Fonts/PingFang.ttc', subfontIndex=0))
    FONT_NAME = 'SourceHanSans'
    FONT_BOLD = 'SourceHanSans-Bold'
except:
    try:
        # 备选字体
        pdfmetrics.registerFont(TTFont('SourceHanSans', '/System/Library/Fonts/STHeiti Light.ttc'))
        FONT_NAME = 'SourceHanSans'
        FONT_BOLD = 'SourceHanSans'
    except:
        # 如果都失败，使用默认字体
        FONT_NAME = 'Helvetica'
        FONT_BOLD = 'Helvetica-Bold'

def create_styles():
    """创建文档样式"""
    styles = getSampleStyleSheet()
    
    # 标题样式
    styles.add(ParagraphStyle(
        name='ChineseTitle',
        parent=styles['Title'],
        fontName=FONT_BOLD,
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    ))
    
    # 一级标题
    styles.add(ParagraphStyle(
        name='ChineseHeading1',
        parent=styles['Heading1'],
        fontName=FONT_BOLD,
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12
    ))
    
    # 二级标题
    styles.add(ParagraphStyle(
        name='ChineseHeading2',
        parent=styles['Heading2'],
        fontName=FONT_BOLD,
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=10
    ))
    
    # 三级标题
    styles.add(ParagraphStyle(
        name='ChineseHeading3',
        parent=styles['Heading3'],
        fontName=FONT_BOLD,
        fontSize=12,
        textColor=colors.HexColor('#555555'),
        spaceAfter=8,
        spaceBefore=8
    ))
    
    # 正文
    styles.add(ParagraphStyle(
        name='ChineseBody',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=10,
        leading=16,
        textColor=colors.HexColor('#333333'),
        alignment=TA_JUSTIFY,
        spaceAfter=8
    ))
    
    # 代码块 - 使用中文字体以支持中文注释
    styles.add(ParagraphStyle(
        name='ChineseCode',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2c3e50'),
        backColor=colors.HexColor('#f5f5f5'),
        leftIndent=10,
        rightIndent=10,
        spaceAfter=8,
        spaceBefore=8
    ))
    
    # 引用
    styles.add(ParagraphStyle(
        name='ChineseQuote',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#555555'),
        leftIndent=20,
        borderPadding=10,
        borderColor=colors.HexColor('#3498db'),
        borderWidth=2,
        spaceAfter=10,
        spaceBefore=10
    ))
    
    return styles

def clean_markdown_text(text):
    """清理 Markdown 文本，转换为纯文本，并转义 HTML 特殊字符"""
    # 移除代码块标记
    text = re.sub(r'```[\s\S]*?```', '[代码块]', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # 移除图片标记
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'[图片: \1]', text)
    
    # 移除链接标记，保留文字
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # 移除粗体和斜体标记
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'\*([^\*]+)\*', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    
    # 移除表格分隔线
    text = re.sub(r'\|[-:]+\|', '', text)
    
    # 转义 HTML 特殊字符
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    return text

def process_markdown_file(filepath, styles):
    """处理单个 Markdown 文件"""
    story = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return story
    
    lines = content.split('\n')
    in_code_block = False
    code_lines = []
    in_table = False
    table_lines = []
    
    for line in lines:
        # 处理代码块
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                if code_lines:
                    # 简化代码块处理，每行单独作为一个段落
                    for code_line in code_lines[:20]:  # 限制代码行数
                        if code_line.strip():
                            clean_line = clean_markdown_text(code_line[:100])  # 限制行长度
                            try:
                                story.append(Paragraph(clean_line, styles['ChineseCode']))
                            except:
                                pass
                    if len(code_lines) > 20:
                        story.append(Paragraph('... (代码省略)', styles['ChineseCode']))
                code_lines = []
            continue
        
        if in_code_block:
            code_lines.append(line)
            continue
        
        # 处理标题
        if line.startswith('# '):
            text = clean_markdown_text(line[2:].strip())
            story.append(Paragraph(text, styles['ChineseTitle']))
            story.append(Spacer(1, 0.5*cm))
        elif line.startswith('## '):
            text = clean_markdown_text(line[3:].strip())
            story.append(Paragraph(text, styles['ChineseHeading1']))
        elif line.startswith('### '):
            text = clean_markdown_text(line[4:].strip())
            story.append(Paragraph(text, styles['ChineseHeading2']))
        elif line.startswith('#### '):
            text = clean_markdown_text(line[5:].strip())
            story.append(Paragraph(text, styles['ChineseHeading3']))
        
        # 处理引用
        elif line.startswith('> '):
            text = clean_markdown_text(line[2:].strip())
            if text:
                story.append(Paragraph(text, styles['ChineseQuote']))
        
        # 处理表格
        elif '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
        else:
            if in_table:
                # 表格结束，简化处理：转为文本
                in_table = False
                for tline in table_lines:
                    cells = [c.strip() for c in tline.split('|') if c.strip()]
                    if cells and not all(c.replace('-', '').replace(':', '') == '' for c in cells):
                        story.append(Paragraph(' | '.join(cells), styles['ChineseBody']))
                table_lines = []
            
            # 处理普通文本
            if line.strip():
                text = clean_markdown_text(line.strip())
                if text:
                    story.append(Paragraph(text, styles['ChineseBody']))
            else:
                story.append(Spacer(1, 0.2*cm))
    
    return story

def generate_pdf():
    """生成 PDF"""
    base_dir = Path(__file__).parent
    output_file = base_dir / "Claude_Code完全指南.pdf"
    
    # 创建 PDF 文档
    doc = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    story = []
    styles = create_styles()
    
    # 文件顺序列表
    file_order = [
        'README.md',
        # 第一部分
        'part1-introduction/chapter01-introduction.md',
        'part1-introduction/chapter02-history.md',
        'part1-introduction/chapter03-installation.md',
        'part1-introduction/chapter04-first-conversation.md',
        'part1-introduction/chapter05-basic-commands.md',
        # 第二部分
        'part2-configuration/chapter06-claude-md.md',
        'part2-configuration/chapter07-permissions.md',
        'part2-configuration/chapter08-multi-environment.md',
        # 第三部分
        'part3-intermediate/chapter09-session-context.md',
        'part3-intermediate/chapter10-file-operations.md',
        'part3-intermediate/chapter11-architecture.md',
        'part3-intermediate/chapter12-prompt-engineering.md',
        'part3-intermediate/chapter13-headless-mode.md',
        # 第四部分
        'part4-advanced/chapter14-hooks.md',
        'part4-advanced/chapter15-skills.md',
        'part4-advanced/chapter16-spec.md',
        'part4-advanced/chapter17-mcp.md',
        # 第五部分
        'part5-workflow/chapter18-workflow-patterns.md',
        'part5-workflow/chapter19-tool-integration.md',
        'part5-workflow/chapter20-multilang.md',
        # 第六部分
        'part6-practice/chapter21-fullstack-project.md',
        'part6-practice/chapter22-refactoring.md',
        'part6-practice/chapter23-testing.md',
        'part6-practice/chapter24-cicd.md',
        # 第七部分
        'part7-mastery/chapter25-enterprise.md',
        'part7-mastery/chapter26-cost.md',
        'part7-mastery/chapter27-performance.md',
        'part7-mastery/chapter28-security.md',
        'part7-mastery/chapter29-future.md',
        # 附录
        'appendix/appendix-a-cheatsheet.md',
        'appendix/appendix-b-decision-tree.md',
        'appendix/appendix-c-version-comparison.md',
        'appendix/appendix-d-troubleshooting.md',
        'appendix/appendix-e-glossary.md',
        'appendix/appendix-f-resources.md',
        'appendix/appendix-g-glossary-new-terms.md',
    ]
    
    print("开始生成 PDF...")
    
    # 处理每个文件
    for i, file_path in enumerate(file_order, 1):
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"处理 ({i}/{len(file_order)}): {file_path}")
            file_story = process_markdown_file(full_path, styles)
            story.extend(file_story)
            
            # 每章后添加分页符（除了最后一个文件）
            if i < len(file_order):
                story.append(PageBreak())
        else:
            print(f"文件不存在: {file_path}")
    
    # 生成 PDF
    print("正在生成 PDF 文件...")
    doc.build(story)
    print(f"✓ PDF 已生成: {output_file}")
    print(f"文件大小: {output_file.stat().st_size / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    generate_pdf()
