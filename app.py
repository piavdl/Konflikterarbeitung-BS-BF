# =====================================================================
# DIGITALE AUSWERTUNG BARRIEREFREIHEIT / BRANDSCHUTZ
# Universitäres Projekt - IPE RWTH Aachen (Sommersemester 2026)
# =====================================================================

import streamlit as st

# 1. Matplotlib IMMER vor allen anderen Imports konfigurieren
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

# 2. Dann erst die Daten-Bibliotheken
import pandas as pd
import re
import threading

# 3. Dann erst Streamlit Konfiguration
st.set_page_config(page_title="Digitale Auswertung", layout="wide")

_lock = threading.Lock()

# ---------------------------------------------------------------------
# PASSPORT-SCHUTZ BEREICH (ZUGANGSKONTROLLE)
# ---------------------------------------------------------------------
def pruefe_passwort():
    """Gibt True zurück, wenn das Passwort korrekt ist."""
    if "authentifiziert" not in st.session_state:
        st.session_state["authentifiziert"] = False

    if st.session_state["authentifiziert"]:
        return True

    # Login-Formular anzeigen
    st.markdown("<h2 style='color:#00549F;'>🔒 Geschützter Bereich</h2>", unsafe_allow_html=True)
    st.info("Dieses Prüftool ist im Rahmen eines universitären Projekts geschützt. Bitte gib das Passwort ein.")
    
    passwort = st.text_input("Passwort eingeben:", type="password")
    
    if st.button("Anmelden"):
        if passwort == "IPE_2026":
            st.session_state["authentifiziert"] = True
            st.rerun()
        else:
            st.error("❌ Falsches Passwort. Bitte versuche es erneut.")
            
    return False

# Falls nicht eingeloggt, stoppt das Skript sofort hier
if not pruefe_passwort():
    st.stop()


# --------------------------------------------------
# RWTH Aachen Corporate Design & UI Optimization (CSS)
# --------------------------------------------------
st.markdown(
    """
    <style>
        /* 1. WICHTIG: Schriftart MUSS ganz oben geladen werden */
        @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css");

        /* 2. Hintergrund der Seitenleiste in original RWTH-Blau */
        [data-testid="stSidebar"] {
            background-color: #00549F !important;
        }
        
        /* Alle Texte in der Seitenleiste weiß machen */
        [data-testid="stSidebar"] .stMarkdown, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] h3, 
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span {
            color: #FFFFFF !important;
        }
        
        /* Die Info-Box in der Seitenleiste dezent transparent/weiß stylen */
        [data-testid="stSidebar"] .stAlert {
            background-color: rgba(255, 255, 255, 0.15) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
        }
        
        /* Trennlinien in der Seitenleiste */
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.3) !important;
        }
        
        /* Hauptseite: Titel farblich an RWTH-Blau anpassen */
        .rwth-title {
            color: #00549F;
            font-weight: 700;
            margin-top: -15px;
            margin-bottom: 0px;
        }
        
        /* Styling für die interaktiven Tabs (Text bleibt!) */
        button[data-baseweb="tab"] {
            font-size: 16px !important;
            font-weight: 600 !important;
        }
        button[aria-selected="true"] {
            color: #00549F !important;
            border-bottom-color: #00549F !important;
        }

        /* 3. ICONS AUTOMATISCH VOR DEN TEXT SETZEN */
        
        /* Icon für den 1. Tab (Dashboard & Indizes) */
        button[data-baseweb="tab"]:nth-of-type(1) p::before {
            content: "\\f4ca  "; /* Chart-Icon + Leerzeichen */
            font-family: "bootstrap-icons" !important;
            color: #00549F;
            font-weight: normal;
        }
        
        /* Icon für den 2. Tab (Detailbericht & Fazit) */
        button[data-baseweb="tab"]:nth-of-type(2) p::before {
            content: "\\f52a  "; /* Lupen-Icon + Leerzeichen */
            font-family: "bootstrap-icons" !important;
            color: #00549F;
            font-weight: normal;
        }
        
        /* Icon für den 3. Tab (Komplette Mängelliste) */
        button[data-baseweb="tab"]:nth-of-type(3) p::before {
            content: "\\f33a  "; /* Warnungs-Icon + Leerzeichen */
            font-family: "bootstrap-icons" !important;
            color: #00549F;
            font-weight: normal;
        }
        /* Icon vor der Überschrift der Gebäude-Analyse */
        .dashboard-title::before {
            content: "\\f431  "; /* Wichtiges Listen-Fakten-Icon */
            font-family: "bootstrap-icons" !important;
            color: #00549F; /* Original RWTH-Blau */
            font-weight: normal;
            margin-right: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HORIZONTALER HEADER: RWTH Logo & Titel
# --------------------------------------------------
col_logo, col_title = st.columns([1, 4])

with col_logo:
    try:
        st.image("RWTH_Aachen_Logo.svg", width=310)
    except:
        st.write("🏫 **RWTH Aachen**")

with col_title:
    st.markdown('<h1 class="rwth-title">Digitale Auswertung: Barrierefreiheit & Brandschutz</h1>', unsafe_allow_html=True)
    st.caption("Prüftool zur Konflikterarbeitung im Rahmen des universitären Projekts | IPE RWTH Aachen")

st.markdown("---")


# --------------------------------------------------
# SEITENLEISTE (SIDEBAR): RWTH Kursinformationen
# --------------------------------------------------
with st.sidebar:
    st.markdown("### Universitäres Projekt")
    st.info(
        """
        **Kurs:** Forschungsfeld: Digitale Konzepte für barrierefreies und sicheres Bauen  
        
        **Info:** Diese Website wurde im Rahmen eines Forschungsfeldes entwickelt und wird zu Lehrzwecken verwendet. 
        
        **Semester:** Sommersemester 2026  
        
        **Institut:** Lehr- und Forschungsgebiet für Immobilienprojektentwicklung IPE

        **Betreuung:** Univ.-Prof. Dr.-Ing. Elisabeth Beusker & Shihui Li, M.Sc. RWTH
        """
    )
    
    st.markdown("### Projektmitglieder")
    st.markdown(
        """
        * Victoria Steiger
        * Pia Vor der Landwehr
        """
    )
    
    st.markdown("---")
    st.caption("Stand: Juli 2026 | Version 1.2")


# --------------------------------------------------
# HAUPTSEITE: Interaktive Steuerung (Zentriert)
# --------------------------------------------------
st.markdown("### Datengrundlage & Analyse")

hochgeladene_datei = st.file_uploader(
    "1. Bitte lade hier deine Excel-Gebäudeanalyse hoch:", 
    type=["xlsx"]
)

auswahl_bauteil = st.selectbox(
    "2. Für welches Bauteil/System möchtest du den Detailbericht sehen?",
    ["Tür", "Flur", "Treppe", "Handlauf", "Rauchmelder", "Leitsystem"]
)

st.markdown("---")


# =====================================================================
# HILFSFUNKTIONEN & ALGORITHMEN
# =====================================================================

def finde_echten_spaltennamen(df_columns, gesuchter_name):
    """Sucht eine Spalte fehlertolerant."""
    if gesuchter_name is None or pd.isna(gesuchter_name):
        return None
    normalisierter_suchname = re.sub(r'\s+', ' ', str(gesuchter_name)).strip().lower()
    for spalte in df_columns:
        if re.sub(r'\s+', ' ', str(spalte)).strip().lower() == normalisierter_suchname:
            return spalte
    return None


def wert_aus_text(wert):
    """Bereinigt Text-Werte aus Excel und wandelt sie in Meter-Zahlen um."""
    if pd.isna(wert):
        return None
    text = str(wert).strip().lower()
    if text in ["", "-", "--", "nan", "none"]:
        return None
    text = text.replace(" ", "").replace(",", ".")

    if "-" in text:
        text = text.replace("cm", "").replace("m", "")
        teile = text.split("-")
        min_wert = float(teile[0])
        max_wert = float(teile[1])
        if min_wert > 5:
            min_wert = min_wert / 100
        max_wert = max_wert / 100
        return (min_wert, max_wert)

    text = text.replace("cm", "").replace("m", "")
    try:
        zahl = float(text)
        if zahl > 5:
            zahl = zahl / 100
        return zahl
    except ValueError:
        return None


def pruefe_ampel(ist, soll):
    """Vergleicht Ist- und Soll-Werte und gibt die passende Ampel zurück."""
    if ist is None or pd.isna(ist):
        return ""
    if soll is None:
        return ""
    if isinstance(soll, tuple):
        soll_min, soll_max = soll
        if soll_min <= ist <= soll_max:
            return "🟢"
        return "🔴"
    if pd.isna(soll):
        return ""
    if ist >= soll:
        return "🟢"
    return "🔴"


def pruefe_ja_nein(wert):
    """Prüft Ja/Nein-Kriterien wie Rauchmelder oder Leitsysteme."""
    if pd.isna(wert):
        return ""
    if str(wert).strip() in ["1", "1.0", "ja", "true", "x", "X"]:
        return "🟢"
    if str(wert).strip() in ["0", "0.0", "nein", "false"]:
        return "🔴"
    return ""


# =====================================================================
# HAUPTPROGRAMM (Wird ausgeführt, sobald eine Datei vorhanden ist)
# =====================================================================
# 1. Cache-Funktion zum sicheren Laden (OBEN im Skript platzieren, nach den Hilfsfunktionen)
@st.cache_data
def load_and_clean_data(file):
    # Einlesen mit Spaltenbegrenzung und automatischer Bereinigung
    df = pd.read_excel(file, header=2, usecols="A:AG")
    df = df.dropna(how="all")
    
    # Spaltennamen säubern (Zeilenumbrüche entfernen & Normalisieren)
    df.columns = [re.sub(r'\s+', ' ', str(c).replace('\n', ' ')).strip() for c in df.columns]
    
    if "Eigenschaft:" in df.columns:
        df = df.drop(columns=["Eigenschaft:"])
        
    if "Geschoss" in df.columns:
        df = df.dropna(subset=["Geschoss"])

    for col in df.columns:
        df[col] = df[col].replace(["-", " - ", "--", "", "nan", "None"], None)
        
    return df

# 2. HAUPTPROGRAMM (Hier den alten Block ersetzen)
if hochgeladene_datei is not None:
    try:
        # Daten über die Cache-Funktion laden
        df = load_and_clean_data(hochgeladene_datei)
        st.success("Datei erfolgreich und speicherschonend geladen!")
        
        # Bauteil-Erzeugung falls Spalte fehlt
        if "Bauteil" not in df.columns and "Raumbez." in df.columns:
            conditions = [
                df["Raumbez."].astype(str).str.contains("Flur|Korridor|Gang", case=False, na=False),
                df["Raumbez."].astype(str).str.contains("Treppe|TH|Treppenhaus", case=False, na=False),
                df["Tür-ID"].notna() & (df["Tür-ID"] != "None") & (df["Tür-ID"] != "")
            ]
            choices = ["Flur", "Treppe", "Tür"]
            df["Bauteil"] = pd.Series(pd.NA).astype(object)
            for cond, choice in zip(conditions, choices):
                df.loc[cond, "Bauteil"] = choice
            df["Bauteil"] = df["Bauteil"].fillna("Sonstiges")

        # Zahlenspalten erzeugen
        if "Türbreite Ist-Wert" in df.columns:
            df["Türbreite Ist"] = df["Türbreite Ist-Wert"].apply(wert_aus_text)
            df["Türbreite Soll BF"] = df["Türbreite Soll-Wert BF"].apply(wert_aus_text)
            df["Türbreite Soll BS"] = df["Türbreite Soll-Wert BS"].apply(wert_aus_text)

        if "Flurbreite Ist-Wert" in df.columns:
            df["Flurbreite Ist"] = df["Flurbreite Ist-Wert"].apply(wert_aus_text)
            df["Flurbreite Soll BF"] = df["Flurbreite Soll-Wert BF"].apply(wert_aus_text)
            df["Flurbreite Soll BS"] = df["Flurbreite Soll-Wert BS"].apply(wert_aus_text)

        if "Treppenbreite Ist-Wert" in df.columns:
            df["Treppenbreite Ist"] = df["Treppenbreite Ist-Wert"].apply(wert_aus_text)
            df["Treppenbreite Soll BF"] = df["Treppenbreite Soll-Wert BF"].apply(wert_aus_text)
            df["Treppenbreite Soll BS"] = df["Treppenbreite Soll-Wert BS"].apply(wert_aus_text)
            df["Auftrittsmaß Ist"] = df["Stufen Auftrittsmaß Ist-Wert"].apply(wert_aus_text)
            df["Auftrittsmaß Soll BF"] = df["Stufen Auftrittsmaß Soll-Wert BF"].apply(wert_aus_text)
            df["Auftrittsmaß Soll BS"] = df["Stufen Auftrittsmaß Soll-Wert BS"].apply(wert_aus_text)
            df["Steigungsmaß Ist"] = df["Stufen Steigungsmaß Ist-Wert"].apply(wert_aus_text)
            df["Steigungsmaß Soll BF"] = df["Stufen Steigungsmaß Soll-Wert BF"].apply(wert_aus_text)
            df["Steigungsmaß Soll BS"] = df["Stufen Steigungsmaß Soll-Wert BS"].apply(wert_aus_text)

        if "Anzahl Handläufe Ist-Wert" in df.columns:
            df["Anzahl Handläufe Ist"] = pd.to_numeric(df["Anzahl Handläufe Ist-Wert"], errors="coerce")
            df["Anzahl Handläufe Soll"] = pd.to_numeric(df["Anzahl Handläufe Soll-Wert"], errors="coerce")
            df["Höhe Handlauf Ist"] = df["Höhe Handlauf Ist-Wert"].apply(wert_aus_text)
            df["Höhe Handlauf Soll BF"] = df["Höhe Handlauf Soll-Wert BF"].apply(wert_aus_text)
            df["Höhe Handlauf Soll BS"] = df["Höhe Handlauf Soll-Wert BS"].apply(wert_aus_text)

        if "Rauchmelder" in df.columns:
            df["Rauchmelder Ist"] = pd.to_numeric(df["Rauchmelder"], errors="coerce")
        if "Leitsystem" in df.columns:
            df["Leitsystem Ist"] = pd.to_numeric(df["Leitsystem"], errors="coerce")

        # Regeltabelle definieren
        regeln = [
            {"Bauteil": "Tür", "Kriterium": "Türbreite", "ID-Spalte": "Tür-ID", "Ist-Spalte": "Türbreite Ist", "Soll-BF-Spalte": "Türbreite Soll BF", "Soll-BS-Spalte": "Türbreite Soll BS", "Ist-Anzeige": "Türbreite Ist-Wert", "Soll-BF-Anzeige": "Türbreite Soll-Wert BF", "Soll-BS-Anzeige": "Türbreite Soll-Wert BS", "Mangel-BF": "Türbreite nach Barrierefreiheit zu gering", "Mangel-BS": "Türbreite nach Brandschutz zu gering", "Pruefart": "vergleich"},
            {"Bauteil": "Flur", "Kriterium": "Flurbreite", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Flurbreite Ist", "Soll-BF-Spalte": "Flurbreite Soll BF", "Soll-BS-Spalte": "Flurbreite Soll BS", "Ist-Anzeige": "Flurbreite Ist-Wert", "Soll-BF-Anzeige": "Flurbreite Soll-Wert BF", "Soll-BS-Anzeige": "Flurbreite Soll-Wert BS", "Mangel-BF": "Flurbreite nach Barrierefreiheit zu gering", "Mangel-BS": "Flurbreite nach Brandschutz zu gering", "Pruefart": "vergleich"},
            {"Bauteil": "Treppe", "Kriterium": "Treppenbreite", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Treppenbreite Ist", "Soll-BF-Spalte": "Treppenbreite Soll BF", "Soll-BS-Spalte": "Treppenbreite Soll BS", "Ist-Anzeige": "Treppenbreite Ist-Wert", "Soll-BF-Anzeige": "Treppenbreite Soll-Wert BF", "Soll-BS-Anzeige": "Treppenbreite Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz", "Pruefart": "vergleich"},
            {"Bauteil": "Treppe", "Kriterium": "Auftrittsmaß", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Auftrittsmaß Ist", "Soll-BF-Spalte": "Auftrittsmaß Soll BF", "Soll-BS-Spalte": "Auftrittsmaß Soll BS", "Ist-Anzeige": "Stufen Auftrittsmaß Ist-Wert", "Soll-BF-Anzeige": "Stufen Auftrittsmaß Soll-Wert BF", "Soll-BS-Anzeige": "Stufen Auftrittsmaß Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz", "Pruefart": "vergleich"},
            {"Bauteil": "Treppe", "Kriterium": "Steigungsmaß", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Steigungsmaß Ist", "Soll-BF-Spalte": "Steigungsmaß Soll BF", "Soll-BS-Spalte": "Steigungsmaß Soll BS", "Ist-Anzeige": "Stufen Steigungsmaß Ist-Wert", "Soll-BF-Anzeige": "Stufen Steigungsmaß Soll-Wert BF", "Soll-BS-Anzeige": "Stufen Steigungsmaß Soll-Wert BS", "Mangel-BF": "Mangel Barrierefreiheit", "Mangel-BS": "Mangel Brandschutz", "Pruefart": "vergleich"},
            {"Bauteil": "Handlauf", "Kriterium": "Anzahl Handläufe", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Anzahl Handläufe Ist", "Soll-BF-Spalte": "Anzahl Handläufe Soll", "Soll-BS-Spalte": "Anzahl Handläufe Soll", "Ist-Anzeige": "Anzahl Handläufe Ist-Wert", "Soll-BF-Anzeige": "Anzahl Handläufe Soll-Wert", "Soll-BS-Anzeige": "Anzahl Handläufe Soll-Wert", "Mangel-BF": "Zu wenige Handläufe", "Mangel-BS": "Zu wenige Handläufe", "Pruefart": "vergleich"},
            {"Bauteil": "Handlauf", "Kriterium": "Höhe Handlauf", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Höhe Handlauf Ist", "Soll-BF-Spalte": "Höhe Handlauf Soll BF", "Soll-BS-Spalte": "Höhe Handlauf Soll BS", "Ist-Anzeige": "Höhe Handlauf Ist-Wert", "Soll-BF-Anzeige": "Höhe Handlauf Soll-Wert BF", "Soll-BS-Anzeige": "Höhe Handlauf Soll-Wert BS", "Mangel-BF": "Handlaufhöhe nicht ausreichend", "Mangel-BS": "Handlaufhöhe nicht ausreichend", "Pruefart": "vergleich"},
            {"Bauteil": "Rauchmelder", "Kriterium": "Rauchmelder vorhanden", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Rauchmelder Ist", "Soll-BF-Spalte": None, "Soll-BS-Spalte": None, "Ist-Anzeige": "Rauchmelder", "Soll-BF-Anzeige": None, "Soll-BS-Anzeige": None, "Mangel-BF": "Rauchmelder nicht vorhanden", "Mangel-BS": "Rauchmelder nicht vorhanden", "Pruefart": "ja_nein"},
            {"Bauteil": "Leitsystem", "Kriterium": "Leitsystem vorhanden", "ID-Spalte": "Raum-ID", "Ist-Spalte": "Leitsystem Ist", "Soll-BF-Spalte": None, "Soll-BS-Spalte": None, "Ist-Anzeige": "Leitsystem", "Soll-BF-Anzeige": None, "Soll-BS-Anzeige": None, "Mangel-BF": "Leitsystem nicht vorhanden", "Mangel-BS": "Leitsystem nicht vorhanden", "Pruefart": "ja_nein"}
        ]

        alle_ergebnisse = []

        for regel in regeln:
            ist_spalte_echt = finde_echten_spaltennamen(df.columns, regel["Ist-Spalte"])
            ist_anzeige_echt = finde_echten_spaltennamen(df.columns, regel["Ist-Anzeige"])
            
            if not ist_spalte_echt or not ist_anzeige_echt:
                continue
                
            teil_df = df[df[ist_spalte_echt].notna()].copy()
            if teil_df.empty:
                continue

            if regel.get("Pruefart") == "ja_nein":
                teil_df["Ampel Barrierefreiheit"] = teil_df[ist_spalte_echt].apply(pruefe_ja_nein)
                teil_df["Ampel Brandschutz"] = teil_df[ist_spalte_echt].apply(pruefe_ja_nein)
            else:
                soll_bf_echt = finde_echten_spaltennamen(df.columns, regel["Soll-BF-Spalte"])
                soll_bs_echt = finde_echten_spaltennamen(df.columns, regel["Soll-BS-Spalte"])
                
                teil_df["Ampel Barrierefreiheit"] = teil_df.apply(lambda row: pruefe_ampel(row[ist_spalte_echt], row[soll_bf_echt] if soll_bf_echt else None), axis=1)
                teil_df["Ampel Brandschutz"] = teil_df.apply(lambda row: pruefe_ampel(row[ist_spalte_echt], row[soll_bs_echt] if soll_bs_echt else None), axis=1)

            def konflikttext(row):
                maengel = []
                soll_bf_anzeige_echt = finde_echten_spaltennamen(df.columns, regel["Soll-BF-Anzeige"])
                soll_bs_anzeige_echt = finde_echten_spaltennamen(df.columns, regel["Soll-BS-Anzeige"])
                
                if row["Ampel Barrierefreiheit"] == "🔴":
                    text = f"{regel['Mangel-BF']} (Kategorie: {regel['Kriterium']}, Ist: {row[ist_anzeige_echt]}"
                    if soll_bf_anzeige_echt is not None:
                        text += f", Soll BF: {row[soll_bf_anzeige_echt]}"
                    text += ")"
                    maengel.append(text)

                if row["Ampel Brandschutz"] == "🔴":
                    text = f"{regel['Mangel-BS']} (Kategorie: {regel['Kriterium']}, Ist: {row[ist_anzeige_echt]}"
                    if soll_bs_anzeige_echt is not None:
                        text += f", Soll BS: {row[soll_bs_anzeige_echt]}"
                    text += ")"
                    maengel.append(text)
                return " | ".join(maengel)

            teil_df["Konflikt / Mangel"] = teil_df.apply(konflikttext, axis=1)

            soll_bf_anzeige_echt = finde_echten_spaltennamen(df.columns, regel["Soll-BF-Anzeige"])
            soll_bs_anzeige_echt = finde_echten_spaltennamen(df.columns, regel["Soll-BS-Anzeige"])
            soll_bf_anzeige_wert = teil_df[soll_bf_anzeige_echt] if soll_bf_anzeige_echt is not None else ""
            soll_bs_anzeige_wert = teil_df[soll_bs_anzeige_echt] if soll_bs_anzeige_echt is not None else ""

            ergebnis = pd.DataFrame({
                "Geschoss": teil_df["Geschoss"],
                "Wohneinheit": teil_df["Wohneinheit"],
                "Raumbez.": teil_df["Raumbez."],
                "Raum-ID": teil_df["Raum-ID"],
                "Bauteil": regel["Bauteil"],
                "Bauteil-ID": teil_df[regel["ID-Spalte"]],
                "Kriterium": regel["Kriterium"],
                "Ist-Wert": teil_df[ist_anzeige_echt],
                "Sollwert Barrierefreiheit": soll_bf_anzeige_wert,
                "Ampel Barrierefreiheit": teil_df["Ampel Barrierefreiheit"],
                "Sollwert Brandschutz": soll_bs_anzeige_wert,
                "Ampel Brandschutz": teil_df["Ampel Brandschutz"],
                "Konflikt / Mangel": teil_df["Konflikt / Mangel"]
            })
            alle_ergebnisse.append(ergebnis)

        if alle_ergebnisse:
            gesamtbericht = pd.concat(alle_ergebnisse, ignore_index=True)
            
            def bewertung_aus_ampeln(row):
                BF = row["Ampel Barrierefreiheit"]
                BS = row["Ampel Brandschutz"]
                if BF == "🟢" and BS == "🟢": return "kein Mangel"
                elif BF == "🔴" and BS == "🟢": return "Mangel Barrierefreiheit"
                elif BF == "🟢" and BS == "🔴": return "Mangel Brandschutz"
                elif BF == "🔴" and BS == "🔴": return "Mangel in Barrierefreiheit und Brandschutz"
                return ""

            gesamtbericht["Ergebnis"] = gesamtbericht.apply(bewertung_aus_ampeln, axis=1)
            gesamtbericht["Wohnung"] = gesamtbericht["Wohneinheit"].fillna("Treppenhaus")

            # Gruppierung für die Wohnungstabelle
            wohnungs_uebersicht = (
                gesamtbericht
                .groupby(["Wohnung", "Bauteil", "Bauteil-ID"], dropna=False)
                .agg({
                    "Ampel Barrierefreiheit": lambda x: "🔴" if "🔴" in list(x) else ("🟢" if "🟢" in list(x) else ""),
                    "Ampel Brandschutz": lambda x: "🔴" if "🔴" in list(x) else ("🟢" if "🟢" in list(x) else ""),
                    "Kriterium": lambda x: ", ".join(x.dropna().astype(str).unique())
                })
                .reset_index()
            )

            wohnungs_uebersicht = wohnungs_uebersicht.rename(columns={
                "Bauteil": "Kategorie", "Bauteil-ID": "ID", "Ampel Barrierefreiheit": "Ampel BF", "Ampel Brandschutz": "Ampel BS", "Kriterium": "Kriterien"
            })

            def gesamtampel(bf, bs):
                if bf == "🔴" and bs == "🔴": return "🔴"
                elif bf == "🔴" or bs == "🔴": return "🟡"
                elif bf == "🟢" and bs == "🟢": return "🟢"
                return ""

            wohnungs_uebersicht["Ampel Gesamt"] = wohnungs_uebersicht.apply(lambda row: gesamtampel(row["Ampel BF"], row["Ampel BS"]), axis=1)

            # Berechnung des Vulnerabilitätsindexes
            wohnungs_uebersicht_bewertet = wohnungs_uebersicht[wohnungs_uebersicht["Ampel Gesamt"] != ""].copy()
            vulnerabilitaet = (
                wohnungs_uebersicht_bewertet
                .groupby("Wohnung")["Ampel Gesamt"]
                .value_counts(normalize=True)
                .mul(100)
                .round(1)
                .unstack(fill_value=0)
                .reset_index()
            )

            for spalte in ["🟢", "🟡", "🔴"]:
                if spalte not in vulnerabilitaet.columns:
                    vulnerabilitaet[spalte] = 0

            vulnerabilitaet = vulnerabilitaet[["Wohnung", "🟢", "🟡", "🔴"]].rename(columns={"🟢": "Grün in %", "🟡": "Gelb in %", "🔴": "Rot in %"})
            vulnerabilitaet["Vulnerabilitätsindex"] = (vulnerabilitaet["Gelb in %"] * 1 + vulnerabilitaet["Rot in %"] * 2) / 2

            # --------------------------------------------------
            # TABS (DURCH CSS AUTOMATISCH MIT BI-ICONS GESTYLT)
            # --------------------------------------------------
            tab1, tab2, tab3 = st.tabs(["Dashboard & Indizes", "Detailbericht & Fazit", "Komplette Mängelliste"])

            # ---- REGISTERKARTE 1: DASHBOARD ----
            with tab1:
                st.markdown('<h3 class="dashboard-title">Gebäude-Analyse & Vulnerabilität</h3>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Vulnerabilitätsindex je Wohneinheit")
                    st.dataframe(vulnerabilitaet, use_container_width=True)
                
                with col2:
                    with _lock:
                        fig1, ax1 = plt.subplots(figsize=(6, 4))
                        ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Grün in %"], color="green", label="Grün")
                        ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Gelb in %"], bottom=vulnerabilitaet["Grün in %"], color="gold", label="Gelb")
                        ax1.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Rot in %"], bottom=vulnerabilitaet["Grün in %"] + vulnerabilitaet["Gelb in %"], color="red", label="Rot")
                        ax1.set_ylabel("Anteil [%]")
                        ax1.set_title("Ampelverteilung je Wohneinheit")
                        plt.xticks(rotation=45)
                        ax1.set_ylim(0, 100)
                        ax1.legend(loc="upper right")
                        st.pyplot(fig1)

                st.subheader("Visualisierung Vulnerabilitätsindex")
                with _lock:
                    fig2, ax2 = plt.subplots(figsize=(10, 3))
                    ax2.bar(vulnerabilitaet["Wohnung"], vulnerabilitaet["Vulnerabilitätsindex"], color="gray")
                    ax2.set_ylabel("Index-Wert")
                    plt.xticks(rotation=45)
                    st.pyplot(fig2)

            # ---- REGISTERKARTE 2: DETAILBERICHTE ----
            with tab2:
                st.header(f"Detailanalyse: {auswahl_bauteil}")
                
                bericht = gesamtbericht[gesamtbericht["Bauteil"] == auswahl_bauteil]
                anzahl = len(bericht)
                bf_gruen = (bericht["Ampel Barrierefreiheit"] == "🟢").sum()
                bf_rot = (bericht["Ampel Barrierefreiheit"] == "🔴").sum()
                bs_gruen = (bericht["Ampel Brandschutz"] == "🟢").sum()
                bs_rot = (bericht["Ampel Brandschutz"] == "🔴").sum()

                fazit = pd.DataFrame({
                    "Kennzahl": ["Geprüfte Elemente", "Barrierefreiheit erfüllt", "Barrierefreiheit nicht erfüllt", "Brandschutz erfüllt", "Brandschutz nicht erfüllt"],
                    "Anzahl": [anzahl, bf_gruen, bf_rot, bs_gruen, bs_rot]
                })

                col_f1, col_f2 = st.columns([1, 2])
                with col_f1:
                    st.subheader("Statistisches Fazit")
                    st.dataframe(fazit, use_container_width=True)
                with col_f2:
                    st.subheader("Gefilterte Bauteildaten")
                    st.dataframe(bericht, use_container_width=True)

            # ---- REGISTERKARTE 3: MÄNGELLISTE & EXCEL DOWNLOAD ----
            with tab3:
                st.header("Gesamte Konflikt- und Mängelliste")
                konfliktliste = gesamtbericht[gesamtbericht["Konflikt / Mangel"] != ""][
                    ["Geschoss", "Wohneinheit", "Raumbez.", "Raum-ID", "Bauteil", "Bauteil-ID", "Kriterium", "Konflikt / Mangel"]
                ]
                
                if not konfliktliste.empty:
                    st.error(f"Achtung: Es wurden {len(konfliktliste)} Mängel im Gebäude identifiziert.")
                    st.dataframe(konfliktliste, use_container_width=True)
                    
                    csv_daten = konfliktliste.to_csv(index=False, sep=";", encoding="utf-8-sig")
                    st.download_button(
                        label="📥 Mängelliste für Excel (.csv) herunterladen",
                        data=csv_daten,
                        file_name="maengelliste_brandschutz_barrierefreiheit.csv",
                        mime="text/csv"
                    )
                else:
                    st.success("Hervorragend! Es wurden keine Konflikte oder Mängel gefunden.")
        else:
            st.warning("⚠️ Keine auswertbaren Daten mit den aktuellen Regeln gefunden.")

    except Exception as e:
        st.error(f"❌ Ein kritischer Fehler ist beim Verarbeiten der Daten aufgetreten: {e}")
        st.info("Bitte überprüfe, ob das Tabellenformat mit der Dateivorlage übereinstimmt.")

else:
    st.info("💡 Bitte lade die Excel-Datei hoch, um die Auswertung zu starten.")