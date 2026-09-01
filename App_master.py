import streamlit as st
import pandas as pd
import numpy as np
import requests
import xml.etree.ElementTree as ET
import time

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="Track X Master Engine",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# 2. Universe Data (389개 고유 종목 정의)
# ==========================================
RAW_UNIVERSE_DATA = """
005930|삼성전자|정보기술|1
000660|SK하이닉스|정보기술|1
005935|삼성전자우|정보기술|1
009150|삼성전기|정보기술|1
066570|LG전자|정보기술|1
034220|LG디스플레이|정보기술|1
011070|LG이노텍|정보기술|1
018260|삼성SDS|정보기술|1
042700|한미반도체|정보기술|1
108320|LX세미콘|정보기술|1
004130|대덕전자|정보기술|1
032390|다우기술|정보기술|1
036810|DI동일|정보기술|1
207940|삼성바이오로직스|헬스케어|1
068270|셀트리온|헬스케어|1
000100|유한양행|헬스케어|1
128940|한미약품|헬스케어|1
006280|GC녹십자|헬스케어|1
185750|종근당|헬스케어|1
214300|대웅제약|헬스케어|1
302440|SK바이오사이언스|헬스케어|1
326030|SK바이오팜|헬스케어|1
008930|한미사이언스|헬스케어|1
003090|대웅|헬스케어|1
102940|코오롱생명과학|헬스케어|1
001060|JW중외제약|헬스케어|1
003000|부광약품|헬스케어|1
003850|보령|헬스케어|1
005250|녹십자홀딩스|헬스케어|1
000670|영진약품|헬스케어|1
000180|성창기업지주|헬스케어|1
020150|일진머티리얼즈|헬스케어|1
105560|KB금융|금융|1
055550|신한지주|금융|1
086790|하나금융지주|금융|1
316140|우리금융지주|금융|1
000060|메리츠금융지주|금융|1
323410|카카오뱅크|금융|1
377300|카카오페이|금융|1
024110|기업은행|금융|1
032830|삼성생명|금융|1
000810|삼성화재|금융|1
005830|DB손해보험|금융|1
001450|현대해상|금융|1
088350|한화생명|금융|1
000370|한화손해보험|금융|1
006800|미래에셋증권|금융|1
016360|삼성증권|금융|1
005940|NH투자증권|금융|1
071050|한국금융지주|금융|1
039490|키움증권|금융|1
003540|대신증권|금융|1
003530|한화투자증권|금융|1
001720|신영증권|금융|1
001750|한양증권|금융|1
003470|유안타증권|금융|1
030210|다올투자증권|금융|1
001270|부국증권|금융|1
021050|서원|금융|1
003620|KG모빌리티|금융|1
402340|SK스퀘어|금융|0
000540|흥국화재|금융|0
000050|경방|금융|0
001200|유진투자증권|금융|0
001500|조선내화|금융|0
005380|현대차|자유소비재|0
000270|기아|자유소비재|0
012330|현대모비스|자유소비재|0
018880|한온시스템|자유소비재|0
011210|현대위아|자유소비재|0
005850|에스엘|자유소비재|0
000240|한국앤컴퍼니|자유소비재|0
000220|덕양산업|자유소비재|0
008770|호텔신라|자유소비재|0
023530|롯데쇼핑|자유소비재|0
139480|이마트|자유소비재|0
004170|신세계|자유소비재|0
007070|GS리테일|자유소비재|0
021240|코웨이|자유소비재|0
009240|한샘|자유소비재|0
001740|SK네트웍스|자유소비재|0
069960|현대백화점|자유소비재|0
020000|한섬|자유소비재|0
192820|코스맥스|자유소비재|0
111770|영원무역|자유소비재|0
093240|형지엘리트|자유소비재|0
001380|SG세계물산|자유소비재|0
004250|한세예스24홀딩스|자유소비재|0
105630|한세실업|자유소비재|0
001070|대한방직|자유소비재|0
002140|고려산업|자유소비재|0
005870|휴니드|자유소비재|0
004870|티웨이홀딩스|자유소비재|0
033530|세종공업|자유소비재|0
009900|명신산업|자유소비재|0
204320|만도|자유소비재|0
001630|종근당홀딩스|자유소비재|0
009540|HD한국조선해양|산업재|0
010140|삼성중공업|산업재|0
042660|한화오션|산업재|0
329180|HD현대중공업|산업재|0
012450|한화에어로스페이스|산업재|0
079550|LIG넥스원|산업재|0
064350|현대로템|산업재|0
000880|한화|산업재|0
028260|삼성물산|산업재|0
047050|포스코인터내셔널|산업재|0
086280|현대글로비스|산업재|0
011200|HMM|산업재|0
003490|대한항공|산업재|0
020560|아시아나항공|산업재|0
000120|CJ대한통운|산업재|0
267250|HD현대일렉트릭|산업재|0
010120|LS ELECTRIC|산업재|0
034020|두산에너빌리티|산업재|0
241560|두산밥캣|산업재|0
000150|두산|산업재|0
000720|현대건설|산업재|0
006360|GS건설|산업재|0
047040|대우건설|산업재|0
375500|DL이앤씨|산업재|0
028050|삼성E&A|산업재|0
001440|대한전선|산업재|0
017800|현대엘리베이|산업재|0
002320|한진|산업재|0
005880|대한해운|산업재|0
010620|현대미포조선|산업재|0
010130|LS|산업재|0
271560|오리온홀딩스|산업재|0
180640|한진칼|산업재|0
003010|혜인|산업재|0
096530|씨에스윈드|산업재|0
011000|진에어|산업재|0
089590|제주항공|산업재|0
026960|동서|산업재|0
033780|KT&G|산업재|0
005960|동부건설|산업재|0
002150|도화엔지니어링|산업재|0
013580|계룡건설|산업재|0
006400|삼성SDI우|산업재|0
373220|LG에너지솔루션|소재|0
051910|LG화학|소재|0
003670|포스코퓨처엠|소재|0
005490|POSCO홀딩스|소재|0
004020|현대제철|소재|0
011170|롯데케미칼|소재|0
011780|금호석유|소재|0
009830|한화솔루션|소재|0
011790|SKC|소재|0
004000|롯데정밀화학|소재|0
005420|코스모화학|소재|0
005070|코스모신소재|소재|0
061970|엘앤에프|소재|0
361610|SK아이이테크놀로지|소재|0
010060|OCI홀딩스|소재|0
285130|SK케미칼|소재|0
002380|KCC|소재|0
003410|쌍용C&E|소재|0
004980|성신양회|소재|0
016380|KG스틸|소재|0
005010|휴스틸|소재|0
002310|태광산업|소재|0
002350|KG케미칼|소재|0
002840|미원상사|소재|0
006110|삼아알미늄|소재|0
001420|태원물산|소재|0
001550|조비|소재|0
001520|동양|소재|0
003080|성안|소재|0
003650|미창석유|소재|0
001390|KG케미칼우|소재|0
000210|DL|소재|0
003520|영진약품우|소재|0
001120|LX하우시스|소재|0
000990|DB하이텍|소재|0
010690|화신|소재|0
035420|NAVER|커뮤니케이션|0
035720|카카오|커뮤니케이션|0
017670|SK텔레콤|커뮤니케이션|0
030200|KT|커뮤니케이션|0
032640|LG유플러스|커뮤니케이션|0
259960|크래프톤|커뮤니케이션|0
036570|엔씨소프트|커뮤니케이션|0
251270|넷마블|커뮤니케이션|0
352820|하이브|커뮤니케이션|0
138040|메리츠금융|커뮤니케이션|0
033630|SK브로드밴드|커뮤니케이션|0
036580|엔씨소프트우|커뮤니케이션|0
051900|LG생활건강|필수소비재|0
090430|아모레퍼시픽|필수소비재|0
002790|아모레G|필수소비재|0
161890|한국콜마|필수소비재|0
097950|CJ제일제당|필수소비재|0
004370|농심|필수소비재|0
003230|삼양식품|필수소비재|0
007310|오뚜기|필수소비재|0
005300|롯데칠성|필수소비재|0
000080|하이트진로|필수소비재|0
001680|대상|필수소비재|0
005180|빙그레|필수소비재|0
003920|남양유업|필수소비재|0
001150|삼양사|필수소비재|0
002270|롯데푸드|필수소비재|0
005440|현대그린푸드|필수소비재|0
001110|CJ씨푸드|필수소비재|0
004410|서울식품|필수소비재|0
005610|SPC삼립|필수소비재|0
007280|한국수출포장|필수소비재|0
002810|삼영무역|필수소비재|0
010950|S-Oil|에너지/유틸리티|0
096770|SK이노베이션|에너지/유틸리티|0
015760|한국전력|에너지/유틸리티|0
036460|한국가스공사|에너지/유틸리티|0
003550|LG|지주사|0
034730|SK|지주사|0
001040|CJ|지주사|0
004800|효성|지주사|0
078930|GS|지주사|0
004990|롯데지주|지주사|0
298040|효성중공업|코스피|0
267260|HD현대일렉트릭|코스피|0
278470|에이피알|코스피|0
272210|한화시스템|코스피|0
047810|한국항공우주|코스피|0
307950|현대오토에버|코스피|0
443060|HD현대마린솔루션|코스피|0
006260|LS|코스피|0
007660|이수페타시스|코스피|0
161390|한국타이어앤테크놀로지|코스피|0
064400|LG씨엔에스|코스피|0
005387|현대차2우B|코스피|0
267270|HD건설기계|코스피|0
062040|산일전기|코스피|0
000500|가온전선|코스피|0
066970|엘앤에프|코스피|0
029780|삼성카드|코스피|0
175330|JB금융지주|코스피|0
353200|대덕전자|코스피|0
088980|맥쿼리인프라|코스피|0
138930|BNK금융지주|코스피|0
052690|한전기술|코스피|0
454910|두산로보틱스|코스피|0
005385|현대차우|코스피|0
082740|한화엔진|코스피|0
103590|일진전기|코스피|0
009420|한올바이오파마|코스피|0
022100|포스코DX|코스피|0
012750|에스원|코스피|0
035250|강원랜드|코스피|0
085620|미래에셋생명|코스피|0
031210|서울보증보험|코스피|0
028670|팬오션|코스피|0
336260|두산퓨얼셀|코스피|0
139130|iM금융지주|코스피|0
483650|달바글로벌|코스피|0
007340|DN오토모티브|코스피|0
450080|에코프로머티|코스피|0
003690|코리안리|코스피|0
383220|F&F|코스피|0
282330|BGF리테일|코스피|0
489790|한화비전|코스피|0
103140|풍산|코스피|0
279570|케이뱅크|코스피|0
181710|NHN|코스피|0
030000|제일기획|코스피|0
009970|영원무역홀딩스|코스피|0
081660|미스토홀딩스|코스피|0
014680|한솔케미칼|코스피|0
018670|SK가스|코스피|0
051600|한전KPS|코스피|0
073240|금호타이어|코스피|0
112610|씨에스윈드|코스피|0
457190|이수스페셜티케미컬|코스피|0
462870|시프트업|코스피|0
475150|SK이터닉스|코스피|0
439260|대한조선|코스피|0
071970|HD현대마린엔진|코스피|0
000155|두산우|코스피|0
089860|롯데렌탈|코스피|0
023590|다우기술|코스피|0
006040|동원산업|코스피|0
120110|코오롱인더|코스피|0
001800|오리온홀딩스|코스피|0
097230|HJ중공업|코스피|0
001430|세아베스틸지주|코스피|0
294870|IPARK현대산업개발|코스피|0
322000|HD현대에너지솔루션|코스피|0
298020|효성티앤씨|코스피|0
069620|대웅제약|코스피|0
009155|삼성전기우|코스피|0
007810|코리아써키트|코스피|0
229640|LS에코에너지|코스피|0
012630|HDC|코스피|0
280360|롯데웰푸드|코스피|0
093370|후성|코스피|0
281820|케이씨텍|코스피|0
000815|삼성화재우|코스피|0
017960|한국카본|코스피|0
082640|동양생명|코스피|0
415640|KB발해인프라|코스피|0
066575|LG전자우|코스피|0
192080|더블유게임즈|코스피|0
300720|한일시멘트|코스피|0
030610|교보증권|코스피|0
001820|삼화콘덴서|코스피|0
006340|대원전선|코스피|0
032350|롯데관광개발|코스피|0
003240|태광산업|코스피|0
003570|SNT다이내믹스|코스피|0
077970|STX엔진|코스피|0
192400|쿠쿠홀딩스|코스피|0
051915|LG화학우|코스피|0
030190|NICE평가정보|코스피|0
034230|파라다이스|코스피|0
009450|경동나비엔|코스피|0
004490|세방전지|코스피|0
195870|해성디에스|코스피|0
079160|CJ CGV|코스피|0
005090|SGC에너지|코스피|0
006120|SK디스커버리|코스피|0
071055|한국금융지주우|코스피|0
071320|지역난방공사|코스피|0
100090|SK오션플랜트|코스피|0
499790|GS피앤엘|코스피|0
298050|HS효성첨단소재|코스피|0
137310|에스디바이오센서|코스피|0
214320|이노션|코스피|0
036530|SNT홀딩스|코스피|0
456040|OCI|코스피|0
003160|디아이|코스피|0
064960|SNT모티브|코스피
093050|LF|코스피|0
317450|명인제약|코스피|0
005690|파미셀|코스피|0
100840|SNT에너지|코스피|0
017940|E1|코스피|0
069260|TKG휴켐스|코스피|0
268280|미원에스씨|코스피|0
000400|롯데손해보험|코스피|0
094800|맵스리얼티|코스피|0
002960|한국쉘석유|코스피|0
014820|동원시스템즈|코스피|0
000640|동아쏘시오홀딩스|코스피|0
248070|솔루엠|코스피|0
033240|자화전자|코스피|0
002990|금호건설|코스피|0
001570|금양|코스피|0
383800|LX홀딩스|코스피|0
006650|대한유화|코스피|0
006380|카프로|코스피|0
453340|현대그린푸드|코스피|0
075580|세진중공업|코스피|0
079900|전진건설로봇|코스피|0
001510|SK증권|코스피|0
114090|GKL|코스피|0
003300|한일홀딩스|코스피|0
001530|DI동일|코스피|0
090460|비에이치|코스피|0
058650|세아홀딩스|코스피|0
178920|PI첨단소재|코스피|0
007700|F&F홀딩스|코스피|0
025540|한국단자|코스피|0
005810|풍산홀딩스|코스피|0
336370|솔루스첨단소재|코스피|0
284740|쿠쿠홈시스|코스피|0
019170|신풍제약|코스피|0
460860|동국제강|코스피|0
039130|하나투어|코스피|0
009410|태영건설|코스피|0
008060|대덕|코스피|0
034310|NICE|코스피|0
161000|애경케미칼|코스피|0
003545|대신증권우|코스피|0
090435|아모레퍼시픽우|코스피|0
010780|아이에스동서|코스피|0
377740|바이오노트|코스피|0
004690|삼천리|코스피|0
145990|삼양사|코스피|0
002240|고려제강|코스피|0
000070|삼양홀딩스|코스피|0
249420|일동제약|코스피|0
029460|케이씨|코스피|0
014830|유니드|코스피|0
002030|아세아|코스피|0
072710|농심홀딩스|코스피|0
092230|KPX홀딩스|코스피|0
005389|현대차3우B|코스피|0
005945|NH투자증권우|코스피|0
317400|자이에스앤디|코스피|0
001230|동국홀딩스|코스피|0
001460|BYC|코스피|0
001790|대한제당|코스피|0
002020|코오롱|코스피|0
002200|수산중공업|코스피|0
002360|SH에너지화학|코스피|0
002710|동일방직|코스피|0
002820|SUN&L|코스피|0
003060|에이프로젠바이오로직스|코스피|0
003200|일지테크|코스피|0
003480|한진중공업홀딩스|코스피|0
003610|방림|코스피|0
003780|진흥기업|코스피|0
003830|대한화섬|코스피|0
003960|사조대림|코스피|0
004060|SG글로벌|코스피|0
004080|디와이|코스피|0
"""

def load_universe():
    seen = set()
    items = []
    for line in RAW_UNIVERSE_DATA.strip().split('\n'):
        parts = line.strip().split('|')
        if len(parts) >= 3:
            code = parts[0].strip()
            name = parts[1].strip()
            sector = parts[2].strip()
            is_large = (len(parts) >= 4 and parts[3].strip() == "1")
            if code and code not in seen:
                seen.add(code)
                items.append({'code': code, 'name': name, 'sector': sector, 'is_large': is_large})
                if len(items) == 389:
                    break
    return items

ALL_389_UNIVERSE = load_universe()
KOSPI_219_CODES = set([x['code'] for x in ALL_389_UNIVERSE[:219]])

# ==========================================
# 3. Indicator & Signal Engines
# ==========================================
def fetch_candles(code, count=900):
    url = f"https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count={count}&requestType=0"
    headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X)'}
    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code == 200:
                xml_data = res.content.decode('euc-kr', errors='ignore')
                root = ET.fromstring(xml_data)
                rows = []
                for item in root.findall('.//item'):
                    val = item.get('data')
                    if val:
                        p = val.split('|')
                        if len(p) >= 6:
                            d, o, h, l, c, v = p[0], float(p[1]), float(p[2]), float(p[3]), float(p[4]), float(p[5])
                            if v > 0 and (o != 0 or h != 0 or l != 0 or c != 0):
                                rows.append({'date': d, 'open': o, 'high': h, 'low': l, 'close': c, 'volume': v})
                df = pd.DataFrame(rows)
                if not df.empty:
                    return df
        except Exception:
            time.sleep(0.1 * (attempt + 1))
    return pd.DataFrame()

def calc_donch_series(df, period=20):
    highs = df['high'].values
    closes = df['close'].values
    res = np.zeros(len(df))
    for i in range(len(df)):
        hm = np.max(highs[max(0, i - period + 1):i + 1])
        res[i] = (1.0 - (closes[i] / hm)) if hm > 0 else 0.0
    return res

def calc_rsi9_series(df, period=9):
    closes = df['close'].values
    n = len(closes)
    rsi = np.full(n, 50.0)
    if n <= period:
        return rsi
    diff = np.diff(closes)
    gains = np.where(diff > 0, diff, 0.0)
    losses = np.where(diff < 0, -diff, 0.0)
    avg_g = np.mean(gains[:period])
    avg_l = np.mean(losses[:period])
    for i in range(period, len(gains)):
        avg_g = (avg_g * (period - 1) + gains[i]) / period
        avg_l = (avg_l * (period - 1) + losses[i]) / period
        rsi[i + 1] = 100.0 if avg_l == 0 else 100.0 - (100.0 / (1.0 + (avg_g / avg_l)))
    return rsi

def calc_volz60_series(df, period=60):
    vols = df['volume'].values
    res = np.zeros(len(df))
    for i in range(len(df)):
        slice_v = vols[max(0, i - period + 1):i + 1]
        if len(slice_v) < 15:
            continue
        m = np.mean(slice_v)
        sd = np.std(slice_v, ddof=1)
        res[i] = (vols[i] - m) / sd if sd > 1e-9 else 0.0
    return res

def calc_wr30_series(df, period=30):
    highs = df['high'].values
    lows = df['low'].values
    closes = df['close'].values
    res = np.full(len(df), -50.0)
    for i in range(len(df)):
        hm = np.max(highs[max(0, i - period + 1):i + 1])
        lm = np.min(lows[max(0, i - period + 1):i + 1])
        diff = hm - lm
        res[i] = ((hm - closes[i]) / diff) * -100.0 if diff > 1e-9 else -50.0
    return res

def calc_stoch_series(df, period=14):
    highs = df['high'].values
    lows = df['low'].values
    closes = df['close'].values
    fk = np.full(len(df), 50.0)
    for i in range(len(df)):
        hm = np.max(highs[max(0, i - period + 1):i + 1])
        lm = np.min(lows[max(0, i - period + 1):i + 1])
        diff = hm - lm
        fk[i] = ((closes[i] - lm) / diff) * 100.0 if diff > 1e-9 else 50.0
    sk = pd.Series(fk).rolling(3, min_periods=1).mean().values
    sd = pd.Series(sk).rolling(3, min_periods=1).mean().values
    return sk, sd

def calc_cci_series(df, period=20):
    tp = (df['high'] + df['low'] + df['close']) / 3.0
    ma = tp.rolling(period, min_periods=1).mean()
    mad = tp.rolling(period, min_periods=1).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    mad = mad.replace(0, 1e-5)
    cci = (tp - ma) / (0.015 * mad)
    cma = cci.rolling(14, min_periods=1).mean().values
    return cci.values, cma

def calc_iip_slope(df):
    if len(df) < 130:
        return 0.0
    diff = np.maximum(1e-5, df['high'] - df['low'])
    ii = ((2.0 * df['close'] - df['high'] - df['low']) / diff) * df['volume']
    iip = (ii.rolling(21, min_periods=1).sum() / np.maximum(1e-4, df['volume'].rolling(21, min_periods=1).sum())) * 100.0
    m = iip.rolling(120, min_periods=1).mean()
    s = iip.rolling(120, min_periods=1).std(ddof=1).replace(0, 1e-4)
    iipZ = (iip - m) / s
    return float(iipZ.iloc[-1] - iipZ.iloc[-4])

def calc_dlaf_slope(df):
    if len(df) < 105:
        return 0.0
    bias = 2.0 * (df['close'] - df['low']) / np.maximum(1e-5, df['high'] - df['low']) - 1.0
    v_ma = df['volume'].rolling(24, min_periods=1).mean().replace(0, 1e-5)
    vRatio = df['volume'] / v_ma
    c_std = df['close'].rolling(5, min_periods=1).std(ddof=1)
    atr = (df['high'] - df['low']).rolling(24, min_periods=1).mean().replace(0, 1e-5)
    vol_ratio = (c_std / atr).replace(0, 1e-5)
    rDlaf = -1.0 * bias * (vRatio / vol_ratio)
    m = rDlaf.rolling(96, min_periods=1).mean()
    s = rDlaf.rolling(96, min_periods=1).std(ddof=1).replace(0, 1e-5)
    dlafZ = (rDlaf - m) / s
    return float(dlafZ.iloc[-1] - dlafZ.iloc[-4])

# ==========================================
# 4. Global Scan Runner
# ==========================================
def run_master_scan():
    progress_bar = st.progress(0)
    status_text = st.empty()
    raw_results = []
    total = len(ALL_389_UNIVERSE)

    for idx, item in enumerate(ALL_389_UNIVERSE):
        status_text.text(f"[{idx+1}/{total}] {item['name']} ({item['code']}) 분석 중...")
        progress_bar.progress((idx + 1) / total)
        df = fetch_candles(item['code'], count=900)
        
        if len(df) >= 90:
            n = len(df) - 1
            pn = n - 1
            d = calc_donch_series(df)
            r = calc_rsi9_series(df)
            v = calc_volz60_series(df)
            wr = calc_wr30_series(df)
            sk, sd = calc_stoch_series(df)
            cci, cma = calc_cci_series(df)
            iip = calc_iip_slope(df)
            dlaf = calc_dlaf_slope(df)
            
            av = (iip <= 0.0) and (dlaf <= 0.0)
            sgc, wrok, ccok = False, False, False
            for j in range(max(0, n - 2), n + 1):
                if j > 0 and sk[j] > sd[j] and sk[j - 1] <= sd[j - 1]:
                    sgc = True
                if wr[j] >= -30.0:
                    wrok = True
                if cci[j] > cma[j]:
                    ccok = True
            
            x2 = 0
            if cci[n] > cma[n]: x2 += 1
            if wr[n] > -20.0: x2 += 1
            if sk[n] > sd[n] and sk[n] > 20.0: x2 += 1
            
            raw_results.append({
                'code': item['code'],
                'name': item['name'],
                'sector': item['sector'],
                'is_large': item['is_large'],
                'date': df['date'].iloc[-1],
                'close': int(df['close'].iloc[-1]),
                'd': d[n], 'r': r[n], 'v': v[n],
                'pd': d[pn], 'pr': r[pn], 'pv': v[pn],
                'wr': wr[n], 'sk': sk[n], 'sd': sd[n],
                'cci': cci[n], 'cma': cma[n],
                'iip': iip, 'dlaf': dlaf,
                'av': av, 'sc': (sgc and wrok and ccok), 'x2': x2
            })
        time.sleep(0.35)

    if not raw_results:
        status_text.error("❌ 시세 데이터를 수집하지 못했습니다.")
        return

    # 최신 영업일 동기화
    date_counts = {}
    for r in raw_results:
        date_counts[r['date']] = date_counts.get(r['date'], 0) + 1
    t_date = max(date_counts, key=date_counts.get)
    synced = [r for r in raw_results if r['date'] == t_date]
    synced.sort(key=lambda x: x['code'])
    synced_219 = [r for r in synced if r['code'] in KOSPI_219_CODES]

    # 1) v1 연산 (오름차순 rank - 1 기준)
    def compute_v1(data_list):
        df_sub = pd.DataFrame(data_list)
        if len(df_sub) < 3: return pd.DataFrame()
        df_sub['r1'] = df_sub['d'].rank(ascending=True, method='min') - 1
        df_sub['r2'] = df_sub['r'].rank(ascending=True, method='min') - 1
        df_sub['r3'] = df_sub['v'].rank(ascending=True, method='min') - 1
        denom = max(1, len(df_sub) - 1)
        df_sub['rank_percentile'] = (df_sub['r1'] + df_sub['r2'] + df_sub['r3']) / (3.0 * denom)
        df_sub = df_sub.sort_values('rank_percentile', ascending=False).reset_index(drop=True)
        df_sub['rank'] = range(1, len(df_sub) + 1)
        return df_sub

    # 2) v3 / v4 연산
    def compute_v3(data_list):
        df_sub = pd.DataFrame(data_list)
        if len(df_sub) < 3: return pd.DataFrame()
        n_ct = len(df_sub)
        df_sub['dr'] = df_sub['d'].rank(ascending=True, method='average') / n_ct
        df_sub['rr'] = df_sub['r'].rank(ascending=True, method='average') / n_ct
        df_sub['vr'] = df_sub['v'].rank(ascending=True, method='average') / n_ct
        df_sub['pdr'] = df_sub['pd'].rank(ascending=True, method='average') / n_ct
        df_sub['prr'] = df_sub['pr'].rank(ascending=True, method='average') / n_ct
        df_sub['pvr'] = df_sub['pv'].rank(ascending=True, method='average') / n_ct
        
        df_sub['rankAll'] = (df_sub['dr'] + df_sub['rr'] + df_sub['vr']) / 3.0
        df_sub['prevRankAll'] = (df_sub['pdr'] + df_sub['prr'] + df_sub['pvr']) / 3.0
        
        sigs = []
        for _, row in df_sub.iterrows():
            tA, pA, av, sc, x2 = row['rankAll'], row['prevRankAll'], row['av'], row['sc'], row['x2']
            if tA >= 0.90 and pA < 0.90: sig = "⚠️ 수급이탈 회피" if av else "🚀 정식 Track X"
            elif tA >= 0.85 and pA < 0.85 and sc: sig = "⚠️ 수급이탈 회피" if av else "🎯 Scout 진입"
            elif tA >= 0.85 and x2 >= 2: sig = "⚠️ 수급이탈 회피" if av else "⚡ Track X2"
            elif av and tA >= 0.80: sig = "⚠️ 수급이탈 회피"
            else: sig = "👀 일반/관망"
            sigs.append(sig)
        df_sub['signal'] = sigs
        df_sub = df_sub.sort_values('rankAll', ascending=False).reset_index(drop=True)
        df_sub['rank'] = range(1, len(df_sub) + 1)
        return df_sub

    v1_219_df = compute_v1(synced_219)
    v1_389_df = compute_v1(synced)
    v3_219_df = compute_v3(synced_219)
    v3_389_df = compute_v3(synced)

    # v4 대형주 계산
    v4_large_df = v3_389_df[v3_389_df['is_large'] == True].copy().reset_index(drop=True)
    v4_sigs = []
    for _, row in v4_large_df.iterrows():
        sig = row['signal']
        if sig == "👀 일반/관망" and row['rankAll'] >= 0.80 and not row['av']:
            sig = "🏛️ 대형주 랠리"
        v4_sigs.append(sig)
    v4_large_df['signal'] = v4_sigs
    v4_large_df = v4_large_df.sort_values('rankAll', ascending=False).reset_index(drop=True)
    v4_large_df['rank'] = range(1, len(v4_large_df) + 1)

    st.session_state['v1_219'] = v1_219_df
    st.session_state['v1_389'] = v1_389_df
    st.session_state['v3_219'] = v3_219_df
    st.session_state['v3_389'] = v3_389_df
    st.session_state['v4_large'] = v4_large_df
    st.session_state['target_date'] = t_date

    progress_bar.empty()
    status_text.success(f"✅ 통합 스캔 완료! (기준 영업일: {t_date} / 대상 389개)")

# ==========================================
# 5. Dashboard UI
# ==========================================
st.title("📈 Track X Master Dashboard")
st.caption("통합 마스터 엔진 (단 1회 스캔으로 v1, v3, v4 대형주 동시 연산)")

if st.button("🚀 마스터 스캔 시작", use_container_width=True):
    run_master_scan()

st.markdown("---")

if 'target_date' in st.session_state:
    st.subheader(f"📅 분석 기준일: {st.session_state['target_date']}")
    
    search_kwd = st.text_input("🔍 종목명 / 코드 / 섹터 검색", "")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["v1 (219)", "v1 (389)", "v3 (219)", "v3 (389)", "🏛️ 대형주 Top 60"])

    def filter_df(df):
        if search_kwd:
            return df[df['name'].str.contains(search_kwd, na=False) | df['code'].str.contains(search_kwd, na=False) | df['sector'].str.contains(search_kwd, na=False)]
        return df

    with tab1:
        d = filter_df(st.session_state['v1_219'])
        t = d[['rank', 'rank_percentile', 'name', 'code', 'sector', 'close', 'r', 'd', 'v']].copy()
        t.columns = ['순위', 'Rank Score', '종목명', '코드', '섹터', '현재가', 'RSI(9)', 'Donch Dist', 'Vol-Z(60)']
        t['Rank Score'] = t['Rank Score'].apply(lambda x: f"{x:.4f}")
        t['현재가'] = t['현재가'].apply(lambda x: f"{x:,}")
        t['RSI(9)'] = t['RSI(9)'].apply(lambda x: f"{x:.1f}")
        t['Donch Dist'] = t['Donch Dist'].apply(lambda x: f"{x:.2f}")
        t['Vol-Z(60)'] = t['Vol-Z(60)'].apply(lambda x: f"{x:.2f}")
        st.dataframe(t, use_container_width=True, hide_index=True)

    with tab2:
        d = filter_df(st.session_state['v1_389'])
        t = d[['rank', 'rank_percentile', 'name', 'code', 'sector', 'close', 'r', 'd', 'v']].copy()
        t.columns = ['순위', 'Rank Score', '종목명', '코드', '섹터', '현재가', 'RSI(9)', 'Donch Dist', 'Vol-Z(60)']
        t['Rank Score'] = t['Rank Score'].apply(lambda x: f"{x:.4f}")
        t['현재가'] = t['현재가'].apply(lambda x: f"{x:,}")
        t['RSI(9)'] = t['RSI(9)'].apply(lambda x: f"{x:.1f}")
        t['Donch Dist'] = t['Donch Dist'].apply(lambda x: f"{x:.2f}")
        t['Vol-Z(60)'] = t['Vol-Z(60)'].apply(lambda x: f"{x:.2f}")
        st.dataframe(t, use_container_width=True, hide_index=True)

    with tab3:
        d = filter_df(st.session_state['v3_219'])
        t = d[['rank', 'rankAll', 'signal', 'name', 'code', 'sector', 'close', 'r', 'd', 'v', 'wr', 'iip', 'dlaf']].copy()
        t.columns = ['순위', 'Rank Score', '시그널', '종목명', '코드', '섹터', '현재가', 'RSI9', 'Donch', 'VolZ', 'WR30', 'IIP', 'DLAF']
        t['Rank Score'] = t['Rank Score'].apply(lambda x: f"{x:.4f}")
        t['현재가'] = t['현재가'].apply(lambda x: f"{x:,}")
        t['RSI9'] = t['RSI9'].apply(lambda x: f"{x:.0f}")
        t['Donch'] = t['Donch'].apply(lambda x: f"{x:.2f}")
        t['VolZ'] = t['VolZ'].apply(lambda x: f"{x:.1f}")
        t['WR30'] = t['WR30'].apply(lambda x: f"{x:.0f}")
        t['IIP'] = t['IIP'].apply(lambda x: f"{x:.2f}")
        t['DLAF'] = t['DLAF'].apply(lambda x: f"{x:.2f}")
        st.dataframe(t, use_container_width=True, hide_index=True)

    with tab4:
        d = filter_df(st.session_state['v3_389'])
        t = d[['rank', 'rankAll', 'signal', 'name', 'code', 'sector', 'close', 'r', 'd', 'v', 'wr', 'iip', 'dlaf']].copy()
        t.columns = ['순위', 'Rank Score', '시그널', '종목명', '코드', '섹터', '현재가', 'RSI9', 'Donch', 'VolZ', 'WR30', 'IIP', 'DLAF']
        t['Rank Score'] = t['Rank Score'].apply(lambda x: f"{x:.4f}")
        t['현재가'] = t['현재가'].apply(lambda x: f"{x:,}")
        t['RSI9'] = t['RSI9'].apply(lambda x: f"{x:.0f}")
        t['Donch'] = t['Donch'].apply(lambda x: f"{x:.2f}")
        t['VolZ'] = t['VolZ'].apply(lambda x: f"{x:.1f}")
        t['WR30'] = t['WR30'].apply(lambda x: f"{x:.0f}")
        t['IIP'] = t['IIP'].apply(lambda x: f"{x:.2f}")
        t['DLAF'] = t['DLAF'].apply(lambda x: f"{x:.2f}")
        st.dataframe(t, use_container_width=True, hide_index=True)

    with tab5:
        d = filter_df(st.session_state['v4_large'])
        t = d[['rank', 'rankAll', 'signal', 'name', 'code', 'sector', 'close', 'r', 'd', 'v', 'wr', 'iip', 'dlaf']].copy()
        t.columns = ['순위', 'Rank Score', '시그널', '종목명', '코드', '섹터', '현재가', 'RSI9', 'Donch', 'VolZ', 'WR30', 'IIP', 'DLAF']
        t['Rank Score'] = t['Rank Score'].apply(lambda x: f"{x:.4f}")
        t['현재가'] = t['현재가'].apply(lambda x: f"{x:,}")
        t['RSI9'] = t['RSI9'].apply(lambda x: f"{x:.0f}")
        t['Donch'] = t['Donch'].apply(lambda x: f"{x:.2f}")
        t['VolZ'] = t['VolZ'].apply(lambda x: f"{x:.1f}")
        t['WR30'] = t['WR30'].apply(lambda x: f"{x:.0f}")
        t['IIP'] = t['IIP'].apply(lambda x: f"{x:.2f}")
        t['DLAF'] = t['DLAF'].apply(lambda x: f"{x:.2f}")
        st.dataframe(t, use_container_width=True, hide_index=True)
