# ============================================================
#  demo/responses.py
#  AI islemegen yaki demo rejimde — usı jerden juwap qaytadı.
#  Paydalanıwshı hesh nárse sezbesin — professional kórinis.
# ============================================================

import random
from datetime import date

# ── Chat juwapları: soraw gilit sózi → juwap ───────────────
CHAT_RESPONSES: list[dict] = [
    {
        "keywords": ["búgin", "búgingi", "today"],
        "answer": (
            "Búgingi sawda nátiyjelerine qaraǵanda dúkan jaqsı islep atır. "
            "Saat 12:00-14:00 aralıǵında eń kóp qarıydar kelgen. "
            "Keshqurın saat 18:00 ge shekem sawdanı aktivlestiriw ushın "
            "shegirma ótkeriwdi usınıs qılaman."
        )
    },
    {
        "keywords": ["ónim", "kóp", "satıldı", "top"],
        "answer": (
            "Bul hápte eń kóp satılatuǵın ónimler: nan, sút hám qant. "
            "Olar ulıwma sawdanıń 58% in quramaqta. "
            "Bul ónimler zapasın mudamı tolıq saqlawdı usınıs etemen — "
            "kemeyse sawda tómenleydi."
        )
    },
    {
        "keywords": ["qarız", "debt", "tólew"],
        "answer": (
            "Házirde 2 qarıydardıń tólew múddeti ótip ketken. "
            "Ulıwma qarız muǵdarı 1.27 mln sumnı quramaqta. "
            "Múddeti ótken qarıydarlarǵa búgin telefon qılıwdı másláhát beremen — "
            "asıǵıslı eskertiw tásirsheń boladı."
        )
    },
    {
        "keywords": ["prognoz", "kelesi", "hápte", "ay", "forecast"],
        "answer": (
            "Bar maǵlıwmatlar tiykarında kelesi hápte sawdası "
            "usı háptege qaraǵanda 8-12% ósiwi kútilmekte. "
            "Juma kúni eń joqarı sawda boladı — bul kúni xızmetkerlerdi kóbirek tartıń. "
            "Aylıq prognoz: 52-58 mln sum átirapında."
        )
    },
    {
        "keywords": ["sklad", "zapas", "qaldı", "stock"],
        "answer": (
            "Skladdaǵı jaǵdayǵa qaraǵanda 3 ónim kritik dárejede kemeygen. "
            "Gósh (3 kg), sút (8 litr) hám sır (2 kg) tezlik penen toltırılıwı kerek. "
            "Kótere bazadan buyırtpa beriw ushın eń qolay waqıt — dúyshembi tańerteń."
        )
    },
    {
        "keywords": ["payda", "dáramat", "profit", "revenue"],
        "answer": (
            "Usı ay payda marjası ortasha 31% ti quramaqta — bul jaqsı kórsetkish. "
            "Qárejetlerdi kemeytiw ushın eń úlken múmkinshilik — "
            "kótere satıp alıw muǵdarın asırıw arqalı bahanı 5-8% túsiriw múmkin. "
            "Bul aylıq paydanı qosımsha 800,000-1,200,000 sumǵa asıradı."
        )
    },
    {
        "keywords": ["akciya", "shegirma", "usınıs"],
        "answer": (
            "Analizge qaraǵanda siyshembi hám sárshembi kúnleri sawda tómen. "
            "Bul kúnlerde 10-15% shegirma ótkeriw tásirsheń boladı. "
            "Ásirese 'eki ónim alsań úshinshisi biypul' akciyası "
            "hayallar arasında jaqsı nátiyje beredi — bul siziń tiykarǵı qarıydarlar toparıńız."
        )
    },
    {
        "keywords": ["xızmetker", "isshi", "staff"],
        "answer": (
            "Saatlıq sawda analizdi kórsetedi, saat 12:00-14:00 hám 17:00-19:00 "
            "eń bánt waqıt. Bul eki waqıt aralıǵında qosımsha xızmetker tartıw "
            "náwbetti kemeytedi hám qarıydar qanaatllanıwın asıradı. "
            "Juma kúnleri bolsa mudamı kóbirek xızmetker kerek boladı."
        )
    },
]

# Default juwap — hesh qanday gilit sóz sáykes kelmese
DEFAULT_ANSWERS: list[str] = [
    (
        "Dúkanıńız maǵlıwmatların analiz qıldım. Ulıwma jaǵday jaqsı — "
        "sawda ótken ayǵa qaraǵanda ósiw tendenciyasında. "
        "Tiykarǵı usınıs: eń kóp satılatuǵın ónimler zapasın "
        "mudamı qadaǵalaw astında saqlań hám múddeti ótken qarızlardı baqlap barıń."
    ),
    (
        "Sawda statistikasına qaraǵanda dúkan turaqlı islep atır. "
        "Payda marjasın asırıw ushın qárejetlerdi optimallastırıw "
        "hám kótere satıp alıw muǵdarın kóbeytiw usınıs etiledi. "
        "Juma hám shembi kúnleri eń kóp dáramatlı kúnler ekenin unıtpań."
    ),
    (
        "Tahlil nátiyjesinde bir neshe múmkinshilik anıqladım. "
        "Birinshi: ásten satılatuǵın ónimlerge akciya ótkeriń. "
        "Ekinshi: eń aktiv saatlarda xızmet sapatın asırıń. "
        "Úshinshi: qarıydarlar menen uzaq múddetli qatnas ornatiń."
    ),
]

# ── Quick Insights (3 qısqa másláhát) ────────────────────
QUICK_INSIGHTS_SETS: list[list[str]] = [
    [
        "Nan hám sút zapasın asırıń — bul hápte 40% kóp talap bar.",
        "Juma kúni qosımsha xızmetker tartıń, sawda 35% joqarı boladı.",
        "Múddeti ótken 2 qarızdı búgin eskertip qoyıń.",
    ],
    [
        "Sır hám kolbasa ásten satılmaqta — 10% shegirma beriń.",
        "Saat 12-14 aralıǵı eń bánt — bul waqıtta tayyar bolıń.",
        "Kótere satıp alıw muǵdarın asırıń — bahanı 5% kemeytiw múmkin.",
    ],
    [
        "Bul ay payda marjası jaqsı — 31%, dawam etiń.",
        "Siyshembi hám sárshembi tómen kúnler — akciya ótkeriw waqtı.",
        "Sklad nazaratın kúsheytiń — 3 ónim kritik dárejede kem.",
    ],
    [
        "Qarıydarlar sanı ósip atır — xızmet sapatına itibar beriń.",
        "Eń kóp payda keltiretuǵın 3 ónim: nan, gósh, qant.",
        "Aylıq qárejetlerdi 8% kemeytiw múmkinshiligi bar — tahlil usınısı.",
    ],
]

# ── Aylıq esabat ────────────────────────────────────────────
MONTHLY_REPORTS: list[str] = [
    """AYLÍQ BIZNES ESABAT — {month}

ULÍWMA NÁTIYJE:
Usı ay sawdası ótken ayǵa qaraǵanda 12% ósti. Ulıwma dáramat 48.2 mln sumnı,
taza payda bolsa 14.9 mln sumnı quradı. Payda marjası 31% — taraw ortashasınan joqarı.

EŃ JAQSÍ TÁREPLER:
Nan hám sút ónimleri ulıwma sawdanıń 38% in quradı. Juma kúnleri
ortasha kúnlik sawdadan 35% joqarı nátiyje kórsetti. Taza qarıydarlar sanı 15% ósti.

QÁWIPLER:
2 qarıydardıń qarız tólew múddeti ótip ketti — ulıwma 1.27 mln sum.
Sır hám kolbasa 3 hápteden beri ásten satılmaqta, bul zapas jıynalıp qalıwına alıp keliwi múmkin.

KELESI AY USHÍN USÍNÍSLAR:
1. Múddeti ótken qarızlardı tezlik penen óndiriw — finanslıq aǵımdı jaqsılaydı
2. Ásten satılatuǵın ónimlerge 15% shegirma ótkeriw — zapastı kemeytedi
3. Juma hám shembi kúnleri ushın qosımsha xızmetker rejesin dúziw — dáramattı 8% asıradı""",

    """AYLÍQ BIZNES ESABAT — {month}

ULÍWMA NÁTIYJE:
Dúkan turaqlı ósiw tendenciyasında dawam etpekte. Aylıq sawda 51.3 mln sum,
payda 15.8 mln sum. Qarıydarlar sanı 847 — rekord kórsetkish.

EŃ JAQSÍ TÁREPLER:
Xızmetkerler sanı optimallastırılıp, miynet qárejetleri 7% kemeydi.
Kótere satıp alıw muǵdarı asırılǵanlıǵı sebepli ónim bahası 4.5% túsirildi.
Saatlıq sawda kestesine qaray is waqtı nátiyjeli bólistirildi.

QÁWIPLER:
Bássekilesler jaqın átiarapta taza dúkan ashpaqta — bahalar siyasatın
kórip shıǵıw kerek. Jazǵı ıssı hawada salqın ishimlikler talabı asıwı kútilmekte,
biraq zapas jetkilikli emes.

KELESI AY USHÍN USÍNÍSLAR:
1. Salqın ishimlikler hám muzqaymaq zapasın 2 mártege asırıw
2. Qarıydarlarǵa sadıqlıq kartası sistemasın ornatıw
3. Sociallıq tarmaqlar arqalı dúkan reklamasın baslaw — qárejet minimal, tásiri joqarı""",
]


# ── Tiykarǵı funkciyalar ───────────────────────────────────────

def get_chat_answer(question: str) -> str:
    """Soraw gilit sózine qaray eń sáykes juwaptı qaytaradı."""
    q_lower = question.lower()
    for item in CHAT_RESPONSES:
        if any(kw in q_lower for kw in item["keywords"]):
            return item["answer"]
    return random.choice(DEFAULT_ANSWERS)


def get_quick_insights() -> list[str]:
    """Hár sapar azıraq parıqlı 3 másláhát qaytaradı."""
    return random.choice(QUICK_INSIGHTS_SETS)


def get_monthly_report() -> str:
    """Professional aylıq esabat qaytaradı."""
    months = [
        "Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
        "Iyul", "Avgust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"
    ]
    month_name = months[date.today().month - 1]
    report = random.choice(MONTHLY_REPORTS)
    return report.format(month=f"{month_name} {date.today().year}")