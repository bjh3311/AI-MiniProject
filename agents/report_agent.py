from typing import Dict
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from dotenv import load_dotenv

load_dotenv()

# 한글 폰트 등록 (Windows에 있는 맑은 고딕 사용)
pdfmetrics.registerFont(TTFont('Malgun', 'C:/Windows/Fonts/malgun.ttf'))

def generate_report(state: Dict) -> Dict:
    """Report 노드에서 AI 미래 기술 트렌드 분석 보고서를 생성하는 함수"""
    
    # 상태에서 데이터 가져오기
    top_trends = state.get("top_trends", [])
    summary_data = state.get("summary", [])

    # 기본 PDF 파일 경로
    output_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = os.path.join(output_dir, f"AI_Tech_Trends_Report_{timestamp}.pdf")
    
    # PDF 생성
    create_pdf_report(pdf_filename, top_trends, summary_data)
    return state

def create_pdf_report(pdf_filename, top_trends, summary_data):
    """
    ReportLab을 사용하여 PDF 보고서 생성
    """
    # 스타일 정의 - 이름 충돌 방지를 위해 Custom 접두사 사용
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CustomTitle', 
                             fontName='Malgun', 
                             fontSize=16, 
                             alignment=1, 
                             spaceAfter=20))
    styles.add(ParagraphStyle(name='CustomHeading', 
                             fontName='Malgun', 
                             fontSize=14, 
                             spaceAfter=10))
    styles.add(ParagraphStyle(name='CustomSubHeading', 
                             fontName='Malgun', 
                             fontSize=12,
                             spaceAfter=8))
    styles.add(ParagraphStyle(name='CustomNormal', 
                             fontName='Malgun', 
                             fontSize=10, 
                             spaceAfter=10))
    styles.add(ParagraphStyle(name='CustomBold',
                             fontName='Malgun',
                             fontSize=10,
                             spaceAfter=10,
                             bold=True))
    
    # PDF 문서 생성
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    story = []
    
    # 표지 추가
    title = Paragraph('미래 기술 트렌드 분석 보고서', styles['CustomTitle'])
    story.append(title)
    
    date = Paragraph(f'작성일: {datetime.now().strftime("%Y년 %m월 %d일")}', styles['CustomNormal'])
    story.append(date)
    story.append(Spacer(1, 30))
    
    # 목차 추가
    toc_title = Paragraph('목차', styles['CustomHeading'])
    story.append(toc_title)
    
    toc_items = []
    toc_items.append(['1. 개요', '3'])
    toc_items.append(['2. 상위 AI 트렌드 요약', '4'])
    
    # 트렌드별 목차 항목 추가
    for i, trend in enumerate(top_trends, 3):
        toc_items.append([f"{i}. {trend['keyword']} 상세 분석", str(i+2)])
    
    # 목차 테이블
    toc = Table(toc_items, colWidths=[350, 50])
    toc.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Malgun'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    story.append(toc)
    story.append(Spacer(1, 30))
    
    # 개요 섹션 추가 (페이지 나누기)
    story.append(Spacer(1, 1))
    story.append(Paragraph('1. 개요', styles['CustomHeading']))
    
    overview_text = """
    본 보고서는 최신 AI 기술 트렌드에 대한 종합적인 분석 결과를 제공합니다. 
    뉴스 기사와 인터넷 자료를 바탕으로 주요 AI 기술 트렌드를 식별하고, 
    각 트렌드의 시장 성장성, 기업 채택률, 기술 성숙도, 혁신 잠재력, 지속가능성을 평가했습니다.
    
    이를 통해 향후 5년 내 기업과 조직이 주목해야 할 AI 기술 방향성을 제시합니다.
    """
    story.append(Paragraph(overview_text, styles['CustomNormal']))
    story.append(Spacer(1, 20))
    
    # 상위 AI 트렌드 요약 테이블 (새 페이지)
    story.append(Spacer(1, 1))
    story.append(Paragraph('2. 상위 AI 트렌드 요약', styles['CustomHeading']))
    
    # 트렌드 테이블 데이터
    table_data = [['키워드', '점수', '주요 이유']]
    for trend in top_trends:
        # 주요 이유 텍스트 길이 제한 (150자 이내로)
        reason_text = trend.get('reason', '')
        if len(reason_text) > 150:
            reason_text = reason_text[:147] + '...'
        
        # Paragraph 객체를 사용하여 자동 줄바꿈 처리
        reason_paragraph = Paragraph(reason_text, styles['CustomNormal'])
        
        table_data.append([
            trend['keyword'], 
            str(trend['score']), 
            reason_paragraph
        ])
    
    # 테이블 생성
    table = Table(table_data, colWidths=[100, 50, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Malgun'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 30))
    
    # 각 트렌드별 상세 페이지 추가
    for i, trend in enumerate(top_trends, 3):
        # 페이지 나누기 및 섹션 제목
        story.append(Spacer(1, 1))
        trend_title = Paragraph(f"{i}. {trend['keyword']} 상세 분석", styles['CustomHeading'])
        story.append(trend_title)
        story.append(Spacer(1, 10))
        
        # 1. 트렌드 이름과 총점
        score_text = Paragraph(f"<b>총점:</b> {trend['score']}/10", styles['CustomBold'])
        story.append(score_text)
        story.append(Spacer(1, 10))
        
        # 2. 트렌드 요약 - summary_data에서 해당 키워드의 요약 찾기
        summary_text = "해당 키워드에 대한 요약 정보가 없습니다."
        for summary_item in summary_data:
            if summary_item.get("keyword") == trend["keyword"]:
                summary_text = summary_item.get("summary", summary_text)
                break
        
        summary_title = Paragraph("2.1 트렌드 요약", styles['CustomSubHeading'])
        story.append(summary_title)
        story.append(Paragraph(summary_text, styles['CustomNormal']))
        story.append(Spacer(1, 10))
        
        # 3. 항목별 점수
        detail_title = Paragraph("2.2 항목별 평가 점수", styles['CustomSubHeading'])
        story.append(detail_title)
        
        if "details" in trend:
            details = trend["details"]
            detail_data = [
                ['평가 항목', '점수 (0-10)'],
                ['시장 성장성', str(details.get('market_growth', 'N/A'))],
                ['기업 채택률', str(details.get('enterprise_adoption', 'N/A'))],
                ['기술 성숙도', str(details.get('tech_maturity', 'N/A'))],
                ['혁신 잠재력', str(details.get('innovation_potential', 'N/A'))],
                ['지속가능성', str(details.get('sustainability', 'N/A'))]
            ]
            
            detail_table = Table(detail_data, colWidths=[150, 100])
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Malgun'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(detail_table)
            story.append(Spacer(1, 15))
            
        # 4. 분석 (reason 내용 포함)
        analysis_title = Paragraph("2.3 분석", styles['CustomSubHeading'])
        story.append(analysis_title)
        analysis_text = trend.get('reason', '분석 내용이 제공되지 않았습니다.')
        story.append(Paragraph(analysis_text, styles['CustomNormal']))
        story.append(Spacer(1, 15))
        
        # 5. 총평 (간단한 요약 및 권장사항)
        conclusion_title = Paragraph("2.4 총평", styles['CustomSubHeading'])
        story.append(conclusion_title)
        
        # 총점 기반 평가 문구
        score = float(trend.get('score', 0))
        if score >= 8.5:
            conclusion = f"{trend['keyword']}는 매우 유망한 기술 트렌드로, 기업들이 우선적으로 투자하고 도입을 검토해야 합니다. 빠른 속도로 발전하고 있으며, 경쟁 우위를 확보하기 위해 즉각적인 관심이 필요합니다."
        elif score >= 7.0:
            conclusion = f"{trend['keyword']}는 향후 중요한 역할을 할 것으로 예상되는 기술 트렌드입니다. 전략적 계획에 포함시키고 준비를 시작하는 것이 좋습니다."
        elif score >= 5.0:
            conclusion = f"{trend['keyword']}는 잠재력이 있지만 더 지켜볼 필요가 있는 기술 트렌드입니다. 현재 단계에서는 모니터링하며 적절한 진입 시점을 탐색하는 것이 권장됩니다."
        else:
            conclusion = f"{trend['keyword']}는 아직 초기 단계이거나 산업 적용성이 제한적일 수 있습니다. 장기적인 관점에서 지켜보는 것이 좋습니다."
        
        story.append(Paragraph(conclusion, styles['CustomNormal']))
        story.append(Spacer(1, 30))
    
    # PDF 빌드
    doc.build(story)
