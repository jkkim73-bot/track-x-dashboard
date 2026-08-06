import streamlit as st
import pandas as pd
import numpy as np
import requests
import xml.etree.ElementTree as ET
import time

# ==========================================
# 1. Streamlit 웹 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="Track X Dashboard",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# 2. KOSPI 219 유니버스 데이터 정의
# ==========================================
KOSPI_219_UNIVERSE = [
    {"code": "005930", "name": "삼성전자", "sector": "정보기술"},
    {"code": "000660", "name": "SK하이닉스", "sector": "정보기술"},
    {"code": "005935", "name": "삼성전자우", "sector": "정보기술"},
    {"code": "009150", "name": "삼성전기", "sector": "정보기술"},
    {"code": "066570", "name": "LG전자", "sector": "정보기술"},
    {"code": "034220", "name": "LG디스플레이", "sector": "정보기술"},
    {"code": "011070", "name": "LG이노텍", "sector": "정보기술"},
    {"code": "018260", "name": "삼성SDS", "sector": "정보기술"},
    {"code": "042700", "name": "한미반도체", "sector": "정보기술"},
    {"code": "108320", "name": "LX세미콘", "sector": "정보기술"},
    {"code": "004130", "name": "대덕전자", "sector": "정보기술"},
    {"code": "032390", "name": "다우기술", "sector": "정보기술"},
    {"code": "036810", "name": "DI동일", "sector": "정보기술"},
    {"code": "207940", "name": "삼성바이오로직스", "sector": "헬스케어"},
    {"code": "068270", "name": "셀트리온", "sector": "헬스케어"},
    {"code": "000100", "name": "유한양행", "sector": "헬스케어"},
    {"code": "128940", "name": "한미약품", "sector": "헬스케어"},
    {"code": "006280", "name": "GC녹십자", "sector": "헬스케어"},
    {"code": "185750", "name": "종근당", "sector": "헬스케어"},
    {"code": "214300", "name": "대웅제약", "sector": "헬스케어"},
    {"code": "302440", "name": "SK바이오사이언스", "sector": "헬스케어"},
    {"code": "326030", "name": "SK바이오팜", "sector": "헬스케어"},
    {"code": "008930", "name": "한미사이언스", "sector": "헬스케어"},
    {"code": "003090", "name": "대웅", "sector": "헬스케어"},
    {"code": "102940", "name": "코오롱생명과학", "sector": "헬스케어"},
    {"code": "001060", "name": "JW중외제약", "sector": "헬스케어"},
    {"code": "003000", "name": "부광약품", "sector": "헬스케어"},
    {"code": "003850", "name": "보령", "sector": "헬스케어"},
    {"code": "005250", "name": "녹십자홀딩스", "sector": "헬스케어"},
    {"code": "000670", "name": "영진약품", "sector": "헬스케어"},
    {"code": "000180", "name": "성창기업지주", "sector": "헬스케어"},
    {"code": "020150", "name": "일진머티리얼즈", "sector": "헬스케어"},
    {"code": "105560", "name": "KB금융", "sector": "금융"},
    {"code": "055550", "name": "신한지주", "sector": "금융"},
    {"code": "086790", "name": "하나금융지주", "sector": "금융"},
    {"code": "316140", "name": "우리금융지주", "sector": "금융"},
    {"code": "000060", "name": "메리츠금융지주", "sector": "금융"},
    {"code": "323410", "name": "카카오뱅크", "sector": "금융"},
    {"code": "377300", "name": "카카오페이", "sector": "금융"},
    {"code": "024110", "name": "기업은행", "sector": "금융"},
    {"code": "032830", "name": "삼성생명", "sector": "금융"},
    {"code": "000810", "name": "삼성화재", "sector": "금융"},
    {"code": "005830", "name": "DB손해보험", "sector": "금융"},
    {"code": "001450", "name": "현대해상", "sector": "금융"},
    {"code": "088350", "name": "한화생명", "sector": "금융"},
    {"code": "000370", "name": "한화손해보험", "sector": "금융"},
    {"code": "006800", "name": "미래에셋증권", "sector": "금융"},
    {"code": "016360", "name": "삼성증권", "sector": "금융"},
    {"code": "005940", "name": "NH투자증권", "sector": "금융"},
    {"code": "071050", "name": "한국금융지주", "sector": "금융"},
    {"code": "039490", "name": "키움증권", "sector": "금융"},
    {"code": "003540", "name": "대신증권", "sector": "금융"},
    {"code": "003530", "name": "한화투자증권", "sector": "금융"},
    {"code": "001720", "name": "신영증권", "sector": "금융"},
    {"code": "001750", "name": "한양증권", "sector": "금융"},
    {"code": "003470", "name": "유안타증권", "sector": "금융"},
    {"code": "030210", "name": "다올투자증권", "sector": "금융"},
    {"code": "001270", "name": "부국증권", "sector": "금융"},
    {"code": "021050", "name": "서원", "sector": "금융"},
    {"code": "003620", "name": "KG모빌리티", "sector": "금융"},
    {"code": "402340", "name": "SK스퀘어", "sector": "금융"},
    {"code": "000540", "name": "흥국화재", "sector": "금융"},
    {"code": "000050", "name": "경방", "sector": "금융"},
    {"code": "001200", "name": "유진투자증권", "sector": "금융"},
    {"code": "001500", "name": "조선내화", "sector": "금융"},
    {"code": "005380", "name": "현대차", "sector": "자유소비재"},
    {"code": "000270", "name": "기아", "sector": "자유소비재"},
    {"code": "012330", "name": "현대모비스", "sector": "자유소비재"},
    {"code": "018880", "name": "한온시스템", "sector": "자유소비재"},
    {"code": "011210", "name": "현대위아", "sector": "자유소비재"},
    {"code": "005850", "name": "에스엘", "sector": "자유소비재"},
    {"code": "000240", "name": "한국앤컴퍼니", "sector": "자유소비재"},
    {"code": "000220", "name": "덕양산업", "sector": "자유소비재"},
    {"code": "008770", "name": "호텔신라", "sector": "자유소비재"},
    {"code": "023530", "name": "롯데쇼핑", "sector": "자유소비재"},
    {"code": "139480", "name": "이마트", "sector": "자유소비재"},
    {"code": "004170", "name": "신세계", "sector": "자유소비재"},
    {"code": "007070", "name": "GS리테일", "sector": "자유소비재"},
    {"code": "021240", "name": "코웨이", "sector": "자유소비재"},
    {"code": "009240", "name": "한샘", "sector": "자유소비재"},
    {"code": "001740", "name": "SK네트웍스", "sector": "자유소비재"},
    {"code": "069960", "name": "현대백화점", "sector": "자유소비재"},
    {"code": "020000", "name": "한섬", "sector": "자유소비재"},
    {"code": "192820", "name": "코스맥스", "sector": "자유소비재"},
    {"code": "111770", "name": "영원무역", "sector": "자유소비재"},
    {"code": "093240", "name": "형지엘리트", "sector": "자유소비재"},
    {"code": "001380", "name": "SG세계물산", "sector": "자유소비재"},
    {"code": "004250", "name": "한세예스24홀딩스", "sector": "자유소비재"},
    {"code": "105630", "name": "한세실업", "sector": "자유소비재"},
    {"code": "001070", "name": "대한방직", "sector": "자유소비재"},
    {"code": "002140", "name": "고려산업", "sector": "자유소비재"},
    {"code": "005870", "name": "휴니드", "sector": "자유소비재"},
    {"code": "004870", "name": "티웨이홀딩스", "sector": "자유소비재"},
    {"code": "033530", "name": "세종공업", "sector": "자유소비재"},
    {"code": "009900", "name": "명신산업", "sector": "자유소비재"},
    {"code": "204320", "name": "만도", "sector": "자유소비재"},
    {"code": "001630", "name": "종근당홀딩스", "sector": "자유소비재"},
    {"code": "009540", "name": "HD한국조선해양", "sector": "산업재"},
    {"code": "010140", "name": "삼성중공업", "sector": "산업재"},
    {"code": "042660", "name": "한화오션", "sector": "산업재"},
    {"code": "329180", "name": "HD현대중공업", "sector": "산업재"},
    {"code": "012450", "name": "한화에어로스페이스", "sector": "산업재"},
    {"code": "079550", "name": "LIG넥스원", "sector": "산업재"},
    {"code": "064350", "name": "현대로템", "sector": "산업재"},
    {"code": "000880", "name": "한화", "sector": "산업재"},
    {"code": "028260", "name": "삼성물산", "sector": "산업재"},
    {"code": "047050", "name": "포스코인터내셔널", "sector": "산업재"},
    {"code": "086280", "name": "현대글로비스", "sector": "산업재"},
    {"code": "011200", "name": "HMM", "sector": "산업재"},
    {"code": "003490", "name": "대한항공", "sector": "산업재"},
    {"code": "020560", "name": "아시아나항공", "sector": "산업재"},
    {"code": "000120", "name": "CJ대한통운", "sector": "산업재"},
    {"code": "267250", "name": "HD현대일렉트릭", "sector": "산업재"},
    {"code": "010120", "name": "LS ELECTRIC", "sector": "산업재"},
    {"code": "034020", "name": "두산에너빌리티", "sector": "산업재"},
    {"code": "241560", "name": "두산밥캣", "sector": "산업재"},
    {"code": "000150", "name": "두산", "sector": "산업재"},
    {"code": "000720", "name": "현대건설", "sector": "산업재"},
    {"code": "006360", "name": "GS건설", "sector": "산업재"},
    {"code": "047040", "name": "대우건설", "sector": "산업재"},
    {"code": "375500", "name": "DL이앤씨", "sector": "산업재"},
    {"code": "028050", "name": "삼성E&A", "sector": "산업재"},
    {"code": "001440", "name": "대한전선", "sector": "산업재"},
    {"code": "017800", "name": "현대엘리베이", "sector": "산업재"},
    {"code": "002320", "name": "한진", "sector": "산업재"},
    {"code": "005880", "name": "대한해운", "sector": "산업재"},
    {"code": "010620", "name": "현대미포조선", "sector": "산업재"},
    {"code": "010130", "name": "LS", "sector": "산업재"},
    {"code": "271560", "name": "오리온홀딩스", "sector": "산업재"},
    {"code": "180640", "name": "한진칼", "sector": "산업재"},
    {"code": "003010", "name": "혜인", "sector": "산업재"},
    {"code": "096530", "name": "씨에스윈드", "sector": "산업재"},
    {"code": "011000", "name": "진에어", "sector": "산업재"},
    {"code": "089590", "name": "제주항공", "sector": "산업재"},
    {"code": "026960", "name": "동서", "sector": "산업재"},
    {"code": "033780", "name": "KT&G", "sector": "산업재"},
    {"code": "005960", "name": "동부건설", "sector": "산업재"},
    {"code": "002150", "name": "도화엔지니어링", "sector": "산업재"},
    {"code": "013580", "name": "계룡건설", "sector": "산업재"},
    {"code": "006400", "name": "삼성SDI우", "sector": "산업재"},
    {"code": "373220", "name": "LG에너지솔루션", "sector": "소재"},
    {"code": "051910", "name": "LG화학", "sector": "소재"},
    {"code": "003670", "name": "포스코퓨처엠", "sector": "소재"},
    {"code": "005490", "name": "POSCO홀딩스", "sector": "소재"},
    {"code": "004020", "name": "현대제철", "sector": "소재"},
    {"code": "011170", "name": "롯데케미칼", "sector": "소재"},
    {"code": "011780", "name": "금호석유", "sector": "소재"},
    {"code": "009830", "name": "한화솔루션", "sector": "소재"},
    {"code": "011790", "name": "SKC", "sector": "소재"},
    {"code": "004000", "name": "롯데정밀화학", "sector": "소재"},
    {"code": "005420", "name": "코스모화학", "sector": "소재"},
    {"code": "005070", "name": "코스모신소재", "sector": "소재"},
    {"code": "061970", "name": "엘앤에프", "sector": "소재"},
    {"code": "361610", "name": "SK아이이테크놀로지", "sector": "소재"},
    {"code": "010060", "name": "OCI홀딩스", "sector": "소재"},
    {"code": "285130", "name": "SK케미칼", "sector": "소재"},
    {"code": "002380", "name": "KCC", "sector": "소재"},
    {"code": "003410", "name": "쌍용C&E", "sector": "소재"},
    {"code": "004980", "name": "성신양회", "sector": "소재"},
    {"code": "016380", "name": "KG스틸", "sector": "소재"},
    {"code": "005010", "name": "휴스틸", "sector": "소재"},
    {"code": "002310", "name": "태광산업", "sector": "소재"},
    {"code": "002350", "name": "KG케미칼", "sector": "소재"},
    {"code": "002840", "name": "미원상사", "sector": "소재"},
    {"code": "006110", "name": "삼아알미늄", "sector": "소재"},
    {"code": "001420", "name": "태원물산", "sector": "소재"},
    {"code": "001550", "name": "조비", "sector": "소재"},
    {"code": "001520", "name": "동양", "sector": "소재"},
    {"code": "003080", "name": "성안", "sector": "소재"},
    {"code": "003650", "name": "미창석유", "sector": "소재"},
    {"code": "001390", "name": "KG케미칼우", "sector": "소재"},
    {"code": "000210", "name": "DL", "sector": "소재"},
    {"code": "003520", "name": "영진약품우", "sector": "소재"},
    {"code": "001120", "name": "LX하우시스", "sector": "소재"},
    {"code": "000990", "name": "DB하이텍", "sector": "소재"},
    {"code": "010690", "name": "화신", "sector": "소재"},
    {"code": "035420", "name": "NAVER", "sector": "커뮤니케이션"},
    {"code": "035720", "name": "카카오", "sector": "커뮤니케이션"},
    {"code": "017670", "name": "SK텔레콤", "sector": "커뮤니케이션"},
    {"code": "030200", "name": "KT", "sector": "커뮤니케이션"},
    {"code": "032640", "name": "LG유플러스", "sector": "커뮤니케이션"},
    {"code": "259960", "name": "크래프톤", "sector": "커뮤니케이션"},
    {"code": "036570", "name": "엔씨소프트", "sector": "커뮤니케이션"},
    {"code": "251270", "name": "넷마블", "sector": "커뮤니케이션"},
    {"code": "352820", "name": "하이브", "sector": "커뮤니케이션"},
    {"code": "138040", "name": "메리츠금융", "sector": "커뮤니케이션"},
    {"code": "033630", "name": "SK브로드밴드", "sector": "커뮤니케이션"},
    {"code": "036580", "name": "엔씨소프트우", "sector": "커뮤니케이션"},
    {"code": "051900", "name": "LG생활건강", "sector": "필수소비재"},
    {"code": "090430", "name": "아모레퍼시픽", "sector": "필수소비재"},
    {"code": "002790", "name": "아모레G", "sector": "필수소비재"},
    {"code": "161890", "name": "한국콜마", "sector": "필수소비재"},
    {"code": "097950", "name": "CJ제일제당", "sector": "필수소비재"},
    {"code": "004370", "name": "농심", "sector": "필수소비재"},
    {"code": "003230", "name": "삼양식품", "sector": "필수소비재"},
    {"code": "007310", "name": "오뚜기", "sector": "필수소비재"},
    {"code": "005300", "name": "롯데칠성", "sector": "필수소비재"},
    {"code": "000080", "name": "하이트진로", "sector": "필수소비재"},
    {"code": "001680", "name": "대상", "sector": "필수소비재"},
    {"code": "005180", "name": "빙그레", "sector": "필수소비재"},
    {"code": "003920", "name": "남양유업", "sector": "필수소비재"},
    {"code": "001150", "name": "삼양사", "sector": "필수소비재"},
    {"code": "002270", "name": "롯데푸드", "sector": "필수소비재"},
    {"code": "005440", "name": "현대그린푸드", "sector": "필수소비재"},
    {"code": "001110", "name": "CJ씨푸드", "sector": "필수소비재"},
    {"code": "004410", "name": "서울식품", "sector": "필수소비재"},
    {"code": "005610", "name": "SPC삼립", "sector": "필수소비재"},
    {"code": "007280", "name": "한국수출포장", "sector": "필수소비재"},
    {"code": "002810", "name": "삼영무역", "sector": "필수소비재"},
    {"code": "010950", "name": "S-Oil", "sector": "에너지/유틸리티"},
    {"code": "096770", "name": "SK이노베이션", "sector": "에너지/유틸리티"},
    {"code": "015760", "name": "한국전력", "sector": "에너지/유틸리티"},
    {"code": "036460", "name": "한국가스공사", "sector": "에너지/유틸리티"},
    {"code": "003550", "name": "LG", "sector": "지주사"},
    {"code": "034730", "name": "SK", "sector": "지주사"},
    {"code": "001040", "name": "CJ", "sector": "지주사"},
    {"code": "004800", "name": "효성", "sector": "지주사"},
    {"code": "078930", "name": "GS", "sector": "지주사"},
    {"code": "004990", "name": "롯데지주", "sector": "지주사"}
]

# ==========================================
# 3. 데이터 수집 및 지표 연산 함수
# ==========================================

def fetch_naver_daily_candles(stk_code, count=120):
    url = f"https://fchart.stock.naver.com/sise.nhn?symbol={stk_code}&timeframe=day&count={count}&requestType=0"
    headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X)'}
    
    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                xml_data = res.content.decode('euc-kr', errors='ignore')
                root = ET.fromstring(xml_data)
                data_list = []
                for item in root.findall('.//item'):
                    val = item.get('data')
                    if val:
                        parts = val.split('|')
                        if len(parts) >= 6:
                            data_list.append({
                                'open': float(parts[1]),
                                'high': float(parts[2]),
                                'low': float(parts[3]),
                                'close': float(parts[4]),
                                'volume': float(parts[5])
                            })
                df = pd.DataFrame(data_list)
                return df
        except Exception:
            time.sleep(0.1 * (attempt + 1))
    return pd.DataFrame()

# Donchian Distance (20일)
def calc_donchian_dist(df, period=20):
    if len(df) < period:
        return 0.0
    sub = df.tail(period)
    last_close = sub['close'].iloc[-1]
    max_high = sub['high'].max()
    if max_high == 0:
        return 0.0
    return (max_high - last_close) / max_high

# Wilder's RSI (9일)
def calc_wilder_rsi(df, period=9):
    if len(df) <= period:
        return 50.0
    delta = df['close'].diff().dropna().values
    gains = np.where(delta > 0, delta, 0.0)
    losses = np.where(delta < 0, -delta, 0.0)
    
    if len(gains) < period:
        return 50.0
        
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))

# Volume Z-Score (96일)
def calc_vol_zscore(df, period=96):
    ct = min(len(df), period)
    if ct <= 5:
        return 0.0
    sub_vol = df['volume'].tail(ct)
    last_vol = sub_vol.iloc[-1]
    m = sub_vol.mean()
    std = sub_vol.std(ddof=1)
    if std == 0 or np.isnan(std):
        return 0.0
    return (last_vol - m) / std

# 횡단면 랭크 연산 (Cross-Sectional Rank)
def calculate_cross_sectional_ranks(metrics_list):
    if len(metrics_list) < 3:
        return pd.DataFrame()
        
    df = pd.DataFrame(metrics_list)
    
    # 각 지표별 오름차순 정렬 랭크 (0부터 N-1까지)
    df['r1'] = df['donch_dist'].rank(ascending=True, method='min') - 1
    df['r2'] = df['rsi9'].rank(ascending=True, method='min') - 1
    df['r3'] = df['vol_z'].rank(ascending=True, method='min') - 1
    
    n_denom = max(1, len(df) - 1)
    df['rank_percentile'] = (df['r1'] + df['r2'] + df['r3']) / (3.0 * n_denom)
    
    df = df.sort_values('rank_percentile', ascending=False).reset_index(drop=True)
    return df

# ==========================================
# 4. Streamlit 웹 화면 UI 구현 (보안 적용)
# ==========================================

st.title("📈 Track X Dashboard")
st.caption("KOSPI Universe 횡단면 랭킹 스카웃 엔진")

st.markdown("---")

if st.button("🚀 KRX 219개 랭킹 탐색 시작", use_container_width=True):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    candidates = []
    total_count = len(KOSPI_219_UNIVERSE)
    
    for idx, item in enumerate(KOSPI_219_UNIVERSE):
        status_text.text(f"[{idx+1}/{total_count}] {item['name']} 분석 중...")
        progress_bar.progress((idx + 1) / total_count)
        
        df_candles = fetch_naver_daily_candles(item['code'])
        if len(df_candles) > 20:
            donch_dist = calc_donchian_dist(df_candles)
            rsi9 = calc_wilder_rsi(df_candles)
            vol_z = calc_vol_zscore(df_candles)
            last_close = df_candles['close'].iloc[-1]
            
            candidates.append({
                'code': item['code'],
                'name': item['name'],
                'sector': item['sector'],
                'close_price': int(last_close),
                'donch_dist': donch_dist,
                'rsi9': rsi9,
                'vol_z': vol_z
            })
            
    status_text.text("📊 횡단면 랭킹 최종 연산 중...")
    df_ranked = calculate_cross_sectional_ranks(candidates)
    
    status_text.success(f"✅ 총 {len(df_ranked)}개 종목 랭킹 분석 완료!")
    progress_bar.empty()
    
    # ⭐ 결과 포맷팅 및 출력 (지표 수치 완전 감춤 / 보안 강화)
    df_display = df_ranked[['rank_percentile', 'name', 'code', 'sector', 'close_price']].copy()
    
    df_display.columns = ['Rank Percentile', '종목명', '종목코드', '섹터', '현재가(원)']
    df_display['Rank Percentile'] = df_display['Rank Percentile'].apply(lambda x: f"{x:.4f}")
    df_display['현재가(원)'] = df_display['현재가(원)'].apply(lambda x: f"{x:,}")
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
