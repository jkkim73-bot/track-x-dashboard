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
    page_title="Track X v1 Dashboard",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# 2. KOSPI 389 유니버스 데이터 정의 (텍스트 파싱)
# ==========================================
RAW_UNIVERSE_DATA = """
005930|삼성전자|정보기술
000660|SK하이닉스|정보기술
005935|삼성전자우|정보기술
009150|삼성전기|정보기술
066570|LG전자|정보기술
034220|LG디스플레이|정보기술
011070|LG이노텍|정보기술
018260|삼성SDS|정보기술
042700|한미반도체|정보기술
108320|LX세미콘|정보기술
004130|대덕전자|정보기술
032390|다우기술|정보기술
036810|DI동일|정보기술
207940|삼성바이오로직스|헬스케어
068270|셀트리온|헬스케어
000100|유한양행|헬스케어
128940|한미약품|헬스케어
006280|GC녹십자|헬스케어
185750|종근당|헬스케어
214300|대웅제약|헬스케어
302440|SK바이오사이언스|헬스케어
326030|SK바이오팜|헬스케어
008930|한미사이언스|헬스케어
003090|대웅|헬스케어
102940|코오롱생명과학|헬스케어
001060|JW중외제약|헬스케어
003000|부광약품|헬스케어
003850|보령|헬스케어
005250|녹십자홀딩스|헬스케어
000670|영진약품|헬스케어
000180|성창기업지주|헬스케어
020150|일진머티리얼즈|헬스케어
105560|KB금융|금융
055550|신한지주|금융
086790|하나금융지주|금융
316140|우리금융지주|금융
000060|메리츠금융지주|금융
323410|카카오뱅크|금융
377300|카카오페이|금융
024110|기업은행|금융
032830|삼성생명|금융
000810|삼성화재|금융
005830|DB손해보험|금융
001450|현대해상|금융
088350|한화생명|금융
000370|한화손해보험|금융
006800|미래에셋증권|금융
016360|삼성증권|금융
005940|NH투자증권|금융
071050|한국금융지주|금융
039490|키움증권|금융
003540|대신증권|금융
003530|한화투자증권|금융
001720|신영증권|금융
001750|한양증권|금융
003470|유안타증권|금융
030210|다올투자증권|금융
001270|부국증권|금융
021050|서원|금융
003620|KG모빌리티|금융
402340|SK스퀘어|금융
000540|흥국화재|금융
000050|경방|금융
001200|유진투자증권|금융
001500|조선내화|금융
005380|현대차|자유소비재
000270|기아|자유소비재
012330|현대모비스|자유소비재
018880|한온시스템|자유소비재
011210|현대위아|자유소비재
005850|에스엘|자유소비재
000240|한국앤컴퍼니|자유소비재
000220|덕양산업|자유소비재
008770|호텔신라|자유소비재
023530|롯데쇼핑|자유소비재
139480|이마트|자유소비재
004170|신세계|자유소비재
007070|GS리테일|자유소비재
021240|코웨이|자유소비재
009240|한샘|자유소비재
001740|SK네트웍스|자유소비재
069960|현대백화점|자유소비재
020000|한섬|자유소비재
192820|코스맥스|자유소비재
111770|영원무역|자유소비재
093240|형지엘리트|자유소비재
001380|SG세계물산|자유소비재
004250|한세예스24홀딩스|자유소비재
105630|한세실업|자유소비재
001070|대한방직|자유소비재
002140|고려산업|자유소비재
005870|휴니드|자유소비재
004870|티웨이홀딩스|자유소비재
033530|세종공업|자유소비재
009900|명신산업|자유소비재
204320|만도|자유소비재
001630|종근당홀딩스|자유소비재
009540|HD한국조선해양|산업재
010140|삼성중공업|산업재
042660|한화오션|산업재
329180|HD현대중공업|산업재
012450|한화에어로스페이스|산업재
079550|LIG넥스원|산업재
064350|현대로템|산업재
000880|한화|산업재
028260|삼성물산|산업재
047050|포스코인터내셔널|산업재
086280|현대글로비스|산업재
011200|HMM|산업재
003490|대한항공|산업재
020560|아시아나항공|산업재
000120|CJ대한통운|산업재
267250|HD현대일렉트릭|산업재
010120|LS ELECTRIC|산업재
034020|두산에너빌리티|산업재
241560|두산밥캣|산업재
000150|두산|산업재
000720|현대건설|산업재
006360|GS건설|산업재
047040|대우건설|산업재
375500|DL이앤씨|산업재
028050|삼성E&A|산업재
001440|대한전선|산업재
017800|현대엘리베이|산업재
002320|한진|산업재
005880|대한해운|산업재
010620|현대미포조선|산업재
010130|LS|산업재
271560|오리온홀딩스|산업재
180640|한진칼|산업재
003010|혜인|산업재
096530|씨에스윈드|산업재
011000|진에어|산업재
089590|제주항공|산업재
026960|동서|산업재
033780|KT&G|산업재
005960|동부건설|산업재
002150|도화엔지니어링|산업재
013580|계룡건설|산업재
006400|삼성SDI우|산업재
373220|LG에너지솔루션|소재
051910|LG화학|소재
003670|포스코퓨처엠|소재
005490|POSCO홀딩스|소재
004020|현대제철|소재
011170|롯데케미칼|소재
011780|금호석유|소재
009830|한화솔루션|소재
011790|SKC|소재
004000|롯데정밀화학|소재
005420|코스모화학|소재
005070|코스모신소재|소재
061970|엘앤에프|소재
361610|SK아이이테크놀로지|소재
010060|OCI홀딩스|소재
285130|SK케미칼|소재
002380|KCC|소재
003410|쌍용C&E|소재
004980|성신양회|소재
016380|KG스틸|소재
005010|휴스틸|소재
002310|태광산업|소재
002350|KG케미칼|소재
002840|미원상사|소재
006110|삼아알미늄|소재
001420|태원물산|소재
001550|조비|소재
001520|동양|소재
003080|성안|소재
003650|미창석유|소재
001390|KG케미칼우|소재
000210|DL|소재
003520|영진약품우|소재
001120|LX하우시스|소재
000990|DB하이텍|소재
010690|화신|소재
035420|NAVER|커뮤니케이션
035720|카카오|커뮤니케이션
017670|SK텔레콤|커뮤니케이션
030200|KT|커뮤니케이션
032640|LG유플러스|커뮤니케이션
259960|크래프톤|커뮤니케이션
036570|엔씨소프트|커뮤니케이션
251270|넷마블|커뮤니케이션
352820|하이브|커뮤니케이션
138040|메리츠금융|커뮤니케이션
033630|SK브로드밴드|커뮤니케이션
036580|엔씨소프트우|커뮤니케이션
051900|LG생활건강|필수소비재
090430|아모레퍼시픽|필수소비재
002790|아모레G|필수소비재
161890|한국콜마|필수소비재
097950|CJ제일제당|필수소비재
004370|농심|필수소비재
003230|삼양식품|필수소비재
007310|오뚜기|필수소비재
005300|롯데칠성|필수소비재
000080|하이트진로|필수소비재
001680|대상|필수소비재
005180|빙그레|필수소비재
003920|남양유업|필수소비재
001150|삼양사|필수소비재
002270|롯데푸드|필수소비재
005440|현대그린푸드|필수소비재
001110|CJ씨푸드|필수소비재
004410|서울식품|필수소비재
005610|SPC삼립|필수소비재
007280|한국수출포장|필수소비재
002810|삼영무역|필수소비재
010950|S-Oil|에너지/유틸리티
096770|SK이노베이션|에너지/유틸리티
015760|한국전력|에너지/유틸리티
036460|한국가스공사|에너지/유틸리티
003550|LG|지주사
034730|SK|지주사
001040|CJ|지주사
004800|효성|지주사
078930|GS|지주사
004990|롯데지주|지주사
298040|효성중공업|코스피
267260|HD현대일렉트릭|코스피
278470|에이피알|코스피
272210|한화시스템|코스피
047810|한국항공우주|코스피
307950|현대오토에버|코스피
443060|HD현대마린솔루션|코스피
006260|LS|코스피
007660|이수페타시스|코스피
161390|한국타이어앤테크놀로지|코스피
064400|LG씨엔에스|코스피
005387|현대차2우B|코스피
267270|HD건설기계|코스피
062040|산일전기|코스피
000500|가온전선|코스피
066970|엘앤에프|코스피
029780|삼성카드|코스피
175330|JB금융지주|코스피
353200|대덕전자|코스피
088980|맥쿼리인프라|코스피
138930|BNK금융지주|코스피
052690|한전기술|코스피
454910|두산로보틱스|코스피
005385|현대차우|코스피
082740|한화엔진|코스피
103590|일진전기|코스피
009420|한올바이오파마|코스피
022100|포스코DX|코스피
012750|에스원|코스피
035250|강원랜드|코스피
085620|미래에셋생명|코스피
031210|서울보증보험|코스피
028670|팬오션|코스피
336260|두산퓨얼셀|코스피
139130|iM금융지주|코스피
483650|달바글로벌|코스피
007340|DN오토모티브|코스피
450080|에코프로머티|코스피
003690|코리안리|코스피
383220|F&F|코스피
282330|BGF리테일|코스피
489790|한화비전|코스피
103140|풍산|코스피
279570|케이뱅크|코스피
181710|NHN|코스피
030000|제일기획|코스피
009970|영원무역홀딩스|코스피
081660|미스토홀딩스|코스피
014680|한솔케미칼|코스피
018670|SK가스|코스피
051600|한전KPS|코스피
073240|금호타이어|코스피
112610|씨에스윈드|코스피
457190|이수스페셜티케미컬|코스피
462870|시프트업|코스피
475150|SK이터닉스|코스피
439260|대한조선|코스피
071970|HD현대마린엔진|코스피
000155|두산우|코스피
089860|롯데렌탈|코스피
023590|다우기술|코스피
006040|동원산업|코스피
120110|코오롱인더|코스피
001800|오리온홀딩스|코스피
097230|HJ중공업|코스피
001430|세아베스틸지주|코스피
294870|IPARK현대산업개발|코스피
322000|HD현대에너지솔루션|코스피
298020|효성티앤씨|코스피
069620|대웅제약|코스피
009155|삼성전기우|코스피
007810|코리아써키트|코스피
229640|LS에코에너지|코스피
012630|HDC|코스피
280360|롯데웰푸드|코스피
093370|후성|코스피
281820|케이씨텍|코스피
000815|삼성화재우|코스피
017960|한국카본|코스피
082640|동양생명|코스피
415640|KB발해인프라|코스피
066575|LG전자우|코스피
192080|더블유게임즈|코스피
300720|한일시멘트|코스피
030610|교보증권|코스피
001820|삼화콘덴서|코스피
006340|대원전선|코스피
032350|롯데관광개발|코스피
003240|태광산업|코스피
003570|SNT다이내믹스|코스피
077970|STX엔진|코스피
192400|쿠쿠홀딩스|코스피
051915|LG화학우|코스피
030190|NICE평가정보|코스피
034230|파라다이스|코스피
009450|경동나비엔|코스피
004490|세방전지|코스피
195870|해성디에스|코스피
079160|CJ CGV|코스피
005090|SGC에너지|코스피
006120|SK디스커버리|코스피
071055|한국금융지주우|코스피
071320|지역난방공사|코스피
100090|SK오션플랜트|코스피
499790|GS피앤엘|코스피
298050|HS효성첨단소재|코스피
137310|에스디바이오센서|코스피
214320|이노션|코스피
036530|SNT홀딩스|코스피
456040|OCI|코스피
003160|디아이|코스피
064960|SNT모티브|코스피
093050|LF|코스피
317450|명인제약|코스피
005690|파미셀|코스피
100840|SNT에너지|코스피
017940|E1|코스피
069260|TKG휴켐스|코스피
268280|미원에스씨|코스피
000400|롯데손해보험|코스피
094800|맵스리얼티|코스피
002960|한국쉘석유|코스피
014820|동원시스템즈|코스피
000640|동아쏘시오홀딩스|코스피
248070|솔루엠|코스피
033240|자화전자|코스피
002990|금호건설|코스피
001570|금양|코스피
383800|LX홀딩스|코스피
006650|대한유화|코스피
006380|카프로|코스피
453340|현대그린푸드|코스피
075580|세진중공업|코스피
079900|전진건설로봇|코스피
001510|SK증권|코스피
114090|GKL|코스피
003300|한일홀딩스|코스피
001530|DI동일|코스피
090460|비에이치|코스피
058650|세아홀딩스|코스피
178920|PI첨단소재|코스피
007700|F&F홀딩스|코스피
025540|한국단자|코스피
005810|풍산홀딩스|코스피
336370|솔루스첨단소재|코스피
284740|쿠쿠홈시스|코스피
019170|신풍제약|코스피
460860|동국제강|코스피
039130|하나투어|코스피
009410|태영건설|코스피
008060|대덕|코스피
034310|NICE|코스피
161000|애경케미칼|코스피
003545|대신증권우|코스피
090435|아모레퍼시픽우|코스피
010780|아이에스동서|코스피
377740|바이오노트|코스피
004690|삼천리|코스피
145990|삼양사|코스피
002240|고려제강|코스피
000070|삼양홀딩스|코스피
249420|일동제약|코스피
029460|케이씨|코스피
014830|유니드|코스피
002030|아세아|코스피
072710|농심홀딩스|코스피
092230|KPX홀딩스|코스피
005389|현대차3우B|코스피
005945|NH투자증권우|코스피
317400|자이에스앤디|코스피
"""

def load_universe_389():
    items = []
    for line in RAW_UNIVERSE_DATA.strip().split('\n'):
        parts = line.strip().split('|')
        if len(parts) >= 3:
            items.append({
                'code': parts[0],
                'name': parts[1],
                'sector': parts[2]
            })
    return items

KOSPI_389_UNIVERSE = load_universe_389()

# ==========================================
# 3. v1 데이터 수집 및 지표 연산 함수
# ==========================================

def fetch_naver_daily_candles(stk_code, count=900):
    url = f"https://fchart.stock.naver.com/sise.nhn?symbol={stk_code}&timeframe=day&count={count}&requestType=0"
    headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X)'}
    
    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code == 200:
                xml_data = res.content.decode('euc-kr', errors='ignore')
                root = ET.fromstring(xml_data)
                data_list = []
                for item in root.findall('.//item'):
                    val = item.get('data')
                    if val:
                        parts = val.split('|')
                        if len(parts) >= 6:
                            d, o, h, l, c, v = parts[0], float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])
                            if v > 0 and (o != 0 or h != 0 or l != 0 or c != 0):
                                data_list.append({
                                    'date': d, 'open': o, 'high': h, 'low': l, 'close': c, 'volume': v
                                })
                df = pd.DataFrame(data_list)
                if not df.empty:
                    return df
        except Exception:
            time.sleep(0.1 * (attempt + 1))
    return pd.DataFrame()

# v1: Donchian Distance (20일)
def calc_donchian_dist(df, period=20):
    if len(df) < period:
        return 0.0
    sub = df.tail(period)
    last_close = sub['close'].iloc[-1]
    max_high = sub['high'].max()
    if max_high == 0:
        return 0.0
    return (max_high - last_close) / max_high

# v1: Wilder's RSI (9일)
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
        avg_gain = (avg_gain * (period - 1.0) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1.0) + losses[i]) / period
        
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))

# v1: Volume Z-Score (96일)
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

# v1: 횡단면 랭크 연산 (Donchian 부호 반전 포함)
def calculate_v1_ranks(metrics_list):
    if len(metrics_list) < 3:
        return pd.DataFrame()
        
    df = pd.DataFrame(metrics_list)
    
    # Donchian은 작을수록 신고가 근접이므로 음수(-) 처리하여 오름차순 랭킹
    df['r1'] = (-df['donch_dist']).rank(ascending=True, method='min') - 1
    df['r2'] = df['rsi9'].rank(ascending=True, method='min') - 1
    df['r3'] = df['vol_z'].rank(ascending=True, method='min') - 1
    
    n_denom = max(1, len(df) - 1)
    df['rank_percentile'] = (df['r1'] + df['r2'] + df['r3']) / (3.0 * n_denom)
    
    df = df.sort_values('rank_percentile', ascending=False).reset_index(drop=True)
    return df

# ==========================================
# 4. Streamlit 웹 화면 UI
# ==========================================

st.title("📈 Track X v1 Dashboard (389 Universe)")
st.caption("KOSPI 389 유니버스")

st.markdown("---")

col1, col2 = st.columns([2, 1])
with col1:
    search_query = st.text_input("🔍 종목명 / 코드 / 섹터 검색", placeholder="예: 삼성전자, 005930, 정보기술")

if st.button("🚀 KOSPI 389개 v1 랭킹 탐색 시작", use_container_width=True):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    raw_candidates = []
    total_count = len(KOSPI_389_UNIVERSE)
    
    for idx, item in enumerate(KOSPI_389_UNIVERSE):
        status_text.text(f"[{idx+1}/{total_count}] {item['name']} 시세 수집 및 v1 팩터 계산 중...")
        progress_bar.progress((idx + 1) / total_count)
        
        df_candles = fetch_naver_daily_candles(item['code'], count=900)
        if len(df_candles) > 20:
            last_date = df_candles['date'].iloc[-1]
            donch_dist = calc_donchian_dist(df_candles)
            rsi9 = calc_wilder_rsi(df_candles)
            vol_z = calc_vol_zscore(df_candles)
            last_close = df_candles['close'].iloc[-1]
            
            raw_candidates.append({
                'code': item['code'],
                'name': item['name'],
                'sector': item['sector'],
                'date': last_date,
                'close_price': int(last_close),
                'donch_dist': donch_dist,
                'rsi9': rsi9,
                'vol_z': vol_z
            })
        time.sleep(0.35)
        
    status_text.text("📊 최신 영업일 기준 동기화 및 횡단면 랭킹 연산 중...")
    
    # 최빈값 날짜 동기화
    date_counts = {}
    for c in raw_candidates:
        d = c['date']
        date_counts[d] = date_counts.get(d, 0) + 1
        
    if date_counts:
        target_date = max(date_counts, key=date_counts.get)
        valid_candidates = [c for c in raw_candidates if c['date'] == target_date]
        valid_candidates.sort(key=lambda x: x['code'])
        
        df_ranked = calculate_v1_ranks(valid_candidates)
        st.session_state['v1_389_df'] = df_ranked
        st.session_state['target_date'] = target_date
        
        status_text.success(f"✅ 총 {len(df_ranked)}개 종목 분석 완료! (기준일자: {target_date})")
    else:
        status_text.error("❌ 시세 데이터를 수집하지 못했습니다.")
    progress_bar.empty()

# 결과 렌더링
if 'v1_389_df' in st.session_state and st.session_state['v1_389_df'] is not None:
    df_result = st.session_state['v1_389_df'].copy()
    
    if search_query:
        df_result = df_result[
            df_result['name'].str.contains(search_query) | 
            df_result['code'].str.contains(search_query) | 
            df_result['sector'].str.contains(search_query)
        ]
        
    df_display = df_result[['rank_percentile', 'name', 'code', 'sector', 'close_price', 'rsi9', 'donch_dist', 'vol_z']].copy()
    df_display.columns = ['Rank Percentile', '종목명', '종목코드', '섹터', '현재가(원)', 'RSI(9)', 'Donch Dist', 'Vol-Z(96)']
    
    df_display['Rank Percentile'] = df_display['Rank Percentile'].apply(lambda x: f"{x:.4f}")
    df_display['현재가(원)'] = df_display['현재가(원)'].apply(lambda x: f"{x:,}")
    df_display['RSI(9)'] = df_display['RSI(9)'].apply(lambda x: f"{x:.1f}")
    df_display['Donch Dist'] = df_display['Donch Dist'].apply(lambda x: f"{x:.2f}")
    df_display['Vol-Z(96)'] = df_display['Vol-Z(96)'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
