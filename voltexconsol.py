#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
#           🔥 SCRIPT OWNER: PROFESSIONAL DEVELOPER REX 🔥
#              ⚡ TELEGRAM: @ador_debnath ⚡
#                 💎 ALL RIGHTS RESERVED 💎
# ═══════════════════════════════════════════════════════════

import os
import re
import time
import requests
import logging
import sqlite3
import threading
import html
import random
from datetime import datetime
import telebot
from telebot import types


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# DATABASE SETUP
# ═══════════════════════════════════════════════════════════
def init_database():
    conn = sqlite3.connect('bot_settings.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    ''')
    defaults = {
        'api_key':        'MEYEPG13TUX',
        'api_base':       'https://api.2oo9.cloud/MXS47FLFX0U/tnevs/@public/api',
        'otp_group_id':   '-1003798603523',
        'get_number_url': 'https://t.me/IVASSMS_NUMBER_PANEL_BOT',
        'developer_url':  'https://t.me/ador_debnath',
        'poll_interval':  '10'
    }
    for key, value in defaults.items():
        cursor.execute(
            'INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)',
            (key, value)
        )
    conn.commit()
    return conn

db_conn = init_database()

def get_setting(key: str) -> str:
    cursor = db_conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    result = cursor.fetchone()
    return result[0] if result else None

def set_setting(key: str, value: str):
    cursor = db_conn.cursor()
    cursor.execute(
        'INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
        (key, value)
    )
    db_conn.commit()


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# OTP EXTRACTION
# ═══════════════════════════════════════════════════════════
def extract_otp(message: str) -> str:
    if not message:
        return "N/A"
    patterns = [
        r'\b([A-Z]{2}-\d{5})\b',
        r'(\d{3})\s+(\d{3})',
        r'\b(\d{6})\b',
        r'\b(\d{5})\b',
        r'\b(\d{4})\b',
        r'code[:\s]+([A-Z0-9\-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            groups = [g for g in match.groups() if g]
            return ''.join(groups)
    return "N/A"


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# LANGUAGE DETECTION
# ═══════════════════════════════════════════════════════════
def detect_language(text: str) -> str:
    if not text:
        return "English"
    checks = [
        (["হয়", "করুন", "আপনার", "কোড"],          "Bengali"),
        (["है", "करें", "आपका", "कोड"],             "Hindi"),
        (["验证码", "你的", "代码"],                  "Chinese"),
        (["です", "ください", "コード"],              "Japanese"),
        (["입니다", "하세요", "코드"],                "Korean"),
        (["رمز", "التحقق", "يرجى"],                 "Arabic"),
        (["подтверждения", "пожалуйста"],            "Russian"),
        (["votre", "est votre", "partagez"],         "French"),
        (["código", "verificación", "ñ"],            "Spanish"),
        (["verificação", "código", "ã"],             "Portuguese"),
        (["doğrulama", "ş", "ğ"],                    "Turkish"),
        (["kode", "verifikasi"],                     "Indonesian"),
        (["รหัส", "ยืนยัน"],                        "Thai"),
        (["xác minh", "ệ", "ộ"],                    "Vietnamese"),
    ]
    for keywords, lang in checks:
        if any(k in text for k in keywords):
            return lang
    return "English"


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# PLATFORM NORMALIZE
# ═══════════════════════════════════════════════════════════
def normalize_platform(sid: str) -> str:
    sid_lower = sid.lower().strip()
    mapping = {
        "facebook":  "Facebook",
        "instagram": "Instagram",
        "whatsapp":  "WhatsApp",
        "telegram":  "Telegram",
        "twitter":   "Twitter",
        "google":    "Google",
        "tiktok":    "TikTok",
        "discord":   "Discord",
        "snapchat":  "Snapchat",
        "linkedin":  "LinkedIn",
    }
    for key, val in mapping.items():
        if key in sid_lower:
            return val
    return sid.title()


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# CONFIGURATION
# ═══════════════════════════════════════════════════════════
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8737601081:AAE1fWH5GvS9RWrN3rBSE4E_6ljBsSMooQU")
ADMINS    = [6484060347, 6034705730]

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# PLATFORM CONFIG
# ═══════════════════════════════════════════════════════════
PLATFORM_CONFIG = {
    "Facebook":  {"emoji": "🔵", "short": "FB"},
    "Instagram": {"emoji": "🟣", "short": "IG"},
    "Telegram":  {"emoji": "✈️",  "short": "TG"},
    "WhatsApp":  {"emoji": "🟢", "short": "WA"},
    "Twitter":   {"emoji": "🐦", "short": "TW"},
    "Google":    {"emoji": "🔴", "short": "GL"},
    "TikTok":    {"emoji": "🎵", "short": "TT"},
    "Discord":   {"emoji": "💜", "short": "DC"},
    "Snapchat":  {"emoji": "🟡", "short": "SC"},
    "LinkedIn":  {"emoji": "🔷", "short": "LI"},
}


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# COUNTRY DATA
# ═══════════════════════════════════════════════════════════
COUNTRY_FLAG = {
    "Algeria": "🇩🇿", "Angola": "🇦🇴", "Benin": "🇧🇯", "Botswana": "🇧🇼",
    "Burkina Faso": "🇧🇫", "Burundi": "🇧🇮", "Cabo Verde": "🇨🇻", "Cameroon": "🇨🇲",
    "Central African Republic": "🇨🇫", "Chad": "🇹🇩", "Comoros": "🇰🇲", "Congo": "🇨🇬",
    "Democratic Republic of Congo": "🇨🇩", "Djibouti": "🇩🇯", "Egypt": "🇪🇬",
    "Equatorial Guinea": "🇬🇶", "Eritrea": "🇪🇷", "Eswatini": "🇸🇿", "Ethiopia": "🇪🇹",
    "Gabon": "🇬🇦", "Gambia": "🇬🇲", "Ghana": "🇬🇭", "Guinea": "🇬🇳",
    "Guinea-Bissau": "🇬🇼", "Ivory Coast": "🇨🇮", "Côte d'Ivoire": "🇨🇮",
    "Kenya": "🇰🇪", "Lesotho": "🇱🇸", "Liberia": "🇱🇷", "Libya": "🇱🇾",
    "Madagascar": "🇲🇬", "Malawi": "🇲🇼", "Mali": "🇲🇱", "Mauritania": "🇲🇷",
    "Mauritius": "🇲🇺", "Morocco": "🇲🇦", "Mozambique": "🇲🇿", "Namibia": "🇳🇦",
    "Niger": "🇳🇪", "Nigeria": "🇳🇬", "Rwanda": "🇷🇼", "Senegal": "🇸🇳",
    "Seychelles": "🇸🇨", "Sierra Leone": "🇸🇱", "Somalia": "🇸🇴", "South Africa": "🇿🇦",
    "South Sudan": "🇸🇸", "Sudan": "🇸🇩", "Tanzania": "🇹🇿", "Togo": "🇹🇬",
    "Tunisia": "🇹🇳", "Uganda": "🇺🇬", "Zambia": "🇿🇲", "Zimbabwe": "🇿🇼",
    "Afghanistan": "🇦🇫", "Armenia": "🇦🇲", "Azerbaijan": "🇦🇿", "Bahrain": "🇧🇭",
    "Bangladesh": "🇧🇩", "Bhutan": "🇧🇹", "Brunei": "🇧🇳", "Cambodia": "🇰🇭",
    "China": "🇨🇳", "Cyprus": "🇨🇾", "Georgia": "🇬🇪", "Hong Kong": "🇭🇰",
    "India": "🇮🇳", "Indonesia": "🇮🇩", "Iran": "🇮🇷", "Iraq": "🇮🇶",
    "Israel": "🇮🇱", "Japan": "🇯🇵", "Jordan": "🇯🇴", "Kazakhstan": "🇰🇿",
    "Kuwait": "🇰🇼", "Kyrgyzstan": "🇰🇬", "Laos": "🇱🇦", "Lebanon": "🇱🇧",
    "Macau": "🇲🇴", "Malaysia": "🇲🇾", "Maldives": "🇲🇻", "Mongolia": "🇲🇳",
    "Myanmar": "🇲🇲", "Nepal": "🇳🇵", "North Korea": "🇰🇵", "Oman": "🇴🇲",
    "Pakistan": "🇵🇰", "Palestine": "🇵🇸", "Philippines": "🇵🇭", "Qatar": "🇶🇦",
    "Saudi Arabia": "🇸🇦", "Singapore": "🇸🇬", "South Korea": "🇰🇷", "Sri Lanka": "🇱🇰",
    "Syria": "🇸🇾", "Taiwan": "🇹🇼", "Tajikistan": "🇹🇯", "Thailand": "🇹🇭",
    "Timor-Leste": "🇹🇱", "Turkey": "🇹🇷", "Turkmenistan": "🇹🇲",
    "United Arab Emirates": "🇦🇪", "Uzbekistan": "🇺🇿", "Vietnam": "🇻🇳", "Yemen": "🇾🇪",
    "Albania": "🇦🇱", "Andorra": "🇦🇩", "Austria": "🇦🇹", "Belarus": "🇧🇾",
    "Belgium": "🇧🇪", "Bosnia and Herzegovina": "🇧🇦", "Bulgaria": "🇧🇬",
    "Croatia": "🇭🇷", "Czech Republic": "🇨🇿", "Denmark": "🇩🇰", "Estonia": "🇪🇪",
    "Finland": "🇫🇮", "France": "🇫🇷", "Germany": "🇩🇪", "Greece": "🇬🇷",
    "Hungary": "🇭🇺", "Iceland": "🇮🇸", "Ireland": "🇮🇪", "Italy": "🇮🇹",
    "Kosovo": "🇽🇰", "Latvia": "🇱🇻", "Liechtenstein": "🇱🇮", "Lithuania": "🇱🇹",
    "Luxembourg": "🇱🇺", "Malta": "🇲🇹", "Moldova": "🇲🇩", "Monaco": "🇲🇨",
    "Montenegro": "🇲🇪", "Netherlands": "🇳🇱", "North Macedonia": "🇲🇰",
    "Norway": "🇳🇴", "Poland": "🇵🇱", "Portugal": "🇵🇹", "Romania": "🇷🇴",
    "Russia": "🇷🇺", "Russian Federation": "🇷🇺", "Serbia": "🇷🇸", "Slovakia": "🇸🇰",
    "Slovenia": "🇸🇮", "Spain": "🇪🇸", "Sweden": "🇸🇪", "Switzerland": "🇨🇭",
    "Ukraine": "🇺🇦", "United Kingdom": "🇬🇧", "Vatican City": "🇻🇦",
    "Argentina": "🇦🇷", "Bahamas": "🇧🇸", "Barbados": "🇧🇧", "Belize": "🇧🇿",
    "Bolivia": "🇧🇴", "Brazil": "🇧🇷", "Canada": "🇨🇦", "Chile": "🇨🇱",
    "Colombia": "🇨🇴", "Costa Rica": "🇨🇷", "Cuba": "🇨🇺", "Dominican Republic": "🇩🇴",
    "Ecuador": "🇪🇨", "El Salvador": "🇸🇻", "Guatemala": "🇬🇹", "Guyana": "🇬🇾",
    "Haiti": "🇭🇹", "Honduras": "🇭🇳", "Jamaica": "🇯🇲", "Mexico": "🇲🇽",
    "Nicaragua": "🇳🇮", "Panama": "🇵🇦", "Paraguay": "🇵🇾", "Peru": "🇵🇪",
    "Suriname": "🇸🇷", "Trinidad and Tobago": "🇹🇹", "United States": "🇺🇸",
    "Uruguay": "🇺🇾", "Venezuela": "🇻🇪",
    "Australia": "🇦🇺", "Fiji": "🇫🇯", "New Zealand": "🇳🇿",
    "Papua New Guinea": "🇵🇬", "Samoa": "🇼🇸", "Solomon Islands": "🇸🇧",
    "Puerto Rico": "🇵🇷", "Guam": "🇬🇺", "Aruba": "🇦🇼",
    "Unknown": "🌍", "Other": "🌐",
}

COUNTRY_ISO_CODE = {
    "Algeria": "DZ", "Angola": "AO", "Benin": "BJ", "Botswana": "BW",
    "Burkina Faso": "BF", "Burundi": "BI", "Cabo Verde": "CV", "Cameroon": "CM",
    "Central African Republic": "CF", "Chad": "TD", "Comoros": "KM", "Congo": "CG",
    "Democratic Republic of Congo": "CD", "Djibouti": "DJ", "Egypt": "EG",
    "Equatorial Guinea": "GQ", "Eritrea": "ER", "Eswatini": "SZ", "Ethiopia": "ET",
    "Gabon": "GA", "Gambia": "GM", "Ghana": "GH", "Guinea": "GN",
    "Guinea-Bissau": "GW", "Ivory Coast": "CI", "Côte d'Ivoire": "CI",
    "Kenya": "KE", "Lesotho": "LS", "Liberia": "LR", "Libya": "LY",
    "Madagascar": "MG", "Malawi": "MW", "Mali": "ML", "Mauritania": "MR",
    "Mauritius": "MU", "Morocco": "MA", "Mozambique": "MZ", "Namibia": "NA",
    "Niger": "NE", "Nigeria": "NG", "Rwanda": "RW", "Senegal": "SN",
    "Seychelles": "SC", "Sierra Leone": "SL", "Somalia": "SO", "South Africa": "ZA",
    "South Sudan": "SS", "Sudan": "SD", "Tanzania": "TZ", "Togo": "TG",
    "Tunisia": "TN", "Uganda": "UG", "Zambia": "ZM", "Zimbabwe": "ZW",
    "Afghanistan": "AF", "Armenia": "AM", "Azerbaijan": "AZ", "Bahrain": "BH",
    "Bangladesh": "BD", "Bhutan": "BT", "Brunei": "BN", "Cambodia": "KH",
    "China": "CN", "Cyprus": "CY", "Georgia": "GE", "Hong Kong": "HK",
    "India": "IN", "Indonesia": "ID", "Iran": "IR", "Iraq": "IQ",
    "Israel": "IL", "Japan": "JP", "Jordan": "JO", "Kazakhstan": "KZ",
    "Kuwait": "KW", "Kyrgyzstan": "KG", "Laos": "LA", "Lebanon": "LB",
    "Macau": "MO", "Malaysia": "MY", "Maldives": "MV", "Mongolia": "MN",
    "Myanmar": "MM", "Nepal": "NP", "North Korea": "KP", "Oman": "OM",
    "Pakistan": "PK", "Palestine": "PS", "Philippines": "PH", "Qatar": "QA",
    "Saudi Arabia": "SA", "Singapore": "SG", "South Korea": "KR", "Sri Lanka": "LK",
    "Syria": "SY", "Taiwan": "TW", "Tajikistan": "TJ", "Thailand": "TH",
    "Timor-Leste": "TL", "Turkey": "TR", "Turkmenistan": "TM",
    "United Arab Emirates": "AE", "Uzbekistan": "UZ", "Vietnam": "VN", "Yemen": "YE",
    "Albania": "AL", "Andorra": "AD", "Austria": "AT", "Belarus": "BY",
    "Belgium": "BE", "Bosnia and Herzegovina": "BA", "Bulgaria": "BG",
    "Croatia": "HR", "Czech Republic": "CZ", "Denmark": "DK", "Estonia": "EE",
    "Finland": "FI", "France": "FR", "Germany": "DE", "Greece": "GR",
    "Hungary": "HU", "Iceland": "IS", "Ireland": "IE", "Italy": "IT",
    "Kosovo": "XK", "Latvia": "LV", "Liechtenstein": "LI", "Lithuania": "LT",
    "Luxembourg": "LU", "Malta": "MT", "Moldova": "MD", "Monaco": "MC",
    "Montenegro": "ME", "Netherlands": "NL", "North Macedonia": "MK",
    "Norway": "NO", "Poland": "PL", "Portugal": "PT", "Romania": "RO",
    "Russia": "RU", "Russian Federation": "RU", "Serbia": "RS", "Slovakia": "SK",
    "Slovenia": "SI", "Spain": "ES", "Sweden": "SE", "Switzerland": "CH",
    "Ukraine": "UA", "United Kingdom": "GB", "Vatican City": "VA",
    "Argentina": "AR", "Bahamas": "BS", "Barbados": "BB", "Belize": "BZ",
    "Bolivia": "BO", "Brazil": "BR", "Canada": "CA", "Chile": "CL",
    "Colombia": "CO", "Costa Rica": "CR", "Cuba": "CU", "Dominican Republic": "DO",
    "Ecuador": "EC", "El Salvador": "SV", "Guatemala": "GT", "Guyana": "GY",
    "Haiti": "HT", "Honduras": "HN", "Jamaica": "JM", "Mexico": "MX",
    "Nicaragua": "NI", "Panama": "PA", "Paraguay": "PY", "Peru": "PE",
    "Suriname": "SR", "Trinidad and Tobago": "TT", "United States": "US",
    "Uruguay": "UY", "Venezuela": "VE",
    "Australia": "AU", "Fiji": "FJ", "New Zealand": "NZ",
    "Papua New Guinea": "PG", "Samoa": "WS", "Solomon Islands": "SB",
    "Puerto Rico": "PR", "Guam": "GU", "Aruba": "AW",
    "Unknown": "XX", "Other": "XX"
}

PREFIX_COUNTRY = {
    "880": "Bangladesh",  "91": "India",         "92": "Pakistan",
    "93": "Afghanistan",  "94": "Sri Lanka",      "95": "Myanmar",
    "855": "Cambodia",    "856": "Laos",           "60": "Malaysia",
    "62": "Indonesia",    "63": "Philippines",     "65": "Singapore",
    "66": "Thailand",     "81": "Japan",           "82": "South Korea",
    "84": "Vietnam",      "86": "China",           "852": "Hong Kong",
    "853": "Macau",       "886": "Taiwan",         "90": "Turkey",
    "98": "Iran",         "212": "Morocco",        "213": "Algeria",
    "216": "Tunisia",     "218": "Libya",          "220": "Gambia",
    "221": "Senegal",     "222": "Mauritania",     "223": "Mali",
    "224": "Guinea",      "225": "Côte d'Ivoire",  "226": "Burkina Faso",
    "227": "Niger",       "228": "Togo",           "229": "Benin",
    "230": "Mauritius",   "231": "Liberia",        "232": "Sierra Leone",
    "233": "Ghana",       "234": "Nigeria",        "235": "Chad",
    "236": "Central African Republic", "237": "Cameroon", "238": "Cabo Verde",
    "239": "Sao Tome and Principe",    "240": "Equatorial Guinea",
    "241": "Gabon",       "242": "Congo",
    "243": "Democratic Republic of Congo",
    "244": "Angola",      "245": "Guinea-Bissau",  "248": "Seychelles",
    "249": "Sudan",       "250": "Rwanda",         "251": "Ethiopia",
    "252": "Somalia",     "253": "Djibouti",       "254": "Kenya",
    "255": "Tanzania",    "256": "Uganda",         "257": "Burundi",
    "258": "Mozambique",  "260": "Zambia",         "261": "Madagascar",
    "263": "Zimbabwe",    "264": "Namibia",        "265": "Malawi",
    "266": "Lesotho",     "267": "Botswana",       "268": "Eswatini",
    "269": "Comoros",     "27": "South Africa",    "291": "Eritrea",
    "30": "Greece",       "31": "Netherlands",     "32": "Belgium",
    "33": "France",       "34": "Spain",           "351": "Portugal",
    "352": "Luxembourg",  "353": "Ireland",        "354": "Iceland",
    "355": "Albania",     "356": "Malta",          "357": "Cyprus",
    "358": "Finland",     "359": "Bulgaria",       "36": "Hungary",
    "370": "Lithuania",   "371": "Latvia",         "372": "Estonia",
    "373": "Moldova",     "374": "Armenia",        "375": "Belarus",
    "376": "Andorra",     "377": "Monaco",         "380": "Ukraine",
    "381": "Serbia",      "382": "Montenegro",     "385": "Croatia",
    "386": "Slovenia",    "387": "Bosnia and Herzegovina",
    "389": "North Macedonia",
    "39": "Italy",        "40": "Romania",         "41": "Switzerland",
    "420": "Czech Republic", "421": "Slovakia",    "423": "Liechtenstein",
    "43": "Austria",      "44": "United Kingdom",  "45": "Denmark",
    "46": "Sweden",       "47": "Norway",          "48": "Poland",
    "49": "Germany",      "501": "Belize",         "502": "Guatemala",
    "503": "El Salvador", "504": "Honduras",       "505": "Nicaragua",
    "506": "Costa Rica",  "507": "Panama",         "509": "Haiti",
    "51": "Peru",         "52": "Mexico",          "53": "Cuba",
    "54": "Argentina",    "55": "Brazil",          "56": "Chile",
    "57": "Colombia",     "58": "Venezuela",       "591": "Bolivia",
    "592": "Guyana",      "593": "Ecuador",        "595": "Paraguay",
    "597": "Suriname",    "598": "Uruguay",
    "1": "United States", "7": "Russia",
}

def get_country_from_number(number: str) -> str:
    clean = re.sub(r'[^0-9]', '', number)
    for length in [4, 3, 2, 1]:
        prefix = clean[:length]
        if prefix in PREFIX_COUNTRY:
            return PREFIX_COUNTRY[prefix]
    return "Unknown"


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# VERSION CHECK
# ═══════════════════════════════════════════════════════════
def get_telebot_version():
    try:
        return telebot.__version__
    except AttributeError:
        try:
            import importlib.metadata
            return importlib.metadata.version("pytelegrambotapi")
        except Exception:
            return "Unknown"


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# ADMIN CHECK
# ═══════════════════════════════════════════════════════════
def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# OTP MESSAGE KEYBOARD
# ═══════════════════════════════════════════════════════════
def make_otp_keyboard(range_val: str) -> types.InlineKeyboardMarkup:
    """
    3 Buttons:
    [GET NUMBER] [📋 Range] [🤖 Developer]
    """
    markup = types.InlineKeyboardMarkup(row_width=3)

    get_number_url = get_setting('get_number_url')
    developer_url  = get_setting('developer_url')

    # GET NUMBER button
    get_btn = types.InlineKeyboardButton(
        text="GET NUMBER",
        url=get_number_url
    )

    # Copy Range button
    if hasattr(types, 'CopyTextButton'):
        copy_btn = types.InlineKeyboardButton(
            text=f"📋 {range_val}",
            copy_text=types.CopyTextButton(text=str(range_val))
        )
    else:
        copy_btn = types.InlineKeyboardButton(
            text=f"📋 {range_val}",
            callback_data=f"copy:{range_val}"
        )

    # Developer button
    dev_btn = types.InlineKeyboardButton(
        text="🤖 Developer",
        url=developer_url
    )

    markup.row(get_btn, copy_btn, dev_btn)
    return markup


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# FORMAT OTP MESSAGE
# ═══════════════════════════════════════════════════════════
def format_otp_message(hit: dict):
    """
    Format:
    ✅ All Active Range ✅

    🌐 Country: 🇬🇳 Guinea [GN]
    📱 Service: 🔵 Facebook
    📊 Range: +22465XXX
    📨 SMS: FB-26227...  French

    [GET NUMBER] [📋 22465XXX] [🤖 Developer]
    """
    message   = hit.get("message", "")
    range_val = hit.get("range", "N/A")
    sid       = hit.get("sid", "Unknown")
    timestamp = hit.get("time", 0)

    # Normalize platform
    platform = normalize_platform(sid)

    # Extract OTP & language
    otp_code = extract_otp(message)
    language = detect_language(message)

    # Country from number prefix
    country_name = get_country_from_number(range_val)
    c_flag       = COUNTRY_FLAG.get(country_name, "🌍")
    c_code       = COUNTRY_ISO_CODE.get(country_name, "XX")

    # Platform
    p_cfg   = PLATFORM_CONFIG.get(platform, {"emoji": "📩", "short": "OT"})
    p_emoji = p_cfg["emoji"]

    # Full number with +
    full_number = range_val
    if not full_number.startswith('+'):
        full_number = f"+{full_number}"

    # Clean SMS (remove hash tags, new lines, limit length)
    clean_msg = re.sub(r'<#>\s*', '', message)
    clean_msg = re.sub(r'\s+', ' ', clean_msg).strip()
    clean_msg = clean_msg[:250]

    # ✅ HTML Format
    text = (
        f"<b>✅ All Active Range ✅</b>\n\n"
        f"🌐 <b>Country:</b> {c_flag} {html.escape(country_name)} [{c_code}]\n"
        f"📱 <b>Service:</b> {p_emoji} {html.escape(platform)}\n"
        f"📊 <b>Range:</b> <code>{html.escape(full_number)}</code>\n"
        f"📨 <b>SMS:</b> {html.escape(clean_msg)}  {html.escape(language)}\n\n"
    )

    keyboard = make_otp_keyboard(range_val)
    return text, keyboard, timestamp


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# API FETCH
# ═══════════════════════════════════════════════════════════
def fetch_console_data():
    api_key  = get_setting('api_key')
    api_base = get_setting('api_base')
    url      = f"{api_base}/console"
    headers  = {
        "mauthapi":     api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        if data.get("meta", {}).get("code") == 200:
            return data.get("data", {}).get("hits", [])
        logger.error(f"API error: {data.get('message')}")
        return []
    except Exception as e:
        logger.error(f"API fetch error: {e}")
        return []


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# SEND TO GROUP
# ═══════════════════════════════════════════════════════════
def send_to_group(text: str, keyboard: types.InlineKeyboardMarkup):
    otp_group_id = int(get_setting('otp_group_id'))
    try:
        bot.send_message(
            chat_id=otp_group_id,
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
        logger.info("✅ OTP sent!")
    except Exception as e:
        logger.error(f"❌ Send Error: {e}")


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# ADMIN PANEL
# ═══════════════════════════════════════════════════════════
def show_admin_panel(chat_id, message_id=None):
    panel_text = (
        "🔧 <b>Admin Panel</b>\n"
        "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
        "✏️ Select a setting to edit:\n\n"
        "<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>"
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔑 API Key",        callback_data="edit_api_key"),
        types.InlineKeyboardButton("🌐 API Base URL",   callback_data="edit_api_base"),
        types.InlineKeyboardButton("📱 OTP Group ID",   callback_data="edit_otp_group_id"),
        types.InlineKeyboardButton("🔗 GET NUMBER URL", callback_data="edit_get_number_url"),
        types.InlineKeyboardButton("👨‍💻 Dev URL",       callback_data="edit_developer_url"),
        types.InlineKeyboardButton("⏱ Poll Interval",  callback_data="edit_poll_interval"),
    )
    markup.add(
        types.InlineKeyboardButton("📊 View Settings", callback_data="view_settings"),
        types.InlineKeyboardButton("❌ Close",          callback_data="close_panel")
    )
    try:
        if message_id:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=panel_text,
                parse_mode="HTML",
                reply_markup=markup
            )
        else:
            bot.send_message(
                chat_id=chat_id,
                text=panel_text,
                parse_mode="HTML",
                reply_markup=markup
            )
    except Exception as e:
        logger.error(f"Admin panel error: {e}")


def show_current_settings(chat_id, message_id):
    text = (
        "📊 <b>Current Settings</b>\n"
        "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
        f"🔑 <b>API Key:</b>\n<code>{get_setting('api_key')}</code>\n\n"
        f"🌐 <b>API Base:</b>\n<code>{get_setting('api_base')}</code>\n\n"
        f"📱 <b>OTP Group ID:</b>\n<code>{get_setting('otp_group_id')}</code>\n\n"
        f"🔗 <b>GET NUMBER URL:</b>\n<code>{get_setting('get_number_url')}</code>\n\n"
        f"👨‍💻 <b>Developer URL:</b>\n<code>{get_setting('developer_url')}</code>\n\n"
        f"⏱ <b>Poll Interval:</b> <code>{get_setting('poll_interval')}s</code>\n"
        "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"
        "<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("◀️ Back", callback_data="admin_panel"))
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Settings error: {e}")


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# BOT COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════

@bot.message_handler(commands=['start'])
def cmd_start(message):
    user_id = message.from_user.id
    if is_admin(user_id):
        text = (
            "🤖 <b>REX OTP Bot</b>\n"
            "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
            f"👋 Welcome Admin!\n"
            f"🆔 Your ID: <code>{user_id}</code>\n\n"
            "<b>📋 Commands:</b>\n"
            "🔧 /admin — Admin Panel\n"
            "📊 /settings — View Settings\n"
            "🆔 /myid — Your Telegram ID\n\n"
            "<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>\n"
            "<i>⚡ @ador_debnath</i>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "🔧 Open Admin Panel", callback_data="admin_panel"
        ))
    else:
        text = (
            "🤖 <b>REX OTP Bot</b>\n"
            "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
            f"🆔 Your ID: <code>{user_id}</code>\n"
            "⚡ Bot is live and posting OTPs!\n\n"
            "<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "🤖 Developer", url=get_setting('developer_url')
        ))
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode="HTML",
        reply_markup=markup
    )


@bot.message_handler(commands=['myid'])
def cmd_myid(message):
    bot.reply_to(
        message,
        f"🆔 <b>Your Telegram ID:</b>\n<code>{message.from_user.id}</code>\n\n"
        f"<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>",
        parse_mode="HTML"
    )


@bot.message_handler(commands=['admin', 'panel'])
def cmd_admin(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(
            message,
            f"❌ <b>Access Denied!</b>\n\n"
            f"🆔 Your ID: <code>{message.from_user.id}</code>\n"
            f"You are not an admin!\n\n"
            f"<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>",
            parse_mode="HTML"
        )
        return
    show_admin_panel(message.chat.id)


@bot.message_handler(commands=['settings'])
def cmd_settings(message):
    if not is_admin(message.from_user.id):
        bot.reply_to(
            message,
            "❌ <b>Access Denied!</b>",
            parse_mode="HTML"
        )
        return
    text = (
        "📊 <b>Current Settings</b>\n"
        "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
        f"🔑 <b>API Key:</b> <code>{get_setting('api_key')}</code>\n\n"
        f"🌐 <b>API Base:</b> <code>{get_setting('api_base')}</code>\n\n"
        f"📱 <b>OTP Group ID:</b> <code>{get_setting('otp_group_id')}</code>\n\n"
        f"🔗 <b>GET NUMBER URL:</b> <code>{get_setting('get_number_url')}</code>\n\n"
        f"👨‍💻 <b>Developer URL:</b> <code>{get_setting('developer_url')}</code>\n\n"
        f"⏱ <b>Poll Interval:</b> <code>{get_setting('poll_interval')}s</code>\n\n"
        "<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔧 Admin Panel", callback_data="admin_panel"))
    bot.reply_to(message, text, parse_mode="HTML", reply_markup=markup)


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# CALLBACK HANDLER
# ═══════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id

    # Copy callback (everyone)
    if call.data.startswith("copy:"):
        val = call.data.split("copy:")[1]
        try:
            bot.answer_callback_query(
                call.id,
                text=f"📋 Copied: {val}",
                show_alert=True
            )
        except Exception as e:
            logger.error(f"Copy callback error: {e}")
        return

    # Admin only
    if not is_admin(user_id):
        bot.answer_callback_query(
            call.id,
            text="❌ Admins only!",
            show_alert=True
        )
        return

    if call.data == "admin_panel":
        bot.answer_callback_query(call.id)
        show_admin_panel(call.message.chat.id, call.message.message_id)

    elif call.data == "view_settings":
        bot.answer_callback_query(call.id)
        show_current_settings(call.message.chat.id, call.message.message_id)

    elif call.data.startswith("edit_"):
        setting_key = call.data.replace("edit_", "")
        bot.answer_callback_query(call.id)

        labels = {
            'api_key':        '🔑 API Key',
            'api_base':       '🌐 API Base URL',
            'otp_group_id':   '📱 OTP Group ID',
            'get_number_url': '🔗 GET NUMBER URL',
            'developer_url':  '👨‍💻 Developer URL',
            'poll_interval':  '⏱ Poll Interval (sec)',
        }

        ask_text = (
            f"✏️ <b>Edit {labels.get(setting_key, setting_key)}</b>\n"
            f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n\n"
            f"📌 Current:\n<code>{get_setting(setting_key)}</code>\n\n"
            f"💬 Send the new value now:\n\n"
            f"<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("❌ Cancel", callback_data="admin_panel"))

        msg = bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=ask_text,
            parse_mode="HTML",
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_setting_update, setting_key)

    elif call.data == "close_panel":
        bot.answer_callback_query(call.id)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            logger.error(f"Delete error: {e}")


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# PROCESS SETTING UPDATE
# ═══════════════════════════════════════════════════════════
def process_setting_update(message, setting_key):
    if message.text and message.text.startswith('/'):
        bot.reply_to(message, "❌ Update cancelled.")
        return

    new_value = (message.text or "").strip()
    if not new_value:
        bot.reply_to(message, "❌ Empty value! Cancelled.")
        return

    if setting_key == 'otp_group_id':
        try:
            int(new_value)
        except ValueError:
            bot.reply_to(
                message,
                "❌ <b>Invalid Group ID!</b>\nMust be a number like <code>-1001234567890</code>",
                parse_mode="HTML"
            )
            return

    elif setting_key == 'poll_interval':
        try:
            if int(new_value) < 5:
                bot.reply_to(message, "❌ Minimum 5 seconds!")
                return
        except ValueError:
            bot.reply_to(message, "❌ Must be a number!")
            return

    set_setting(setting_key, new_value)

    labels = {
        'api_key':        'API Key',
        'api_base':       'API Base URL',
        'otp_group_id':   'OTP Group ID',
        'get_number_url': 'GET NUMBER URL',
        'developer_url':  'Developer URL',
        'poll_interval':  'Poll Interval',
    }

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔧 Back to Panel", callback_data="admin_panel"))

    bot.reply_to(
        message,
        f"✅ <b>{labels.get(setting_key, setting_key)} Updated!</b>\n\n"
        f"📌 New value:\n<code>{html.escape(new_value)}</code>\n\n"
        f"<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>",
        parse_mode="HTML",
        reply_markup=markup
    )
    logger.info(f"✅ Setting updated: {setting_key} = {new_value}")


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# STARTUP MESSAGE
# ═══════════════════════════════════════════════════════════
def send_startup_message():
    otp_group_id = int(get_setting('otp_group_id'))
    version      = get_telebot_version()
    copy_support = "✅ Auto Copy" if hasattr(types, 'CopyTextButton') else "⚠️ Callback"

    text = (
        f"🤖 <b>REX OTP Bot Started!</b>\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"
        f"✅ Bot is <b>Online</b> and Running\n"
        f"⏱ Interval: <code>{get_setting('poll_interval')}s</code>\n"
        f"📡 Source: <code>api.2oo9.cloud</code>\n"
        f"📦 Version: <code>v{version}</code>\n"
        f"📋 Copy: {copy_support}\n"
        f"┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n"
        f"⚡ <i>Waiting for live OTP data...</i>\n\n"
        f"<i>👨‍💻 SCRIPT OWNER: DEVELOPER REX</i>\n"
        f"<i>⚡ @ador_debnath</i>"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "🤖 Developer", url=get_setting('developer_url')
    ))
    try:
        bot.send_message(
            chat_id=otp_group_id,
            text=text,
            parse_mode="HTML",
            reply_markup=markup
        )
        logger.info("✅ Startup message sent!")
    except Exception as e:
        logger.error(f"Startup error: {e}")


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# OTP POLLING LOOP (BACKGROUND THREAD)
# ═══════════════════════════════════════════════════════════
def otp_polling_loop():
    sent_timestamps = set()
    total_sent      = 0
    retry_count     = 0

    logger.info("📡 OTP polling thread started!")

    while True:
        try:
            poll_interval = int(get_setting('poll_interval'))
            time.sleep(poll_interval)

            hits = fetch_console_data()

            if not hits:
                logger.info(f"⏳ No data | Total: {total_sent}")
                retry_count = 0
                continue

            new_count = 0
            for hit in reversed(hits):
                result = format_otp_message(hit)
                if result[0] is None:
                    continue

                text, keyboard, timestamp = result
                if timestamp in sent_timestamps:
                    continue

                send_to_group(text, keyboard)
                sent_timestamps.add(timestamp)
                total_sent += 1
                new_count  += 1
                time.sleep(1.5)

            if new_count > 0:
                logger.info(f"📨 {new_count} new | Total: {total_sent}")
            else:
                logger.info(f"✔ No new | Total: {total_sent}")

            # Clean cache
            if len(sent_timestamps) > 2000:
                oldest = sorted(sent_timestamps)[:500]
                for ts in oldest:
                    sent_timestamps.discard(ts)
                logger.info("🗑 Cache cleaned")

            retry_count = 0

        except Exception as e:
            retry_count += 1
            logger.error(f"OTP loop error ({retry_count}): {e}")
            time.sleep(min(retry_count * 5, 60))


# ═══════════════════════════════════════════════════════════
# 👨‍💻 SCRIPT OWNER BY REX
# MAIN
# ═══════════════════════════════════════════════════════════
def main():
    version = get_telebot_version()
    logger.info("🚀 REX OTP Bot starting...")
    me = bot.get_me()
    logger.info(f"✅ Bot: @{me.username}")
    logger.info(f"📦 pyTeleBot: v{version}")
    logger.info(f"👥 Admins: {ADMINS}")

    # Start OTP polling background thread
    otp_thread = threading.Thread(target=otp_polling_loop, daemon=True)
    otp_thread.start()
    logger.info("✅ OTP thread started!")

    # Startup message
    send_startup_message()

    # Bot polling (main thread - handles all commands)
    logger.info("🔄 Bot polling started...")
    bot.infinity_polling(
        timeout=30,
        long_polling_timeout=20,
        logger_level=logging.WARNING
    )


# ═══════════════════════════════════════════════════════════
# 🔥 SCRIPT OWNER: PROFESSIONAL DEVELOPER REX 🔥
# ⚡ TELEGRAM: @ador_debnath ⚡
# 💎 ALL RIGHTS RESERVED 💎
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("👋 REX Bot Shutdown!")
        db_conn.close()