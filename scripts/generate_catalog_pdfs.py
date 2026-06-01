from pathlib import Path
from shutil import copyfile
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets" / "catalogs"
IMAGE_DIR = ROOT / "images" / "products"

DARK = colors.HexColor("#070b12")
PANEL = colors.HexColor("#111820")
PANEL_2 = colors.HexColor("#161f28")
GOLD = colors.HexColor("#d4a855")
GOLD_DARK = colors.HexColor("#9f7430")
CREAM = colors.HexColor("#f8f0dc")
MUTED = colors.HexColor("#b9c0c9")
LINE = colors.HexColor("#2a3540")
WHITE = colors.white


def register_fonts():
    font_candidates = [
        (
            Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
            Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ),
        (
            Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
            Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ),
    ]

    for regular, bold in font_candidates:
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont("KMZ-Regular", str(regular)))
            pdfmetrics.registerFont(TTFont("KMZ-Bold", str(bold)))
            return "KMZ-Regular", "KMZ-Bold"

    fallback = Path(__import__("reportlab").__file__).parent / "fonts" / "Vera.ttf"
    bold_fallback = Path(__import__("reportlab").__file__).parent / "fonts" / "VeraBd.ttf"
    pdfmetrics.registerFont(TTFont("KMZ-Regular", str(fallback)))
    pdfmetrics.registerFont(TTFont("KMZ-Bold", str(bold_fallback)))
    return "KMZ-Regular", "KMZ-Bold"


FONT_REGULAR, FONT_BOLD = register_fonts()


def paragraph(text, style):
    return Paragraph(escape(text), style)


def make_styles():
    return {
        "cover_badge": ParagraphStyle(
            "cover_badge",
            fontName=FONT_BOLD,
            fontSize=9,
            leading=12,
            textColor=GOLD,
            alignment=TA_LEFT,
            uppercase=True,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName=FONT_BOLD,
            fontSize=32,
            leading=38,
            textColor=CREAM,
            alignment=TA_LEFT,
            spaceAfter=12,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            fontName=FONT_REGULAR,
            fontSize=13,
            leading=20,
            textColor=MUTED,
            alignment=TA_LEFT,
            spaceAfter=22,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName=FONT_BOLD,
            fontSize=20,
            leading=26,
            textColor=CREAM,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName=FONT_BOLD,
            fontSize=15,
            leading=20,
            textColor=CREAM,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            fontName=FONT_REGULAR,
            fontSize=9.7,
            leading=14.2,
            textColor=MUTED,
            alignment=TA_LEFT,
        ),
        "body_light": ParagraphStyle(
            "body_light",
            fontName=FONT_REGULAR,
            fontSize=9.4,
            leading=13.4,
            textColor=colors.HexColor("#e5e9ee"),
            alignment=TA_LEFT,
        ),
        "card_title": ParagraphStyle(
            "card_title",
            fontName=FONT_BOLD,
            fontSize=13.5,
            leading=17,
            textColor=CREAM,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "formula": ParagraphStyle(
            "formula",
            fontName=FONT_BOLD,
            fontSize=8.5,
            leading=11,
            textColor=GOLD,
            alignment=TA_LEFT,
            spaceAfter=5,
        ),
        "label": ParagraphStyle(
            "label",
            fontName=FONT_BOLD,
            fontSize=7.5,
            leading=10,
            textColor=GOLD,
            alignment=TA_LEFT,
        ),
        "value": ParagraphStyle(
            "value",
            fontName=FONT_REGULAR,
            fontSize=7.7,
            leading=10.4,
            textColor=colors.HexColor("#e5e9ee"),
            alignment=TA_LEFT,
        ),
        "small": ParagraphStyle(
            "small",
            fontName=FONT_REGULAR,
            fontSize=7.8,
            leading=10.8,
            textColor=MUTED,
            alignment=TA_LEFT,
        ),
        "contact": ParagraphStyle(
            "contact",
            fontName=FONT_BOLD,
            fontSize=10,
            leading=14,
            textColor=CREAM,
            alignment=TA_CENTER,
        ),
    }


TEXT = {
    "de": {
        "language_name": "Deutsch",
        "version": "Ausgabe 2026",
        "public": "Öffentliche Käuferübersicht",
        "full_title": "KMZ Trade Gesamtkatalog",
        "minerals_title": "KMZ Trade Mineralienkatalog",
        "food_title": "KMZ Trade Lebensmittelkatalog",
        "full_subtitle": "Industriemineralien, Speiseöle und Zucker für internationale Käufer, mit strukturierter Dokumentation und kontrollierter Beschaffung.",
        "minerals_subtitle": "Mineralienportfolio mit Analyse-, Herkunfts- und Versanddokumenten auf verifizierte Anfrage.",
        "food_subtitle": "Lebensmittelprodukte für Großhandel, Industrie und Export mit Spezifikationen nach Käuferanforderung.",
        "intro_title": "Käuferinformationen",
        "intro_full": "Dieser Katalog dient als kompakte Erstprüfung für Einkaufsteams. Technische Detailwerte, COA, Analyseberichte, Herkunftsnachweise und Versanddokumente sind vorhanden und werden nach Käuferverifizierung projektbezogen geteilt.",
        "intro_minerals": "Die Mineralienübersicht zeigt die verfügbaren Rohstoffe, typische industrielle Anwendungen und den dokumentierten Einkaufsprozess. Sensible Analysewerte werden nicht vollständig im öffentlichen PDF veröffentlicht.",
        "intro_food": "Die Lebensmittelübersicht fasst die verfügbaren Produktgruppen zusammen. Spezifikation, Verpackung, Herkunftsunterlagen und Lieferdokumente werden je nach Käuferanforderung vorbereitet.",
        "note_title": "Analysebericht vorhanden",
        "note": "Alle gelisteten Produkte verfügen über einen Analysebericht und ein relevantes Dokumentenpaket. Öffentliche PDFs zeigen bewusst nur eine sichere Übersicht; detaillierte Dateien werden direkt per E-Mail geteilt.",
        "section_products": "Produktübersicht",
        "labels": {
            "main": "Hauptbestandteil",
            "quality": "Qualität",
            "form": "Lieferform",
            "packaging": "Verpackung",
            "docs": "Dokumente",
            "apps": "Anwendungen",
        },
        "quality": "Analysebericht verfügbar",
        "docs_minerals": "Analysebericht, COA, Herkunft und Versandpapiere auf Anfrage verfügbar",
        "docs_food": "Analysebericht, Spezifikation, Herkunft und Versandpapiere auf Anfrage verfügbar",
        "contact_title": "Dokumente oder Angebot anfordern",
        "contact_text": "Senden Sie Produkt, Menge, Zielhafen und gewünschte Dokumente. KMZ Trade teilt die passende Datei nach Käuferprüfung.",
        "footer": "KMZ Trade | info@kmztrade.com | Im Krämer 12, 61169 Friedberg | kmztrade.com",
    },
    "en": {
        "language_name": "English",
        "version": "2026 Edition",
        "public": "Public buyer overview",
        "full_title": "KMZ Trade Full Catalog",
        "minerals_title": "KMZ Trade Minerals Catalog",
        "food_title": "KMZ Trade Food Catalog",
        "full_subtitle": "Industrial minerals, edible oils and sugar for international buyers, supported by structured documentation and controlled sourcing.",
        "minerals_subtitle": "Minerals portfolio with assay, origin and shipment documentation available for verified buyer requests.",
        "food_subtitle": "Food products for wholesale, industry and export with specifications aligned to buyer requirements.",
        "intro_title": "Buyer information",
        "intro_full": "This catalog gives purchasing teams a concise first review. Technical details, COA, assay reports, origin records and shipment documents are available and shared project by project after buyer verification.",
        "intro_minerals": "The minerals overview presents available commodities, typical industrial uses and the documented sourcing process. Sensitive assay details are intentionally not fully published in the public PDF.",
        "intro_food": "The food overview summarizes available product groups. Specification, packaging, origin records and shipment documentation are prepared according to buyer requirements.",
        "note_title": "Analysis report available",
        "note": "Every listed product has an analysis report and a relevant document pack available. Public PDFs show a safe summary only; detailed files are shared directly by email.",
        "section_products": "Product overview",
        "labels": {
            "main": "Main component",
            "quality": "Quality basis",
            "form": "Delivery form",
            "packaging": "Packaging",
            "docs": "Documents",
            "apps": "Applications",
        },
        "quality": "Analysis report available",
        "docs_minerals": "Analysis report, COA, origin and shipment papers available on request",
        "docs_food": "Analysis report, specification, origin and shipment papers available on request",
        "contact_title": "Request documents or quotation",
        "contact_text": "Send product, quantity, destination port and required documents. KMZ Trade shares the relevant file after buyer review.",
        "footer": "KMZ Trade | info@kmztrade.com | Im Krämer 12, 61169 Friedberg | kmztrade.com",
    },
    "tr": {
        "language_name": "Türkçe",
        "version": "2026 Baskısı",
        "public": "Açık alıcı özeti",
        "full_title": "KMZ Trade Tam Katalog",
        "minerals_title": "KMZ Trade Maden Kataloğu",
        "food_title": "KMZ Trade Gıda Kataloğu",
        "full_subtitle": "Uluslararası alıcılar için endüstriyel madenler, yemeklik yağlar ve şeker; düzenli dokümantasyon ve kontrollü tedarik süreciyle sunulur.",
        "minerals_subtitle": "Doğrulanmış alıcı talepleri için analiz, menşe ve sevkiyat belgeleri mevcut maden portföyü.",
        "food_subtitle": "Toptan satış, sanayi ve ihracat için alıcı talebine göre spesifikasyonu düzenlenen gıda ürünleri.",
        "intro_title": "Alıcı bilgisi",
        "intro_full": "Bu katalog satın alma ekipleri için kısa ve güvenli bir ilk inceleme dokümanıdır. Teknik detaylar, COA, analiz raporları, menşe kayıtları ve sevkiyat evrakları mevcut olup alıcı doğrulamasından sonra proje bazlı paylaşılır.",
        "intro_minerals": "Maden özeti mevcut ürünleri, tipik endüstriyel kullanım alanlarını ve belgeli tedarik sürecini gösterir. Hassas analiz detayları açık PDF içinde bilinçli olarak tam yayımlanmaz.",
        "intro_food": "Gıda özeti mevcut ürün gruplarını gösterir. Spesifikasyon, ambalaj, menşe kayıtları ve sevkiyat belgeleri alıcı ihtiyacına göre hazırlanır.",
        "note_title": "Analiz raporu mevcut",
        "note": "Listelenen tüm ürünler için analiz raporu ve ilgili belge paketi mevcuttur. Açık PDF'ler yalnızca güvenli bir özet sunar; detaylı dosyalar e-posta ile doğrudan paylaşılır.",
        "section_products": "Ürün özeti",
        "labels": {
            "main": "Ana bileşen",
            "quality": "Kalite temeli",
            "form": "Teslim formu",
            "packaging": "Ambalaj",
            "docs": "Belgeler",
            "apps": "Kullanım alanları",
        },
        "quality": "Analiz raporu mevcut",
        "docs_minerals": "Analiz raporu, COA, menşe ve sevkiyat evrakları talep üzerine mevcut",
        "docs_food": "Analiz raporu, spesifikasyon, menşe ve sevkiyat evrakları talep üzerine mevcut",
        "contact_title": "Belge veya teklif talep edin",
        "contact_text": "Ürün, miktar, varış limanı ve istenen belgeleri iletin. KMZ Trade ilgili dosyayı alıcı kontrolünden sonra paylaşır.",
        "footer": "KMZ Trade | info@kmztrade.com | Im Krämer 12, 61169 Friedberg | kmztrade.com",
    },
}


def t(de, en, tr):
    return {"de": de, "en": en, "tr": tr}


def product(key, image, formula, main, form, packaging, apps, name, desc):
    return {
        "key": key,
        "image": image,
        "formula": formula,
        "main": main,
        "form": form,
        "packaging": packaging,
        "apps": apps,
        "name": name,
        "desc": desc,
    }


MINERALS = [
    product("manganese", "manganese-ore.jpg", "Mn", t("Manganerz", "Manganese ore", "Manganez cevheri"), t("Erz / Konzentrat", "Ore / concentrate", "Cevher / konsantre"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Stahl, Legierungen, Batterie-Vorprodukte", "Steel, alloys, battery precursors", "Çelik, alaşımlar, batarya ön ürünleri"), t("Manganerz", "Manganese Ore", "Manganez Cevheri"), t("Manganerz für Stahl, Ferrolegierungen und Batterie-Vorprodukte; lieferbar nach Analysezertifikat, Herkunftsnachweis und vereinbarter Körnung.", "Manganese ore for steel, ferroalloys and battery precursor supply, available with analysis certificate, origin documents and agreed sizing.", "Çelik, ferro alaşım ve batarya ön ürünleri için manganez cevheri; analiz sertifikası, menşe belgesi ve istenen tane boyutuyla tedarik edilir.")),
    product("zirconium", "zirconium-sand.jpg", "ZrSiO4", t("Zirconium", "Zirconium", "Zirconium"), t("Mineralischer Rohstoff", "Mineral raw material", "Mineral hammadde"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Keramik, Gießerei, Refraktär", "Ceramics, foundry, refractory", "Seramik, döküm, refrakter"), t("Zirconium", "Zirconium", "Zirconium"), t("Zirconiumhaltiger Rohstoff für Keramik, Gießerei, Refraktärproduktion und technische Anwendungen mit dokumentierter Analyse.", "Zirconium-bearing raw material for ceramics, foundry, refractory production and technical applications with documented analysis.", "Seramik, döküm, refrakter üretimi ve teknik uygulamalar için belgeli analizle sunulan zirconium içerikli hammadde.")),
    product("silicate", "zirconium-sand.jpg", "ZrHfO2", t("Zirconium Silicate", "Zirconium Silicate", "Zirconium Silicate"), t("Konzentrat / Mineralsand", "Concentrate / mineral sand", "Konsantre / mineral kumu"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Keramik, Glasuren, Hochtemperatur", "Ceramics, glazes, high temperature", "Seramik, sır, yüksek sıcaklık"), t("Zirconium Silicate", "Zirconium Silicate", "Zirconium Silicate"), t("Zirkonium-Silikat-Konzentrat für Keramik, Glasuren, Gießerei und Hochtemperaturanwendungen mit dokumentierter Qualität.", "Zirconium silicate concentrate for ceramics, glazes, foundry and high-temperature applications with documented quality.", "Seramik, sır, döküm ve yüksek sıcaklık uygulamaları için belgeli kaliteyle sunulan zirkonyum silikat konsantresi.")),
    product("titanium", "titanium-tio2.jpg", "TiO2", t("Titanium TiO2", "Titanium TiO2", "Titanium TiO2"), t("Rohstoff / Konzentrat", "Raw material / concentrate", "Hammadde / konsantre"), t("Projektbezogene Mengen", "Project-based volumes", "Proje bazlı miktarlar"), t("Pigmente, Beschichtungen, Kunststoffe", "Pigments, coatings, plastics", "Pigment, kaplama, plastik"), t("Titanium TiO2", "Titanium TiO2", "Titanium TiO2"), t("Titandioxid-Rohstoff für Pigmente, Beschichtungen, Kunststoffe und industrielle Weiterverarbeitung nach Käuferanforderung.", "Titanium dioxide feedstock for pigments, coatings, plastics and downstream industrial processing according to buyer requirements.", "Pigment, kaplama, plastik ve ileri endüstriyel işleme için alıcı talebine göre sunulan titanyum dioksit hammaddesi.")),
    product("columbite", "columbite.jpg", "NbTa2O5", t("Columbit", "Columbite", "Columbite"), t("Erz / Konzentrat", "Ore / concentrate", "Cevher / konsantre"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Elektronik, Superlegierung, Niob", "Electronics, superalloys, niobium", "Elektronik, süper alaşım, niyobyum"), t("Columbit", "Columbite", "Columbite"), t("Niob-Tantal-haltiges Erz für Spezialmetalle, Elektronikkomponenten und hochfeste Legierungsanwendungen.", "Niobium-tantalum bearing ore for specialty metals, electronic components and high-strength alloy applications.", "Özel metaller, elektronik bileşenler ve yüksek dayanımlı alaşımlar için niyobyum-tantal içeren cevher.")),
    product("tin", "tin-ore.jpg", "Sn", t("Zinnerz", "Tin ore", "Kalay cevheri"), t("Erz / Kassiterit-Konzentrat", "Ore / cassiterite concentrate", "Cevher / kasiterit konsantresi"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Metallurgie, Lötmittel, Legierungen", "Metallurgy, solder, alloys", "Metalurji, lehim, alaşımlar"), t("Zinnerz", "Tin Ore", "Kalay Cevheri"), t("Zinnerz und Kassiterit-Konzentrat für Metallurgie, Lötmittel, Legierungen und industrielle Rohstoffbeschaffung.", "Tin ore and cassiterite concentrate for metallurgy, solder, alloys and industrial raw material sourcing.", "Metalurji, lehim, alaşım ve endüstriyel hammadde tedariki için kalay cevheri ve kasiterit konsantresi.")),
    product("monazite", "monazite-ore.jpg", "(Ce,La,Nd,Th)PO4", t("Monazit", "Monazite", "Monazite"), t("Mineralsand / Konzentrat", "Mineral sand / concentrate", "Mineral kumu / konsantre"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Seltene Erden, Technologie, Industrie", "Rare earths, technology, industry", "Nadir topraklar, teknoloji, sanayi"), t("Monazit Erz", "Monazite Ore", "Monazite Cevheri"), t("Monazit-Konzentrat mit seltenen Erden für spezialisierte industrielle Abnehmer; Lieferung mit geprüfter Dokumentation.", "Monazite concentrate containing rare earth elements for specialized industrial buyers, supplied with verified documentation.", "Nadir toprak elementleri içeren monazite konsantresi; uzman endüstriyel alıcılar için doğrulanmış belgelerle tedarik edilir.")),
    product("lanthanum", "rare-earth-elements.jpg", "La", t("Lanthan", "Lanthanum", "Lantanyum"), t("Seltene-Erden-Rohstoff", "Rare earth raw material", "Nadir toprak hammaddesi"), t("Auf Anfrage", "On request", "Talep üzerine"), t("Katalysatoren, Spezialglas, Metallurgie", "Catalysts, specialty glass, metallurgy", "Katalizör, özel cam, metalurji"), t("Lanthan", "Lanthanum", "Lantanyum"), t("Lanthan-haltige Seltene-Erden-Rohstoffe für Katalysatoren, Spezialglas, Metallurgie und technische Anwendungen.", "Lanthanum-bearing rare earth raw materials for catalysts, specialty glass, metallurgy and technical applications.", "Katalizör, özel cam, metalurji ve teknik uygulamalar için lantanyum içeren nadir toprak hammaddeleri.")),
    product("cerium", "rare-earth-elements.jpg", "Ce", t("Cer", "Cerium", "Seryum"), t("Seltene-Erden-Rohstoff", "Rare earth raw material", "Nadir toprak hammaddesi"), t("Auf Anfrage", "On request", "Talep üzerine"), t("Poliermittel, Katalysatoren, Glas", "Polishing, catalysts, glass", "Parlatma, katalizör, cam"), t("Cer", "Cerium", "Seryum"), t("Cer-haltige Seltene-Erden-Rohstoffe für Poliermittel, Katalysatoren, Glasindustrie und Spezialchemie.", "Cerium-bearing rare earth raw materials for polishing compounds, catalysts, glass production and specialty chemistry.", "Parlatma bileşikleri, katalizörler, cam üretimi ve özel kimya için seryum içeren nadir toprak hammaddeleri.")),
    product("praseodymium", "rare-earth-elements.jpg", "Pr", t("Praseodym", "Praseodymium", "Praseodymium"), t("Seltene-Erden-Rohstoff", "Rare earth raw material", "Nadir toprak hammaddesi"), t("Auf Anfrage", "On request", "Talep üzerine"), t("Magnete, Legierungen, Pigmente", "Magnets, alloys, pigments", "Mıknatıs, alaşım, pigment"), t("Praseodym", "Praseodymium", "Praseodymium"), t("Praseodym-haltige Seltene-Erden-Rohstoffe für Magnete, Legierungen, Pigmente und technische Komponenten.", "Praseodymium-bearing rare earth raw materials for magnets, alloys, pigments and technical components.", "Mıknatıs, alaşım, pigment ve teknik komponentler için praseodymium içeren nadir toprak hammaddeleri.")),
    product("gadolinium", "rare-earth-elements.jpg", "Gd", t("Gadolinium", "Gadolinium", "Gadolinyum"), t("Seltene-Erden-Rohstoff", "Rare earth raw material", "Nadir toprak hammaddesi"), t("Auf Anfrage", "On request", "Talep üzerine"), t("Speziallegierungen, Magnetmaterialien", "Special alloys, magnetic materials", "Özel alaşım, manyetik malzeme"), t("Gadolinium", "Gadolinium", "Gadolinyum"), t("Gadolinium-haltige Seltene-Erden-Rohstoffe für Speziallegierungen, Magnetmaterialien und technische Anwendungen.", "Gadolinium-bearing rare earth raw materials for specialty alloys, magnetic materials and technical applications.", "Özel alaşımlar, manyetik malzemeler ve teknik uygulamalar için gadolinyum içeren nadir toprak hammaddeleri.")),
    product("lithium", "lithium-ore.jpg", "Li", t("Lithium", "Lithium", "Lityum"), t("Erz / Spodumen-Konzentrat", "Ore / spodumene concentrate", "Cevher / spodümen konsantresi"), t("Projektbezogene Mengen", "Project-based volumes", "Proje bazlı miktarlar"), t("Batterie-Vorprodukte, Keramik", "Battery precursors, ceramics", "Batarya ön ürünleri, seramik"), t("Lithium", "Lithium", "Lityum"), t("Lithiumhaltiges Erz und Spodumen-Konzentrat für Batterie-Vorprodukte, Keramik und technische Lieferketten.", "Lithium-bearing ore and spodumene concentrate for battery precursors, ceramics and technical supply chains.", "Batarya ön ürünleri, seramik ve teknik tedarik zincirleri için lityum içeren cevher ve spodümen konsantresi.")),
    product("barite", "barite.jpg", "BaSO4", t("Baryt", "Barite", "Barit"), t("Mineral / Pulver oder Stückgut", "Mineral / powder or lump", "Mineral / toz veya parça"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Bohrflüssigkeiten, Füllstoffe, Beschichtungen", "Drilling fluids, fillers, coatings", "Sondaj çamuru, dolgu, kaplama"), t("Baryt", "Barite", "Barit"), t("Baryt für Bohrflüssigkeiten, Füllstoffe, Beschichtungen und industrielle Anwendungen mit prüfbarer Spezifikation.", "Barite for drilling fluids, fillers, coatings and industrial applications with verifiable specification.", "Sondaj çamuru, dolgu, kaplama ve endüstriyel uygulamalar için doğrulanabilir spesifikasyonla sunulan barit.")),
    product("copper", "copper-ore.jpg", "Cu", t("Kupfererz", "Copper ore", "Bakır cevheri"), t("Erz / Konzentrat", "Ore / concentrate", "Cevher / konsantre"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Metallurgie, Kabel, Legierungen", "Metallurgy, cable, alloys", "Metalurji, kablo, alaşım"), t("Kupfererz", "Copper Ore", "Bakır Cevheri"), t("Kupfererz und Kupferkonzentrat für Metallurgie, Kabelindustrie, Legierungen und industrielle Weiterverarbeitung.", "Copper ore and copper concentrate for metallurgy, cable industry, alloys and downstream industrial processing.", "Metalurji, kablo sanayi, alaşımlar ve ileri endüstriyel işleme için bakır cevheri ve bakır konsantresi.")),
    product("fluorite", "fluorite.jpg", "CaF2", t("Fluorit", "Fluorite", "Fluorit"), t("Mineral / Konzentrat", "Mineral / concentrate", "Mineral / konsantre"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Stahl, Chemie, Glas, Keramik", "Steel, chemicals, glass, ceramics", "Çelik, kimya, cam, seramik"), t("Fluorit", "Fluorite", "Fluorit"), t("Fluorit für Stahl, Chemie, Glas, Keramik und Flusssäure-nahe industrielle Anwendungen mit Analyseunterlagen.", "Fluorite for steel, chemicals, glass, ceramics and hydrofluoric-acid-adjacent industrial applications with assay documents.", "Çelik, kimya, cam, seramik ve hidroflorik asit bağlantılı endüstriyel uygulamalar için analiz belgeli fluorit.")),
    product("feldspar", "feldspar.jpg", "K/Na", t("Feldspat", "Feldspar", "Feldspat"), t("Mineral / Körnung nach Anfrage", "Mineral / sizing by request", "Mineral / talebe göre tane boyutu"), t("Bulk oder Big Bag", "Bulk or Big Bag", "Bulk veya Big Bag"), t("Keramik, Glas, Füllstoffe", "Ceramics, glass, fillers", "Seramik, cam, dolgu"), t("Feldspat", "Feldspar", "Feldspat"), t("Feldspat für Keramik, Glas, Füllstoffe und Baustoffe mit abgestimmter Körnung und Lieferform.", "Feldspar for ceramics, glass, fillers and construction materials with agreed sizing and delivery form.", "Seramik, cam, dolgu ve yapı malzemeleri için tane boyutu ve teslim formu netleştirilmiş feldspat.")),
    product("coal", "coal.jpg", "Coal", t("Kohle", "Coal", "Kömür"), t("Industriekohle", "Industrial coal", "Endüstriyel kömür"), t("Projektbezogene Mengen", "Project-based volumes", "Proje bazlı miktarlar"), t("Energie, Prozesswärme, Rohstoffbedarf", "Energy, process heat, raw material demand", "Enerji, proses ısısı, hammadde ihtiyacı"), t("Kohle", "Coal", "Kömür"), t("Kohle für industrielle Energie, Prozesswärme und Rohstoffbedarf; Qualität und Logistik werden projektbezogen abgestimmt.", "Coal for industrial energy, process heat and raw material demand; quality and logistics are aligned per project.", "Endüstriyel enerji, proses ısısı ve hammadde ihtiyacı için kömür; kalite ve lojistik proje bazında netleştirilir.")),
]


FOOD = [
    product("sunflower", "sunflower-oil.jpg", "Food grade", t("Raffiniertes Sonnenblumenöl", "Refined sunflower oil", "Rafine ayçiçek yağı"), t("0.5 lt, 1 lt, 2 lt, 3 lt, 5 lt, 20 lt", "0.5 lt, 1 lt, 2 lt, 3 lt, 5 lt, 20 lt", "0.5 lt, 1 lt, 2 lt, 3 lt, 5 lt, 20 lt"), t("Flasche, Kanister, IBC, Flexitank", "Bottle, jerrycan, IBC, flexitank", "Şişe, bidon, IBC, flexitank"), t("Lebensmittelindustrie, Großhandel, Gastronomie", "Food industry, wholesale, gastronomy", "Gıda sanayi, toptan satış, gastronomi"), t("Sonnenblumenöl", "Sunflower Oil", "Ayçiçek Yağı"), t("Raffiniertes Sonnenblumenöl für Lebensmittelindustrie, Großhandel und Gastronomie; verfügbar in 0.5 lt, 1 lt, 2 lt, 3 lt, 5 lt und 20 lt.", "Refined sunflower oil for food industry, wholesale and gastronomy; available in 0.5 lt, 1 lt, 2 lt, 3 lt, 5 lt and 20 lt.", "Gıda sanayi, toptan ticaret ve gastronomi için rafine ayçiçek yağı; 0.5 lt, 1 lt, 2 lt, 3 lt, 5 lt ve 20 lt ambalaj seçenekleriyle sunulur.")),
    product("palm", "palm-oil.jpg", "Food / industrial grade", t("Palmöl", "Palm oil", "Palm yağı"), t("Nach Käuferanforderung", "By buyer requirement", "Alıcı ihtiyacına göre"), t("Flexitank, IBC oder Bulk", "Flexitank, IBC or bulk", "Flexitank, IBC veya bulk"), t("Lebensmittel, Kosmetik, Weiterverarbeitung", "Food, cosmetics, further processing", "Gıda, kozmetik, ileri işleme"), t("Palmöl", "Palm Oil", "Palm Yağı"), t("Palmöl für industrielle Lebensmittelproduktion, Kosmetik und Weiterverarbeitung; Beschaffung und Dokumentation nach Kundenvorgabe.", "Palm oil for industrial food production, cosmetics and further processing, with sourcing and documentation aligned to customer requirements.", "Endüstriyel gıda üretimi, kozmetik ve ileri işleme için palm yağı; kaynak ve belge süreçleri müşteri ihtiyacına göre düzenlenir.")),
    product("olive", "olive-oil.jpg", "Food grade", t("Olivenöl", "Olive oil", "Zeytinyağı"), t("Nach Käuferanforderung", "By buyer requirement", "Alıcı ihtiyacına göre"), t("Flasche, Kanister, IBC oder Bulk", "Bottle, jerrycan, IBC or bulk", "Şişe, bidon, IBC veya bulk"), t("Lebensmittelhandel, Gastronomie, Abfüllung", "Food trade, gastronomy, bottling", "Gıda ticareti, gastronomi, dolum"), t("Olivenöl", "Olive Oil", "Zeytinyağı"), t("Olivenöl für Lebensmittelhandel, Gastronomie und Abfüllprojekte; Spezifikation, Verpackung und Herkunft werden nach Käuferbedarf abgestimmt.", "Olive oil for food trade, gastronomy and bottling projects; specification, packaging and origin are aligned to buyer requirements.", "Gıda ticareti, gastronomi ve dolum projeleri için zeytinyağı; spesifikasyon, ambalaj ve menşe alıcı talebine göre netleştirilir.")),
    product("rapeseed", "rapeseed-oil.jpg", "Food grade", t("Rapsöl", "Rapeseed oil", "Kanola yağı"), t("Nach Käuferanforderung", "By buyer requirement", "Alıcı ihtiyacına göre"), t("Flasche, Kanister, IBC oder Flexitank", "Bottle, jerrycan, IBC or flexitank", "Şişe, bidon, IBC veya flexitank"), t("Lebensmittelindustrie, Großhandel, technische Anwendungen", "Food industry, wholesale, technical applications", "Gıda sanayi, toptan satış, teknik uygulamalar"), t("Rapsöl", "Rapeseed Oil", "Kanola Yağı"), t("Raps- bzw. Kanolaöl für Lebensmittelindustrie, Großhandel und technische Anwendungen mit flexiblem Verpackungskonzept.", "Rapeseed / canola oil for the food industry, wholesale and technical applications with flexible packaging concepts.", "Gıda sanayi, toptan satış ve teknik uygulamalar için esnek ambalaj seçenekleriyle kanola/raps yağı.")),
    product("sugar", "sugar.jpg", "ICUMSA 45", t("ICUMSA 45 Zucker", "ICUMSA 45 sugar", "ICUMSA 45 şeker"), t("Ursprung Brasilien", "Origin Brazil", "Menşe Brezilya"), t("Säcke, Big Bag oder Containerladung", "Bags, Big Bag or container load", "Çuval, Big Bag veya konteyner yükleme"), t("Lebensmittelindustrie, Großhandel, Export", "Food industry, wholesale, export", "Gıda sanayi, toptan satış, ihracat"), t("ICUMSA 45 Zucker", "ICUMSA 45 Sugar", "ICUMSA 45 Şeker"), t("Weißer ICUMSA 45 Zucker mit Ursprung Brasilien für Lebensmittelindustrie, Großhandel und Export; Verpackung und Dokumente nach Käuferanforderung.", "White ICUMSA 45 sugar of Brazil origin for the food industry, wholesale and export; packaging and documents follow buyer requirements.", "Brezilya menşeli beyaz ICUMSA 45 şeker; gıda sanayi, toptan satış ve ihracat için ambalaj ve belgeler alıcı talebine göre hazırlanır.")),
]


def draw_background(canvas, doc, strings, catalog_label):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, width, height, stroke=0, fill=1)

    canvas.setStrokeColor(colors.Color(0.83, 0.66, 0.33, alpha=0.16))
    canvas.setLineWidth(0.4)
    for offset in (40, 160, 280, 400, 520):
        canvas.line(offset, 0, offset + 170, height)

    canvas.saveState()
    try:
        canvas.setFillAlpha(0.045)
    except AttributeError:
        pass
    canvas.setFillColor(GOLD)
    canvas.setFont(FONT_BOLD, 72)
    canvas.translate(width / 2, height / 2)
    canvas.rotate(32)
    canvas.drawCentredString(0, 0, "KMZ TRADE")
    canvas.restoreState()

    canvas.setFillColor(CREAM)
    canvas.setFont(FONT_BOLD, 11)
    canvas.drawCentredString(13.5 * mm, height - 17.4 * mm, "KMZ")
    canvas.setFillColor(GOLD)
    canvas.circle(13.5 * mm, height - 14.5 * mm, 6.5 * mm, stroke=1, fill=0)
    canvas.setFillColor(CREAM)
    canvas.setFont(FONT_BOLD, 10)
    canvas.drawString(27 * mm, height - 18 * mm, "TRADE")

    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_REGULAR, 7.6)
    canvas.drawRightString(width - 18 * mm, height - 17 * mm, f"{catalog_label} | {strings['language_name']}")
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, height - 25 * mm, width - 18 * mm, height - 25 * mm)

    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_REGULAR, 7.4)
    canvas.drawString(18 * mm, 13 * mm, strings["footer"])
    canvas.drawRightString(width - 18 * mm, 13 * mm, f"{doc.page}")
    canvas.restoreState()


def cover_block(strings, title_key, subtitle_key, styles):
    title = strings[title_key]
    subtitle = strings[subtitle_key]
    cells = [
        [
            paragraph(strings["public"], styles["cover_badge"]),
            paragraph(strings["version"], styles["cover_badge"]),
        ],
        [
            paragraph(strings["note_title"], styles["contact"]),
            paragraph(strings["language_name"], styles["contact"]),
        ],
    ]
    table = Table(cells, colWidths=[74 * mm, 74 * mm], rowHeights=[12 * mm, 18 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                ("BOX", (0, 0), (-1, -1), 0.7, GOLD_DARK),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    return [
        Spacer(1, 72 * mm),
        paragraph("KMZ TRADE", styles["cover_badge"]),
        paragraph(title, styles["cover_title"]),
        paragraph(subtitle, styles["cover_subtitle"]),
        Spacer(1, 12 * mm),
        table,
        Spacer(1, 20 * mm),
        note_box(strings["note_title"], strings["note"], styles),
    ]


def note_box(title, text, styles):
    content = [
        paragraph(title, styles["h2"]),
        paragraph(text, styles["body_light"]),
    ]
    table = Table([[content]], colWidths=[170 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PANEL_2),
                ("BOX", (0, 0), (-1, -1), 0.75, GOLD_DARK),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return table


def intro_section(strings, catalog_type, styles):
    intro_key = {
        "full": "intro_full",
        "minerals": "intro_minerals",
        "food": "intro_food",
    }[catalog_type]
    return [
        paragraph(strings["intro_title"], styles["h1"]),
        paragraph(strings[intro_key], styles["body"]),
        Spacer(1, 7 * mm),
        note_box(strings["note_title"], strings["note"], styles),
        Spacer(1, 9 * mm),
        paragraph(strings["section_products"], styles["h1"]),
    ]


def product_card(product, lang, strings, styles, category):
    image_path = IMAGE_DIR / product["image"]
    image = Image(str(image_path), width=48 * mm, height=32 * mm)
    labels = strings["labels"]
    docs_key = "docs_food" if category == "food" else "docs_minerals"

    name_block = [
        paragraph(product["name"][lang], styles["card_title"]),
        paragraph(product["formula"], styles["formula"]),
        paragraph(product["desc"][lang], styles["body_light"]),
        Spacer(1, 3.2 * mm),
    ]

    rows = [
        [paragraph(labels["main"], styles["label"]), paragraph(product["main"][lang], styles["value"])],
        [paragraph(labels["quality"], styles["label"]), paragraph(strings["quality"], styles["value"])],
        [paragraph(labels["form"], styles["label"]), paragraph(product["form"][lang], styles["value"])],
        [paragraph(labels["packaging"], styles["label"]), paragraph(product["packaging"][lang], styles["value"])],
        [paragraph(labels["docs"], styles["label"]), paragraph(strings[docs_key], styles["value"])],
        [paragraph(labels["apps"], styles["label"]), paragraph(product["apps"][lang], styles["value"])],
    ]
    specs = Table(rows, colWidths=[26 * mm, 88 * mm])
    specs.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -2), 0.25, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    name_block.append(specs)

    card = Table([[image, name_block]], colWidths=[55 * mm, 121 * mm])
    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#26323d")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return KeepTogether([card, Spacer(1, 7 * mm)])


def contact_section(strings, styles):
    table = Table(
        [
            [paragraph(strings["contact_title"], styles["h2"])],
            [paragraph(strings["contact_text"], styles["body_light"])],
            [paragraph("Email: info@kmztrade.com   |   Address: Im Krämer 12, 61169 Friedberg", styles["contact"])],
        ],
        colWidths=[170 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PANEL_2),
                ("BOX", (0, 0), (-1, -1), 0.75, GOLD_DARK),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return [Spacer(1, 4 * mm), table]


def build_pdf(lang, catalog_type, products, title_key, subtitle_key, output_path):
    strings = TEXT[lang]
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=33 * mm,
        bottomMargin=25 * mm,
        title=strings[title_key],
        author="KMZ Trade",
        subject="Buyer catalog",
    )

    story = []
    story.extend(cover_block(strings, title_key, subtitle_key, styles))
    story.append(PageBreak())
    story.extend(intro_section(strings, catalog_type, styles))
    story.append(Spacer(1, 3 * mm))

    for product in products:
        category = "food" if product in FOOD else "minerals"
        story.append(product_card(product, lang, strings, styles, category))

    story.extend(contact_section(strings, styles))

    catalog_label = strings[title_key]
    doc.build(
        story,
        onFirstPage=lambda canvas, d: draw_background(canvas, d, strings, catalog_label),
        onLaterPages=lambda canvas, d: draw_background(canvas, d, strings, catalog_label),
    )


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    catalogs = {
        "full": (MINERALS + FOOD, "full_title", "full_subtitle"),
        "minerals": (MINERALS, "minerals_title", "minerals_subtitle"),
        "food": (FOOD, "food_title", "food_subtitle"),
    }

    for lang in ("de", "en", "tr"):
        for catalog_type, (products, title_key, subtitle_key) in catalogs.items():
            output_path = OUT_DIR / f"kmz-trade-{catalog_type}-catalog-{lang}.pdf"
            build_pdf(lang, catalog_type, products, title_key, subtitle_key, output_path)

    # Keep the legacy file names as German defaults for old links and direct bookmarks.
    for catalog_type in catalogs:
        copyfile(
            OUT_DIR / f"kmz-trade-{catalog_type}-catalog-de.pdf",
            OUT_DIR / f"kmz-trade-{catalog_type}-catalog.pdf",
        )


if __name__ == "__main__":
    main()
