"""
샘플 계약서 PDF 생성 스크립트
탭2 계약서 리스크 분석기 테스트용
각 계약서에 HIGH/MEDIUM/LOW 리스크 조항이 의도적으로 포함되어 있음

실행: python generate_sample_contracts.py
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT_DIR = Path(__file__).parent

# 윈도우 맑은 고딕 등록
FONT = r"C:\Windows\Fonts\malgun.ttf"
FONT_BD = r"C:\Windows\Fonts\malgunbd.ttf"
pdfmetrics.registerFont(TTFont("Malgun", FONT))
pdfmetrics.registerFont(TTFont("MalgunBd", FONT_BD))


def get_styles():
    styles = {}
    styles["title"] = ParagraphStyle(
        "title", fontName="MalgunBd", fontSize=16, leading=22,
        alignment=1, spaceAfter=6
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle", fontName="Malgun", fontSize=10, leading=14,
        alignment=1, spaceAfter=12, textColor=colors.HexColor("#555555")
    )
    styles["h1"] = ParagraphStyle(
        "h1", fontName="MalgunBd", fontSize=12, leading=16,
        spaceBefore=12, spaceAfter=4,
        textColor=colors.HexColor("#1A3C5E")
    )
    styles["body"] = ParagraphStyle(
        "body", fontName="Malgun", fontSize=9.5, leading=16,
        spaceBefore=2, spaceAfter=2
    )
    styles["risk_high"] = ParagraphStyle(
        "risk_high", fontName="Malgun", fontSize=9.5, leading=16,
        spaceBefore=2, spaceAfter=2,
        backColor=colors.HexColor("#FFF0F0"),
        leftIndent=8, rightIndent=8
    )
    styles["risk_medium"] = ParagraphStyle(
        "risk_medium", fontName="Malgun", fontSize=9.5, leading=16,
        spaceBefore=2, spaceAfter=2,
        backColor=colors.HexColor("#FFFBF0"),
        leftIndent=8, rightIndent=8
    )
    styles["risk_low"] = ParagraphStyle(
        "risk_low", fontName="Malgun", fontSize=9.5, leading=16,
        spaceBefore=2, spaceAfter=2,
        backColor=colors.HexColor("#F0FFF4"),
        leftIndent=8, rightIndent=8
    )
    styles["note"] = ParagraphStyle(
        "note", fontName="Malgun", fontSize=8, leading=12,
        textColor=colors.HexColor("#888888"), leftIndent=12
    )
    return styles


def divider():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC"), spaceAfter=6, spaceBefore=6)


# ─────────────────────────────────────────────────────────────────────────────
# 계약서 1: 물품공급계약서 (사무용 가구)
# 리스크: HIGH×3, MEDIUM×2, LOW×3
# ─────────────────────────────────────────────────────────────────────────────
def create_goods_supply_contract():
    path = OUTPUT_DIR / "물품공급계약서_샘플_리스크포함.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    s = get_styles()
    story = []

    story.append(Paragraph("물품공급계약서", s["title"]))
    story.append(Paragraph("(사무용 가구 납품 계약)", s["subtitle"]))
    story.append(divider())

    # 계약 당사자
    story.append(Paragraph("【계약 당사자】", s["h1"]))
    party_data = [
        ["구분", "회사명", "사업자번호", "대표자", "주소"],
        ["갑 (구매자)", "㈜테크솔루션", "123-45-67890", "이구매", "서울 강남구 테헤란로 100"],
        ["을 (공급업체)", "㈜퍼니처킹", "987-65-43210", "박공급", "경기도 고양시 일산동구 중앙로 500"],
    ]
    t = Table(party_data, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 2.5*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1A3C5E")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,-1), "Malgun"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F5F8FC")]),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("위 당사자는 다음과 같이 물품공급계약을 체결한다.", s["body"]))
    story.append(Spacer(1, 0.3*cm))

    # 제1조
    story.append(Paragraph("제1조 (목적)", s["h1"]))
    story.append(Paragraph(
        "본 계약은 갑이 업무에 필요한 사무용 가구를 을로부터 구매하고, 을이 이를 납품함에 있어 "
        "필요한 제반 사항을 정함을 목적으로 한다.", s["body"]))

    # 제2조
    story.append(Paragraph("제2조 (계약 기간)", s["h1"]))
    story.append(Paragraph(
        "본 계약의 유효기간은 2026년 6월 1일부터 2027년 5월 31일까지로 한다.", s["body"]))

    # 제3조
    story.append(Paragraph("제3조 (납품 품목 및 계약 금액)", s["h1"]))
    item_data = [
        ["품목", "규격", "수량", "단가(원)", "금액(원)"],
        ["사무용 의자", "높낮이/등받이 조절, 팔걸이 포함", "80", "180,000", "14,400,000"],
        ["스탠딩 데스크", "전동식 높낮이 조절, 1200×700mm", "40", "480,000", "19,200,000"],
        ["3인용 소파", "패브릭, 회의용", "10", "850,000", "8,500,000"],
        ["", "", "", "합 계", "42,100,000"],
    ]
    t2 = Table(item_data, colWidths=[3.5*cm, 6*cm, 1.5*cm, 3*cm, 3*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E6DA4")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,-1), "Malgun"),
        ("FONTNAME", (0,0), (-1,0), "MalgunBd"),
        ("FONTNAME", (-2,-1), (-1,-1), "MalgunBd"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (2,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("PADDING", (0,0), (-1,-1), 5),
        ("SPAN", (0,-1), (-3,-1)),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("※ 위 금액은 부가가치세(VAT) 별도 금액임.", s["note"]))

    # 제4조 (LOW RISK: 납품 방식 미명시)
    story.append(Paragraph("제4조 (납품 방식)", s["h1"]))
    story.append(Paragraph(
        "납품 장소, 방식 및 일정은 당사자 간 별도 협의에 의하여 정한다. "
        "납품 관련 세부 조건은 계약 체결 후 을이 제시하는 납품 계획서에 따른다.",
        s["risk_low"]))
    story.append(Paragraph("⚠ [낮은 리스크] 납품 방식 및 장소가 계약서에 명시되지 않아 분쟁 소지 있음", s["note"]))

    # 제5조 (LOW RISK: 검수 기준 미상세)
    story.append(Paragraph("제5조 (검수 및 인수)", s["h1"]))
    story.append(Paragraph(
        "갑은 납품 완료일로부터 7일 이내에 검수를 완료하여야 한다. "
        "이 기간 내 갑의 이의 제기가 없는 경우 검수가 완료된 것으로 간주한다. "
        "하자 발견 시 을에게 서면으로 통보한다.",
        s["risk_low"]))
    story.append(Paragraph("⚠ [낮은 리스크] 검수 기준(품질 기준, 수량 확인 방법 등)이 구체적으로 명시되지 않음", s["note"]))

    # 제6조
    story.append(Paragraph("제6조 (대금 지급)", s["h1"]))
    story.append(Paragraph(
        "갑은 납품 완료 및 세금계산서 수령 후 30일 이내에 계약 금액 전액을 을의 지정 계좌로 지급한다.",
        s["body"]))

    # 제7조 (MEDIUM RISK: 가격 변동 허용)
    story.append(Paragraph("제7조 (가격 조정)", s["h1"]))
    story.append(Paragraph(
        "원자재(철강, 목재, 패브릭) 가격이 계약 시점 대비 10% 이상 변동된 경우, 을은 갑에게 "
        "서면으로 통보한 날로부터 30일 이후 계약 단가를 변경할 수 있다. "
        "이 경우 갑은 을의 가격 조정 요청에 정당한 사유 없이 거부할 수 없다.",
        s["risk_medium"]))
    story.append(Paragraph("⚠ [중간 리스크] 가격 변동 조항 — 을이 일방적으로 단가 인상 가능, 갑의 거부권 제한", s["note"]))

    # 제8조 (HIGH RISK: 납품 지연 면책)
    story.append(Paragraph("제8조 (납품 지연 및 면책)", s["h1"]))
    story.append(Paragraph(
        "을의 귀책사유 없는 사유로 인한 납품 지연에 대하여 갑은 지연 손해금 및 어떠한 손해배상도 "
        "청구할 수 없다. 여기서 '을의 귀책사유 없는 사유'는 천재지변, 전쟁, 파업, 공장 설비 "
        "고장, 원자재 수급 차질, 물류 혼잡, 기타 을이 통제할 수 없다고 판단하는 모든 사유를 "
        "포함한다. 납품 지연 여부 및 면책 사유 해당 여부에 대한 최종 판단은 을이 한다.",
        s["risk_high"]))
    story.append(Paragraph(
        "🔴 [높은 리스크] 납품 지연 면책 범위 과도 — '을이 통제할 수 없다고 판단하는 모든 사유'는 "
        "사실상 무제한 면책이며, 면책 해당 여부 판단권도 을에게 있어 갑에게 극히 불리", s["note"]))

    # 제9조 (HIGH RISK: 손해배상 한도)
    story.append(Paragraph("제9조 (손해배상 한도)", s["h1"]))
    story.append(Paragraph(
        "어떠한 경우에도 을의 갑에 대한 손해배상 책임은 해당 계약 금액의 5%를 초과하지 아니한다. "
        "간접 손해, 기대 이익의 손실, 영업 손실에 대하여 을은 어떠한 책임도 지지 않는다.",
        s["risk_high"]))
    story.append(Paragraph(
        "🔴 [높은 리스크] 손해배상 한도 제한 — 계약금의 5%(210만원)로 상한 설정, "
        "실제 피해 대비 극히 부족하며 간접 손해 면책도 갑에게 불리", s["note"]))

    # 제10조
    story.append(Paragraph("제10조 (계약 해지)", s["h1"]))
    story.append(Paragraph(
        "당사자 일방이 계약을 중대하게 위반하고 14일 이내에 시정하지 않는 경우 "
        "상대방은 서면 통보로 계약을 해지할 수 있다. 단, 을은 갑의 대금 미지급 시 "
        "즉시 계약을 해지하고 이미 납품한 물품의 반환을 청구할 수 있다.",
        s["body"]))

    # 제11조 (HIGH RISK: 자동갱신)
    story.append(Paragraph("제11조 (계약 자동 갱신)", s["h1"]))
    story.append(Paragraph(
        "계약 만료 60일 전까지 갑 또는 을 중 어느 일방의 서면 해지 통보가 없을 경우, "
        "본 계약은 동일한 조건으로 1년씩 자동 연장된다. "
        "자동 연장된 계약에는 제7조의 가격 조정 조항이 우선 적용된다.",
        s["risk_high"]))
    story.append(Paragraph(
        "🔴 [높은 리스크] 자동갱신 조항 — 60일 전 통보 기한 단기, 자동갱신 시 가격조정 조항 "
        "자동 발동되어 비용 증가 위험", s["note"]))

    # 제12조 (MEDIUM RISK: 관할법원)
    story.append(Paragraph("제12조 (분쟁 해결 및 관할법원)", s["h1"]))
    story.append(Paragraph(
        "본 계약과 관련한 모든 분쟁은 협의로 해결함을 원칙으로 하되, "
        "협의가 불성립한 경우 을의 본사 소재지인 경기도 고양시 관할 법원을 "
        "제1심 관할 법원으로 한다.",
        s["risk_medium"]))
    story.append(Paragraph("⚠ [중간 리스크] 분쟁 관할법원이 공급업체(을) 소재지 — 갑(구매자) 입장에서 소송 시 불편", s["note"]))

    # 제13조 (LOW RISK: 하자보증 단기)
    story.append(Paragraph("제13조 (하자보증)", s["h1"]))
    story.append(Paragraph(
        "을은 납품 완료일로부터 3개월간 하자 보증 책임을 진다. "
        "하자보증 기간 이후 발생한 결함에 대하여 을은 책임을 지지 아니한다.",
        s["risk_low"]))
    story.append(Paragraph("⚠ [낮은 리스크] 하자보증 3개월 — 사무가구 통상 보증기간(1~2년) 대비 현저히 짧음", s["note"]))

    # 서명란
    story.append(Spacer(1, 0.8*cm))
    story.append(divider())
    story.append(Paragraph("본 계약을 증명하기 위하여 계약서 2부를 작성하고 당사자가 서명·날인한다.", s["body"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("계약일: 2026년 6월 1일", s["body"]))
    story.append(Spacer(1, 0.5*cm))
    sign_data = [
        ["갑 (구매자)", "", "을 (공급업체)", ""],
        ["회사명: ㈜테크솔루션", "", "회사명: ㈜퍼니처킹", ""],
        ["대표자: 이구매  (인)", "", "대표자: 박공급  (인)", ""],
    ]
    t3 = Table(sign_data, colWidths=[5*cm, 2*cm, 5*cm, 5*cm])
    t3.setStyle(TableStyle([
        ("FONTNAME", (0,0), (-1,-1), "Malgun"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(t3)

    doc.build(story)
    print(f"OK: {path.name}")


# ─────────────────────────────────────────────────────────────────────────────
# 계약서 2: 용역계약서 (건물 청소 용역)
# 리스크: HIGH×2, MEDIUM×3, LOW×2
# ─────────────────────────────────────────────────────────────────────────────
def create_service_contract():
    path = OUTPUT_DIR / "용역계약서_샘플_리스크포함.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    s = get_styles()
    story = []

    story.append(Paragraph("용역공급계약서", s["title"]))
    story.append(Paragraph("(건물 청소 및 위생관리 용역)", s["subtitle"]))
    story.append(divider())

    story.append(Paragraph("【계약 당사자】", s["h1"]))
    party_data = [
        ["구분", "회사명", "사업자번호", "대표자", "주소"],
        ["갑 (발주자)", "㈜글로벌커머스", "234-56-78901", "김발주", "서울 강남구 삼성동 250"],
        ["을 (용역업체)", "㈜클린프로서비스", "876-54-32109", "최청소", "서울 마포구 상암로 200"],
    ]
    t = Table(party_data, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 2.5*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1A3C5E")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,-1), "Malgun"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F5F8FC")]),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("제1조 (목적 및 용역 내용)", s["h1"]))
    story.append(Paragraph(
        "갑은 자사 건물(서울 강남구 삼성동 250 소재, 지하1층~지상12층, 연면적 8,400㎡)의 "
        "청소 및 위생관리 용역을 을에게 위탁하고, 을은 이를 성실히 이행한다.", s["body"]))
    story.append(Spacer(1, 0.2*cm))
    work_data = [
        ["용역 항목", "주기", "내용"],
        ["일상청소", "매일(주5일)", "각 층 사무공간, 복도, 화장실(총 24개) 청소"],
        ["정기청소", "월 2회", "바닥 왁싱, 유리창 내부 청소, 블라인드 청소"],
        ["특수청소", "분기 1회", "외벽 유리창 고소작업 청소"],
        ["소독", "월 1회", "화장실 전면 소독, 엘리베이터(4대) 소독"],
    ]
    t2 = Table(work_data, colWidths=[4*cm, 3*cm, 10*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E6DA4")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,-1), "Malgun"),
        ("FONTNAME", (0,0), (-1,0), "MalgunBd"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("PADDING", (0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F5F8FC")]),
    ]))
    story.append(t2)

    story.append(Paragraph("제2조 (계약 기간 및 금액)", s["h1"]))
    story.append(Paragraph(
        "계약 기간: 2026년 7월 1일 ~ 2027년 6월 30일 (1년)", s["body"]))
    story.append(Paragraph(
        "월 용역 금액: 금 4,800,000원 (부가세 별도) | 연간 총액: 57,600,000원 (부가세 별도)", s["body"]))
    story.append(Paragraph(
        "지급 방법: 매월 말일 익월 5일 이내 지급 (세금계산서 발행 기준)", s["body"]))

    story.append(Paragraph("제3조 (용역 인력)", s["h1"]))
    story.append(Paragraph(
        "을은 상시 청소 인력 최소 8명을 배치하여야 하며, 인력 교체 시 갑에게 사전 통보하여야 한다. "
        "다만, 인력 수급 사정에 따라 을은 갑의 동의 없이 일시적으로 인력을 조정할 수 있다.",
        s["body"]))

    # 제4조 (MEDIUM RISK: 용역 품질 기준 미상세)
    story.append(Paragraph("제4조 (용역 품질 기준)", s["h1"]))
    story.append(Paragraph(
        "을은 용역 수행에 있어 관련 법령 및 업계 통상 수준을 준수하여야 한다. "
        "갑이 용역 품질에 이의가 있는 경우 을에게 시정을 요청할 수 있으며, "
        "이의 인정 여부는 을이 최종 판단한다.",
        s["risk_medium"]))
    story.append(Paragraph("⚠ [중간 리스크] 품질 기준이 '업계 통상 수준'으로 모호하고 이의 인정 판단권이 을에게 있음", s["note"]))

    # 제5조 (HIGH RISK: 일방적 계약 해지권)
    story.append(Paragraph("제5조 (계약 해지)", s["h1"]))
    story.append(Paragraph(
        "을은 다음 각 호에 해당하는 경우 갑에게 30일 전 서면 통보만으로 계약을 해지할 수 있다. "
        "① 사업 운영 방향 변경 ② 용역 단가의 경제적 타당성 상실 ③ 기타 을이 합리적이라고 "
        "판단하는 사유. 을의 해지로 인한 갑의 손해에 대하여 을은 책임을 지지 아니한다.",
        s["risk_high"]))
    story.append(Paragraph(
        "🔴 [높은 리스크] 일방적 해지권 — 을이 '경제적 타당성 상실' 등 모호한 사유로 30일 통보 후 "
        "해지 가능, 갑은 대체 업체 수배 시간 부족 및 손해배상 청구 불가", s["note"]))

    # 제6조 (HIGH RISK: 손해배상 한도)
    story.append(Paragraph("제6조 (손해배상 및 책임 한도)", s["h1"]))
    story.append(Paragraph(
        "을의 용역 수행과 관련하여 발생한 손해에 대한 을의 배상 책임은 월 용역 금액의 50%를 "
        "한도로 한다. 을의 직원 또는 하도급 업체의 과실로 인한 갑의 재산 손해, 개인정보 유출, "
        "업무 방해에 대하여 을은 직접 손해만 배상하며 간접 손해 및 영업 손실은 배상 대상에서 제외한다.",
        s["risk_high"]))
    story.append(Paragraph(
        "🔴 [높은 리스크] 손해배상 한도 월 용역비의 50%(240만원) — 청소 직원 실수로 인한 "
        "비품 훼손, 도난 등 실손해가 이를 초과할 경우 갑이 초과분 부담", s["note"]))

    # 제7조 (MEDIUM RISK: 하도급 제한 불명확)
    story.append(Paragraph("제7조 (하도급)", s["h1"]))
    story.append(Paragraph(
        "을은 특수청소(고소작업) 등 전문성이 요구되는 작업에 대하여 갑의 사전 동의 없이 "
        "제3자에게 하도급을 줄 수 있다. 하도급 업체의 작업 결과에 대한 최종 책임은 을에게 있으나, "
        "하도급 업체의 불법행위로 인한 손해에 대하여는 을의 귀책이 없는 것으로 본다.",
        s["risk_medium"]))
    story.append(Paragraph("⚠ [중간 리스크] 동의 없는 하도급 허용, 하도급 업체 불법행위 시 책임 회피 가능", s["note"]))

    # 제8조 (MEDIUM RISK: 지식재산권)
    story.append(Paragraph("제8조 (자료 및 지식재산권)", s["h1"]))
    story.append(Paragraph(
        "을이 용역 수행 과정에서 취득한 갑의 사업장 정보, 임직원 정보, 방문객 정보 등은 "
        "용역 수행 목적 외 사용을 금한다. 단, 을이 개발한 청소 관리 시스템, 용역 수행 노하우 "
        "등 지적재산은 을의 소유로 하며 갑은 이에 대한 권리를 주장할 수 없다.",
        s["risk_medium"]))
    story.append(Paragraph("⚠ [중간 리스크] 지식재산권 귀속 조항이 불명확 — 갑의 시설 맞춤 개선 노하우도 을 소유로 귀속 가능", s["note"]))

    # 제9조 (LOW RISK: 하자보증 기간)
    story.append(Paragraph("제9조 (용역 결과 보증)", s["h1"]))
    story.append(Paragraph(
        "을은 용역 완료 후 3일 이내에 갑이 이의를 제기한 사항에 한하여 무상 재작업을 실시한다. "
        "3일 이후 제기된 이의에 대하여 을은 별도 요금을 청구할 수 있다.",
        s["risk_low"]))
    story.append(Paragraph("⚠ [낮은 리스크] 용역 결과 보증 기간 3일 — 청소 후 위생 문제는 수일 후 발현될 수 있어 단기", s["note"]))

    # 제10조 (LOW RISK: 작업 시간 미명시)
    story.append(Paragraph("제10조 (작업 시간)", s["h1"]))
    story.append(Paragraph(
        "청소 작업 시간은 갑과 을의 협의로 정하되, 업무 효율을 고려하여 을이 적절히 조정할 수 있다.",
        s["risk_low"]))
    story.append(Paragraph("⚠ [낮은 리스크] 구체적 작업 시간 미명시 — 야간/주말 작업 여부, 업무 시간 중 작업 범위 불명확", s["note"]))

    story.append(Spacer(1, 0.8*cm))
    story.append(divider())
    story.append(Paragraph("계약일: 2026년 7월 1일", s["body"]))
    story.append(Spacer(1, 0.5*cm))
    sign_data = [
        ["갑 (발주자)", "", "을 (용역업체)", ""],
        ["회사명: ㈜글로벌커머스", "", "회사명: ㈜클린프로서비스", ""],
        ["대표자: 김발주  (인)", "", "대표자: 최청소  (인)", ""],
    ]
    t3 = Table(sign_data, colWidths=[5*cm, 2*cm, 5*cm, 5*cm])
    t3.setStyle(TableStyle([("FONTNAME", (0,0), (-1,-1), "Malgun"), ("FONTSIZE", (0,0), (-1,-1), 9), ("TOPPADDING", (0,0), (-1,-1), 6)]))
    story.append(t3)

    doc.build(story)
    print(f"OK: {path.name}")


# ─────────────────────────────────────────────────────────────────────────────
# 계약서 3: 유지보수계약서 (IT 시스템 유지보수)
# 리스크: HIGH×2, MEDIUM×2, LOW×3
# ─────────────────────────────────────────────────────────────────────────────
def create_maintenance_contract():
    path = OUTPUT_DIR / "유지보수계약서_샘플_리스크포함.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    s = get_styles()
    story = []

    story.append(Paragraph("IT시스템 유지보수 계약서", s["title"]))
    story.append(Paragraph("(ERP 및 그룹웨어 유지보수)", s["subtitle"]))
    story.append(divider())

    story.append(Paragraph("【계약 당사자】", s["h1"]))
    party_data = [
        ["구분", "회사명", "사업자번호", "대표자", "주소"],
        ["갑 (발주사)", "㈜한국제조", "345-67-89012", "정발주", "경기도 수원시 영통구 광교로 100"],
        ["을 (유지보수업체)", "㈜아이티솔루션즈", "765-43-21098", "손IT", "서울 서초구 반포대로 200"],
    ]
    t = Table(party_data, colWidths=[2.5*cm, 3.5*cm, 3.5*cm, 2.5*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1A3C5E")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,-1), "Malgun"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F5F8FC")]),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))

    story.append(Paragraph("제1조 (목적)", s["h1"]))
    story.append(Paragraph(
        "본 계약은 갑이 운영하는 ERP(SAP S/4HANA) 및 그룹웨어(Microsoft 365) 시스템의 "
        "안정적 운영을 위해 을이 유지보수 서비스를 제공함에 있어 필요한 사항을 정한다.", s["body"]))

    story.append(Paragraph("제2조 (유지보수 범위)", s["h1"]))
    scope_data = [
        ["서비스 항목", "SLA 기준", "비고"],
        ["장애 대응", "긴급: 2시간 / 일반: 24시간 내 복구", "연중 무휴"],
        ["정기 점검", "월 1회, 4시간 이내", "주말 실시"],
        ["소프트웨어 패치", "분기 1회", "을의 판단에 따라 실시"],
        ["사용자 교육", "연 2회, 각 4시간", "온라인 가능"],
        ["백업 관리", "일 1회 증분, 주 1회 전체", "보관: 30일"],
    ]
    t2 = Table(scope_data, colWidths=[4*cm, 6*cm, 5*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2E6DA4")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,-1), "Malgun"),
        ("FONTNAME", (0,0), (-1,0), "MalgunBd"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("PADDING", (0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F5F8FC")]),
    ]))
    story.append(t2)

    story.append(Paragraph("제3조 (계약 금액)", s["h1"]))
    story.append(Paragraph(
        "월 유지보수 비용: 금 6,500,000원 (부가세 별도) | 연간 총액: 78,000,000원", s["body"]))
    story.append(Paragraph(
        "지급 조건: 매월 1일 선급 지급 (세금계산서 말일 발행)", s["body"]))

    # 제4조 (MEDIUM RISK: 가격 인상)
    story.append(Paragraph("제4조 (유지보수 비용 조정)", s["h1"]))
    story.append(Paragraph(
        "을은 인건비 상승률, 소프트웨어 라이선스 비용 변동, 물가 상승률을 반영하여 "
        "연 1회에 한하여 유지보수 비용을 조정할 수 있다. 조정 폭은 전년도 소비자물가지수 "
        "상승률의 150% 이내로 하며, 갑에게 60일 전 서면 통보로 효력이 발생한다. "
        "갑이 이를 거부할 경우 을은 본 계약을 해지할 수 있다.",
        s["risk_medium"]))
    story.append(Paragraph("⚠ [중간 리스크] 연간 자동 가격 인상 조항 — 거부 시 을의 계약 해지권 발동, 갑의 협상력 약화", s["note"]))

    # 제5조 (HIGH RISK: 자동갱신)
    story.append(Paragraph("제5조 (계약 기간 및 자동 갱신)", s["h1"]))
    story.append(Paragraph(
        "본 계약의 유효기간은 2026년 8월 1일부터 2027년 7월 31일까지로 하되, "
        "계약 만료 90일 전까지 갑이 서면으로 해지 의사를 통보하지 않는 경우 "
        "동일 조건으로 1년씩 자동 갱신된다. "
        "자동 갱신 시 제4조에 의한 비용 조정이 자동 적용된다.",
        s["risk_high"]))
    story.append(Paragraph(
        "🔴 [높은 리스크] 90일 전 통보 기한 + 자동갱신 시 가격 인상 자동 적용 — "
        "갑이 타사 검토 기회를 놓칠 경우 비용 증가와 함께 장기 고착화 위험", s["note"]))

    # 제6조 (HIGH RISK: 손해배상)
    story.append(Paragraph("제6조 (손해배상 및 서비스 중단 면책)", s["h1"]))
    story.append(Paragraph(
        "을의 유지보수 서비스 중단 또는 장애 복구 지연으로 인한 갑의 손해에 대하여 "
        "을의 배상 책임은 해당 월 유지보수 비용의 30%를 초과하지 아니한다. "
        "을의 귀책사유 없는 서비스 중단(외부 인터넷망 장애, 클라우드 사업자 장애, "
        "갑의 내부 네트워크 이슈 등)으로 인한 손해에 대하여 을은 어떠한 책임도 지지 않는다. "
        "ERP 장애로 인한 생산 중단, 영업 손실, 데이터 손실에 대한 간접 손해는 배상하지 않는다.",
        s["risk_high"]))
    story.append(Paragraph(
        "🔴 [높은 리스크] 손해배상 한도 월비의 30%(195만원) — ERP 장애로 인한 생산 라인 중단 "
        "등 실제 손해는 수억 원에 달할 수 있으나 사실상 면책", s["note"]))

    # 제7조 (MEDIUM RISK: 지식재산권)
    story.append(Paragraph("제7조 (소스코드 및 지식재산권)", s["h1"]))
    story.append(Paragraph(
        "을이 유지보수 과정에서 개발한 커스터마이징 코드, 스크립트, 보고서 양식 등의 "
        "지식재산권은 을에게 귀속된다. 갑은 을과의 계약 기간 중에 한하여 이를 사용할 수 있으며, "
        "계약 해지 시 을은 소스코드 등의 반환 의무를 지지 않는다.",
        s["risk_medium"]))
    story.append(Paragraph(
        "⚠ [중간 리스크] 갑의 시스템을 위해 개발된 커스터마이징 코드 소유권이 을에게 귀속 — "
        "계약 해지 후 소스코드 미반환 시 시스템 운영 연속성 위협", s["note"]))

    # 제8조 (LOW RISK: 장애 대응 기준)
    story.append(Paragraph("제8조 (장애 등급 및 대응 기준)", s["h1"]))
    story.append(Paragraph(
        "장애 등급 분류는 을의 내부 기준에 따르며, 갑은 장애 접수 후 을의 등급 판단에 따라 "
        "서비스를 받는다. 장애 등급에 대한 이견이 있는 경우 협의로 해결한다.",
        s["risk_low"]))
    story.append(Paragraph("⚠ [낮은 리스크] 장애 등급 판단 기준이 을 내부 기준에 따라 주관적 — 갑이 긴급이라 판단해도 일반 처리될 수 있음", s["note"]))

    # 제9조 (LOW RISK: 정기점검 후 검수)
    story.append(Paragraph("제9조 (정기점검 결과 보고)", s["h1"]))
    story.append(Paragraph(
        "을은 월 1회 정기점검 후 점검 결과를 구두 또는 이메일로 갑에게 통보한다. "
        "갑이 3일 이내에 이의를 제기하지 않는 경우 정기점검이 완료된 것으로 본다.",
        s["risk_low"]))
    story.append(Paragraph("⚠ [낮은 리스크] 구두 보고 허용 — 서면 점검 결과서 없이 처리, 추후 분쟁 시 이행 여부 증명 곤란", s["note"]))

    # 제10조 (LOW RISK: 하자보증)
    story.append(Paragraph("제10조 (작업 결과 보증)", s["h1"]))
    story.append(Paragraph(
        "을이 수행한 패치 및 업그레이드 작업에 대한 하자 보증 기간은 작업 완료 후 14일로 한다. "
        "14일 이후 발생하는 동일 현상은 신규 장애로 처리하여 추가 비용이 발생할 수 있다.",
        s["risk_low"]))
    story.append(Paragraph("⚠ [낮은 리스크] 패치 작업 하자보증 14일 — 소프트웨어 패치 영향은 14일 이후 발현될 수 있음", s["note"]))

    # 제11조
    story.append(Paragraph("제11조 (비밀유지)", s["h1"]))
    story.append(Paragraph(
        "을은 업무 수행 중 취득한 갑의 영업 비밀, 기술 정보, 고객 정보 등을 "
        "계약 기간 및 계약 종료 후 2년간 제3자에게 누설하지 않는다.", s["body"]))

    story.append(Spacer(1, 0.8*cm))
    story.append(divider())
    story.append(Paragraph("계약일: 2026년 8월 1일", s["body"]))
    story.append(Spacer(1, 0.5*cm))
    sign_data = [
        ["갑 (발주사)", "", "을 (유지보수업체)", ""],
        ["회사명: ㈜한국제조", "", "회사명: ㈜아이티솔루션즈", ""],
        ["대표자: 정발주  (인)", "", "대표자: 손IT  (인)", ""],
    ]
    t3 = Table(sign_data, colWidths=[5*cm, 2*cm, 5*cm, 5*cm])
    t3.setStyle(TableStyle([("FONTNAME", (0,0), (-1,-1), "Malgun"), ("FONTSIZE", (0,0), (-1,-1), 9), ("TOPPADDING", (0,0), (-1,-1), 6)]))
    story.append(t3)

    doc.build(story)
    print(f"OK: {path.name}")


if __name__ == "__main__":
    print("샘플 계약서 PDF 생성 중...")
    create_goods_supply_contract()
    create_service_contract()
    create_maintenance_contract()
    print("모든 계약서 PDF 생성 완료!")
    print(f"저장 위치: {OUTPUT_DIR}")
